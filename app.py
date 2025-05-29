from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def show_table():
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main revenue table (with class 'wikitable')
    table = soup.find('table', {'class': 'wikitable'})

    # Convert the table to a string of HTML
    table_html = str(table)

    # HTML Template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>US Companies by Revenue</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Top US Companies by Revenue (Live from Wikipedia)</h2>
        {table_html}
    </body>
    </html>
    """

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
