import requests
import json

def random_word():
    response = requests.get("https://api.urbandictionary.com/v0/random")

    return response.text

def parse_random_word(response_text):
    # Parse the JSON response
    data = json.loads(response_text)
    
    # Check if the response contains the 'list' key and if it's not empty
    if 'list' in data and data['list']:
        # Extract the first item from the 'list' array
        random_word_data = data['list'][0]
        
        # Extract word and definition
        word = random_word_data.get('word', 'N/A')
        definition = random_word_data.get('definition', 'N/A')
        
        return word, definition
    else:
        return None, None

if __name__ == "__main__":
    response_text = random_word()
    word, definition = parse_random_word(response_text)
    if word and definition:
        print("Random Word:", word)
        print("Definition:", definition)
    else:
        print("Unable to retrieve random word.")