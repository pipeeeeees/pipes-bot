import requests
import json
    
def random_popular_word():
    while True:
        response = requests.get("https://api.urbandictionary.com/v0/random")
        data = json.loads(response.text)
        
        for word_data in data['list']:
            word = word_data.get('word', '').strip()
            thumbs_up = word_data.get('thumbs_up', 0)
            # Check if the word is one word and consists only of alphabetic characters
            if word and len(word.split()) == 1 and word.isalpha() and thumbs_up >= 100:
                definition = word_data.get('definition', 'N/A')
                # Remove square brackets from the definition
                definition = definition.replace("[", "").replace("]", "")
                return word, definition

if __name__ == "__main__":
    word, definition = random_popular_word()
    if word and definition:
        print("Random Word:", word)
        print("Definition:", definition)
    else:
        print("Unable to retrieve random word.")
