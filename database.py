import json
import random

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.load()
    
    def load(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except Exception as e:
            print(e)
    
    def save(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file)
        except Exception as e:
            print(e)
    
    def add_word(self, German, English, level, desc=None):
        if self.data:
            self.data.append({
                "id": len(self.data),  # This is a potential issue if cards are removed!
                "German": German,
                "English": English,
                "score": 0,
                "level": level
            })
        else:
            raise Exception("Data is empty")

    def remove_word(self, word_id):
        if self.data:
            for word in self.data:
                if word['id'] == word_id:
                    self.data.remove(word)
                    break
        else:
            raise Exception("Data is empty")
        
    def fetch_word(self, word_id):
        if self.data:
            for word in self.data:
                if word['id'] == word_id:
                    return word
        else:
            raise Exception("Data is empty")

    def update_score(self, word_id, score):
        if self.data:
            for word in self.data:
                if word['id'] == word_id:
                    word['score'] += score  # Add to score
                    break
        else:
            raise Exception("Data is empty")
    
    def fetch_all(self):
        if self.data:
            return self.data
        else:
            raise Exception("Data is empty")
    
    def fetch_reverse_sorted(self, limit=None):
        if self.data:
            if limit:
                return sorted(self.data, key=lambda x: x['score'])[::-1][:limit]
            else:
                return sorted(self.data, key=lambda x: x['score'])[::-1]
        else:
            raise Exception("Data is empty")

    def fetch_sorted(self, limit=None):
        if self.data:
            if limit:
                return sorted(self.data, key=lambda x: x['score'])[:limit]
            else:
                return sorted(self.data, key=lambda x: x['score'])
        else:
            raise Exception("Data is empty")

    def fetch_random(self, limit=None):
        if self.data:
            if limit:
                return random.sample(self.data, limit)
            else:
                return random.sample(self.data, len(self.data))
        else:
            raise Exception("Data is empty")
    
    def fetch_random_card(self):
        # Fetch a random card
        if self.data:
            return random.choice(self.data)
        else:
            return None

    def fetch_random_meaning(self):
        # Fetch a random English meaning
        if self.data:
            return random.choice(self.data)['English']
        else:
            return None
