import requests

def get_html(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch the HTML from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

def save_html(html_content, file_path):
    """
    Saves the HTML content to a file.

    Args:
        html_content (str): The HTML content to save.
        file_path (str): The path to save the file.

    Returns:
        None
    """
    with open(file_path, 'w') as file:
        file.write(html_content)

def load_html(file_path):
    """
    Loads the HTML content from a file.

    Args:
        file_path (str): The path to load the file from.

    Returns:
        str: The HTML content loaded from the file.
    """
    with open(file_path, 'r') as file:
        html_content = file.read()
    return html_content

# Add more utility functions for web crawling as needed
