import re
import sys
import requests
from bs4 import BeautifulSoup

def read_words_from_paragraph_file(file_path):
    """Reads a text file and extracts unique words from paragraphs."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        text = file.read()
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words (case-insensitive)
    return list(set(words))  # Remove duplicates and return as a list

def filter_by_length(words, length):
    """Filters words by their length."""
    return [word for word in words if len(word) == length]

def filter_by_character_position(words, char_positions):
    """
    Filters words based on characters at specific positions.
    :param char_positions: Dictionary with 0-based positions as keys and expected characters as values.
    """
    filtered_words = []
    for word in words:
        match = all(len(word) > pos and word[pos] == char for pos, char in char_positions.items())
        if match:
            filtered_words.append(word)
    return filtered_words

def filter_by_included_characters(words, included_chars):
    """
    Filters words to include specific characters anywhere.
    :param included_chars: List of characters that must appear in the word.
    """
    return [word for word in words if all(char in word for char in included_chars)]

def filter_words_by_excluded_characters(words, excluded_chars):
    """Filters out words that contain any of the excluded characters."""
    excluded_set = set(excluded_chars)  # Convert to set for efficient checks
    return [word for word in words if not any(char in excluded_set for char in word)]

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

def apply_filter(words, filter_type):
    """Apply a filter based on the type and user input."""
    if filter_type == "position":
        specific_positions = input("\nEnter specific positions and characters (e.g., 0:a,2:c) or press Enter to skip: ")
        if specific_positions.strip():
            try:
                char_positions = {int(pos): char for pos, char in (item.split(':') for item in specific_positions.split(','))}
                return filter_by_character_position(words, char_positions)
            except ValueError:
                print("Invalid input format. Skipping this filter.")
        else:
            print("Skipped filtering by specific positions.")
    elif filter_type == "include":
        included_chars = input("\nEnter characters that must appear in the word (comma-separated) or press Enter to skip: ")
        if included_chars.strip():
            return filter_by_included_characters(words, included_chars.split(','))
        else:
            print("Skipped filtering by included characters.")
    elif filter_type == "exclude":
        excluded_chars = input("\nEnter characters that must not appear in the word (comma-separated) or press Enter to skip: ")
        if excluded_chars.strip():
            return filter_words_by_excluded_characters(words, excluded_chars.split(','))
        else:
            print("Skipped filtering by excluded characters.")
    return words


def main():
    print('Options:\n 1. With Words stored at the text file (data/text.txt).\n 2. With Web Scraping\n 3. Exit\n')
    option = input("Select an option: ")
    
    if option == "1":
        # Read words from a file
        file_path = "data/text.txt"
        words = read_words_from_paragraph_file(file_path)
        print(f"Loaded {len(words)} unique words.")
    elif option == "2":
        # From web scrapping
        try:
            url = input("Enter the URL of the website (e.g. https://abc.com): ")
            html_content = fetch_website_content(url)
            words = extract_words_from_html(html_content)
            print(f"Loaded {len(words)} unique words.")
        except Exception as e:
           print(e) 
           sys.exit()
    else:
        sys.exit()

    # Step 2: Filter by word length
    length = int(input("Enter the required word length: "))
    words = filter_by_length(words, length)
    print(f"{len(words)} words have {length} characters.")
    print('Those words are:', words)

    while len(words) > 1:
        print("\nStarting a new filtering round...")
        for filter_type in ["position", "include", "exclude"]:
            words = apply_filter(words, filter_type)
            print(f"{len(words)} words remain after filtering.")
            print('Those words are: ', words)
            if len(words) <= 1:
                break

        if len(words) > 1:
            continue_filtering = input("\nDo you want to continue filtering? (yes/no): ").strip().lower()
            if continue_filtering != 'yes':
                break

    # Final output
    print("\nFiltered Words:")
    if words:
        for word in words:
            print(word)
    else:
        print("No words match the criteria.")

if __name__ == "__main__":
    main()
