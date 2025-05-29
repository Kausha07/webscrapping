from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Company Data by Rank</title>
    {% raw %}
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: auto; }
        input[type=number] { padding: 8px; width: 80px; }
        button { padding: 8px 12px; margin-left: 10px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .error { color: red; margin-top: 20px; }
    </style>
    {% endraw %}
</head>
<body>
    <h1>US Companies by Revenue - Search by Rank</h1>
    <form method="get">
        <label for="rank">Enter Rank:</label>
        <input type="number" name="rank" id="rank" min="1" required value="{{rank or ''}}">
        <button type="submit">Show Company</button>
    </form>

    {% if row_html %}
        <h2>Company Details for Rank {{rank}}</h2>
        <table>
            {{row_html | safe}}
        </table>
    {% elif rank %}
        <p class="error">No company found with Rank {{rank}}.</p>
    {% endif %}
</body>
</html>
"""


@app.route('/', methods=['GET'])
def index():
    rank = request.args.get('rank')
    row_html = None

    if rank and rank.isdigit():
        rank = int(rank)

        url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first wikitable class table (the main revenue table)
        table = soup.find('table', {'class': 'wikitable'})

        if table:
            # Find all rows (skip header)
            rows = table.find_all('tr')[1:]
            
            # Search for the row matching the Rank input (Rank is in the first column)
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if cols:
                    # The Rank is usually in the first column
                    rank_text = cols[0].get_text(strip=True)
                    # Sometimes rank can have footnotes/sup tags, so clean it
                    try:
                        rank_num = int(rank_text)
                    except:
                        continue
                    if rank_num == rank:
                        # Extract this row as HTML, but only the row (without <table>)
                        # We'll generate header row manually for better control
                        # Extract all column headers from original table header for display:
                        headers = [th.get_text(strip=True) for th in table.find('tr').find_all('th')]

                        # Create HTML for header row
                        header_html = '<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>'
                        # Current matched row HTML
                        row_html = header_html + str(row)
                        break

    return render_template_string(HTML, rank=rank, row_html=row_html)


if __name__ == '__main__':
    app.run(debug=True)
