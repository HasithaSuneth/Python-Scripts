
import requests
from bs4 import BeautifulSoup
import re

def fetch_website_content(url):
    """Fetch the HTML content of the website."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def extract_words_from_html(html_content):
    """Extract words from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    # Get all visible text from the website
    text = soup.get_text(separator=' ')
    # Extract words using regex
    words = re.findall(r'\b\w+\b', text.lower())
    return list(set(words))  # Remove duplicates

def save_words_to_file(words, file_path):
    """Save the list of words to a text file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(sorted(words)))  # Sort for better readability
        print(f"Words saved to {file_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

def main():
    url = input("Enter the URL of the website (e.g. https://abc.com): ")
    # file_path = input("Enter the output file path (e.g., output.txt): ")
    file_path = "data/output.txt"

    print("Fetching website content...")
    html_content = fetch_website_content(url)

    if html_content:
        print("Extracting words...")
        words = extract_words_from_html(html_content)

        print(f"Extracted {len(words)} unique words.")
        save_words_to_file(words, file_path)

if __name__ == "__main__":
    main()
