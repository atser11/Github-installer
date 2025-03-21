import requests
import argparse
from openai import OpenAI
from bs4 import BeautifulSoup
from github import Github
import re
import subprocess

username = ''
repo_name = ''
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


repo = g.get_repo(f"{username}/{repo_name}")

# Function to list files and directories in the repository and return a list
def list_files_and_folders(repo, path=""):
    file_list = []
    contents = repo.get_contents(path)
    for content_file in contents:
        file_list.append(content_file.path)
        if content_file.type == "dir":
            # If it's a directory, you can recursively call this function to get its contents
            file_list.extend(list_files_and_folders(repo, content_file.path))
    return file_list

# Call the function to list files and folders in the repository
file_structure = list_files_and_folders(repo)


client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages = [
    {
        "role": "user",
        "content": f"""
        From the Read.me below, create a single bash script that would be a step-by-step installation of the GitHub program. 
        Assume I am using an Ubuntu machine, and let the bash script contain the necessary commands to run the program
        and should navigate to the directory and run the program. 
        When done with the bash script, end it with '###':

        {readme_str}

        If not enough information is given in the Readme, use the file structure below to make a reasonable guess and create a single bash script that would be a step-by-step installation of the GitHub program:

        {file_structure}

        To clone the repository, first create a new folder for the program and navigate into it. Use the following commands to do this:
        
        mkdir program_folder_name
        cd program_folder_name
        
        Then, clone the repository with this command:
        git clone https://github.com/{username}/{repo_name}
        
        After cloning, navigate into the cloned repository and make sure to run the program.
        """
    }
])
chatgpt_message = completion.choices[0].message.content


# Define the regex pattern to capture content between ```bash and ###
pattern = r"```bash(.*?)###"

# Search for the pattern
match = re.search(pattern, chatgpt_message, re.DOTALL)

# If a match is found, print the captured content
if match:
    print("Match found")
else:
    print("No match found.")

# Define the file path where you want to create the script
file_path = "installer.sh"

# Write the Bash script to the file
with open(file_path, "w") as file:
    file.write(str(match.group(1).strip()))

# Print confirmation
print(f"Bash script has been created and saved as {file_path}")

subprocess.run(["chmod", "+x", file_path])

# Run the Bash script using subprocess
try:
    result = subprocess.run([f"./{file_path}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Script executed successfully.")
    print("Output:", result.stdout.decode())
except subprocess.CalledProcessError as e:
    print("Error executing script.")
    print("Error:", e.stderr.decode())