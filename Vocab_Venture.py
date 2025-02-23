import random

# Vocabulary data categorized by levels
vocabulary = {
    "A1.1": [
        {"word": "Apfel", "meaning": "Apple", "score": 0},
        {"word": "Auto", "meaning": "Car", "score": 0},
        {"word": "Buch", "meaning": "Book", "score": 0},
        {"word": "Haus", "meaning": "House", "score": 0},
        {"word": "Hund", "meaning": "Dog", "score": 0}
    ],
    "A1.2": [
        {"word": "Katze", "meaning": "Cat", "score": 0},
        {"word": "Stuhl", "meaning": "Chair", "score": 0},
        {"word": "Tisch", "meaning": "Table", "score": 0},
        {"word": "Blume", "meaning": "Flower", "score": 0},
        {"word": "Baum", "meaning": "Tree", "score": 0}
    ],
    "A2.1": [
        {"word": "Tür", "meaning": "Door", "score": 0},
        {"word": "Fenster", "meaning": "Window", "score": 0},
        {"word": "Garten", "meaning": "Garden", "score": 0},
        {"word": "Freund", "meaning": "Friend", "score": 0},
        {"word": "Familie", "meaning": "Family", "score": 0}
    ],
    "A2.2": [
        {"word": "Arzt", "meaning": "Doctor", "score": 0},
        {"word": "Lehrer", "meaning": "Teacher", "score": 0},
        {"word": "Schule", "meaning": "School", "score": 0},
        {"word": "Essen", "meaning": "Food", "score": 0},
        {"word": "Wasser", "meaning": "Water", "score": 0}
    ]
}

def play_level(level):
    words = vocabulary[level]
    while words:
        # Select a random word from the current level
        current_word = random.choice(words)
        print(f"Word: {current_word['word']}")
        user_input = input("Do you know this word? (yes/no): ").strip().lower()
        
        if user_input == 'yes':
            # User knows the word, reduce score
            current_word['score'] += 1
            print("Correct!\n")
        elif user_input == 'no':
            # User doesn't know the word, show meaning
            print(f"Correct meaning: {current_word['meaning']}")
            print("Try again.\n")
        else:
            print("Invalid input. Please respond with 'yes' or 'no'.\n")
        
        # Remove word from list if score is 1 (all known)
        if current_word['score'] >= 1:
            words.remove(current_word)
    
    print(f"Congratulations! You've completed {level} level.\n")

def main():
    level = "A1.1"
    
    while level:
        print(f"Starting {level} level...\n")
        play_level(level)
        
        # Proceed to next level if current one is completed
        if not vocabulary[level]:
            if level == "A1.1":
                level = "A1.2"
            elif level == "A1.2":
                level = "A2.1"
            elif level == "A2.1":
                level = "A2.2"
            else:
                level = None # Game over

if __name__ == "__main__":
    main()
