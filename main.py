import requests
import argparse
import openai
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("url", help="Enter the github url you want to install ")
args = parser.parse_args()
url = requests.get(args.url)

if url.status_code == 200:
    readme_content = url.text


else:
    print(f"Failed to retrieve README file. Status code: {url.status_code}")

