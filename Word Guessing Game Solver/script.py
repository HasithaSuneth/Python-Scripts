import re
import sys
import json
import time
import inflect
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

# Cache dictionary
cache_file = "data/datamuse_cache.json"

def read_words_from_paragraph_file(file_path):
    """Reads a text file and extracts unique words from paragraphs."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            text = file.read()
    except FileNotFoundError:
        # Create an empty file if it does not exist
        with open(file_path, 'w', encoding='utf-8') as file:
            text = ""
        print(f"File '{file_path}' did not exist and has been created.")
        
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
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print("The URL does not contain valid HTML content.")
            return None
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

def load_cache():
    """Load the cache from a file."""
    try:
        with open(cache_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache):
    """Save the cache to a file."""
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
    except IOError as e:
        print(f"Error writing to cache: {e}")

def fetch_related_forms_from_datamuse(word, api_cache):
    """Fetch related forms (singular/plural) using Datamuse API with caching."""
    if word in api_cache:
        return set(api_cache[word])  # Return cached result

    url = f"https://api.datamuse.com/words?rel_gen={word}"
    try:
        response = requests.get(url)
        if response.status_code == 429:  # Too Many Requests
            print("Rate limit reached, sleeping for 1 second...")
            time.sleep(1)
            return fetch_related_forms_from_datamuse(word)
        response.raise_for_status()
        data = response.json()
        related_forms = [entry['word'] for entry in data]
        api_cache[word] = related_forms  # Cache the result
        save_cache(api_cache)  # Persist cache
        return set(related_forms)
    except requests.RequestException as e:
        print(f"Error fetching data from Datamuse API: {e}")
        return set()
    
def add_singular_plural_forms(words, api_cache):
    """
    Adds singular and plural forms of words to the list of words.
    Uses inflect for regular cases and Datamuse API for irregular cases.
    Keeps the original words while avoiding duplicates.
    """
    p = inflect.engine()
    updated_words = set(words)

    # for word in words:
    for word in tqdm(words, desc="Processing words", unit="word"):
        # Add singular form using inflect
        singular_form = p.singular_noun(word)
        if singular_form and singular_form != word:
            updated_words.add(singular_form)

        # Add plural form using inflect
        plural_form = p.plural_noun(word)
        if plural_form and plural_form != word:
            updated_words.add(plural_form)

        # Fetch related forms from Datamuse API as a fallback
        related_forms = fetch_related_forms_from_datamuse(word, api_cache)
        updated_words.update(related_forms)

    return list(updated_words)

def save_words_to_file(file_path, new_words, url):
    """
    Saves words to a file, preserving old data and avoiding duplicates.
    """
    try:
        # Read existing words from the file
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_words = set(file.read().split())  # Read and split into a set of unique words
        except FileNotFoundError:
            existing_words = set()  # If file doesn't exist, start with an empty set

        # Convert new_words to a set for comparison
        new_words_set = set(new_words)
        
        # Identify new unique words not already in the file
        new_unique_words = new_words_set - existing_words

        if new_unique_words:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"\n\n{url}\n")  # Double new line for clarity
                # Write new unique words sorted for readability
                file.write('\n'.join(sorted(new_unique_words)) + '\n')
            print(f"New words added to {file_path}")
        else:
            print("No new words to add. File remains unchanged.")

    except IOError as e:
        print(f"Error writing to file: {e}")
    
def separate_words_by_unique_characters(words):
    """
    Separates words into two lists:
    - One list with words where each character appears only once.
    - Another list with words where at least one character appears more than once.

    :param words: List of words to filter.
    :return: A tuple of two lists: (unique_char_words, duplicate_char_words).
    """
    unique_char_words = []
    duplicate_char_words = []

    for word in words:
        # Check if all characters in the word are unique
        if len(set(word)) == len(word):
            unique_char_words.append(word)
        else:
            duplicate_char_words.append(word)

    return unique_char_words, duplicate_char_words    

def main():
    print('Options:\n 1. With Words stored at the text file (data/text.txt).\n 2. With Web Scraping\n 3. Exit\n')
    option = input("Select an option: ")
    file_path = "data/text.txt"
    
    if option == "1":
        # Read words from a file
        words = read_words_from_paragraph_file(file_path)
    elif option == "2":
        # From web scrapping
        try:
            url = input("Enter the URL of the website (e.g. https://abc.com): ")
            html_content = fetch_website_content(url)
            words = extract_words_from_html(html_content)
            original_words = words
        except Exception as e:
           print("Failed to establish a connection to provided URL") 
           sys.exit()
    else:
        sys.exit()

    irregular_singular_plural_forms = input("\nDo you want to add singular, plural and irregular forms to word list? (yes/no): ").strip().lower()
    if irregular_singular_plural_forms == 'yes':
        try:
            # Load the cache at the start
            api_cache = load_cache()
            # Step 1: Add singular and plural forms
            words = add_singular_plural_forms(words, api_cache)
        except:
            print("Failed to add singular, plural and irregular forms to word list. continue with original word list.")
    
    print(f"\nLoaded {len(words)} unique words.")
    
    # Step 2: Filter by word length
    try:
        length = int(input("Enter the required word length: "))
        words = filter_by_length(words, length)
        unique_char_words, duplicate_char_words = separate_words_by_unique_characters(words)
        print(f"{len(words)} words have {length} characters.")
        print('Those words are:\nUnique Words: ', unique_char_words, '\n\nOther words: ', duplicate_char_words)
    except:
        print("Invalid word length")
        sys.exit()

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
        
    if option == "2":
        update_textfile = input("\nDo you want to add fetched words from URL to the text file (data/text.txt)? (yes/no): ").strip().lower()
        if update_textfile == 'yes':
            save_words_to_file(file_path, original_words, url)               

if __name__ == "__main__":
    main()
