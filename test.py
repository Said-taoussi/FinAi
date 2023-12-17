import requests

url = "https://api.openai.com/v1/files/file-Lu56mEZhIlFqXkmAy8IMCjmd/content"
response = requests.get(url)

if response.status_code == 200:
    # The file content is in response.content
    with open("downloaded_file.ext", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")