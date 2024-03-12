import requests
import os
from pprint import pprint

def get_doi(article_title):
    # Base URL for Core API
    base_url = "https://core.ac.uk:443/api-v2/articles/search"

    # Parameters for the query
    params = {
        "apiKey": os.getenv("CORE_API"),  # Replace "YOUR_API_KEY" with your actual API key
        "query": f"title:({article_title})",
        "pageSize": 1  # Limiting to 1 result
    }

    try:
        # Sending GET request to Core API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extracting DOI from the response
        data = response.json()
        pprint(data)
        """
        if data.get("data"):
            doi = data["data"][0].get("doi")
            return doi
        else:
            return "DOI not found"
        """
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Test the function
article_title = input("Enter the title of the article: ")
doi = get_doi(article_title)
print("DOI:", doi)
