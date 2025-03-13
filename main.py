import requests
import argparse
import openai
from bs4 import BeautifulSoup
from github import Github
import re


parser = argparse.ArgumentParser()
parser.add_argument("url", help="Enter the github url you want to install ")
args = parser.parse_args()
url = requests.get(args.url)
readme_string =  ''

g = Github("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")

# Parse the URL to extract the username and repository name
match = re.match(r"https://github\.com/([^/]+)/([^/]+)(?:/blob/([^/]+)/(.+))?", str(args.url))

if match:
    username = match.group(1)
    repo_name = match.group(2)

    # Get the repository
    repo = g.get_repo(f"{username}/{repo_name}")

    # Print repository details (for example, the README)
    readme = repo.get_readme()
    print(readme.decoded_content.decode('utf-8'))
else:
    print("Invalid URL format.")

