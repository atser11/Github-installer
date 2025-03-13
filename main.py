import requests
import argparse
from openai import OpenAI
from bs4 import BeautifulSoup
from github import Github
import re


parser = argparse.ArgumentParser()
parser.add_argument("url", help="Enter the github url you want to install ")
args = parser.parse_args()
url = requests.get(args.url)
readme_str = ''

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
    readme_str =readme.decoded_content.decode('utf-8')
    #print(readme.decoded_content.decode('utf-8'))
else:
    print("Invalid URL format.")



client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "From the Read me create a step by step installation of this github program: "+ readme_str }
  ]
)

print(completion.choices[0].message);
