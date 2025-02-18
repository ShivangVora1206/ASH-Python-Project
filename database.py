import json
import random
import copy
class Database:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.game_queue = None
        self.load()
        self.load_game_queue("Default")
    
    def load(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except Exception as e:
            print(e)
    
    def save(self):
        print("Saving data to file...")
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file)
        except Exception as e:
            print(e)
    
    def load_game_queue(self, game_mode):
        print("load_game_queue", game_mode)
        try:
            if game_mode == "Default":

                self.game_queue = copy.deepcopy(sorted(self.data, key=lambda x: x['score']))
            elif game_mode == "Level A1":
                print("loading game queue Level A1")
                self.game_queue = None
                self.game_queue = sorted([word for word in self.data if word['level'] == "A1"], key=lambda x: x['score'])
            elif game_mode == "Level A2":
                self.game_queue = None
                self.game_queue = sorted([word for word in self.data if word['level'] == "A2"], key=lambda x: x['score'])
            elif game_mode == "Level B1":
                self.game_queue = None
                self.game_queue = sorted([word for word in self.data if word['level'] == "B1"], key=lambda x: x['score'])
            elif game_mode == "Level B2":
                self.game_queue = None
                self.game_queue = sorted([word for word in self.data if word['level'] == "B2"], key=lambda x: x['score'])
            elif game_mode == "Level C1":
                self.game_queue = None
                self.game_queue = sorted([word for word in self.data if word['level'] == "C1"], key=lambda x: x['score'])
            elif game_mode == "Level C2":
                self.game_queue = None
                self.game_queue = sorted([word for word in self.data if word['level'] == "C2"], key=lambda x: x['score'])
            elif game_mode == "Limited":
                #TODO
                pass
            else:
                self.game_queue = copy.deepcopy(sorted(self.data, key=lambda x: x['score']))



        except Exception as e:
            print(e)

    def set_game_mode(self, game_mode):
        self.load_game_queue(game_mode)

    def add_word(self, German, English, level, desc=None):
        if self.data:
            self.data.append({
                "id": len(self.data),  # This is a potential issue if cards are removed!
                "German": German,
                "English": English,
                "score": 0,
                "level": level
            })
            self.save()
        else:
            raise Exception("Data is empty")

    def remove_word(self, word_id):
        if self.data:
            for word in self.data:
                if word['id'] == word_id:
                    print(f"Removing word: {word['German']} ({word['English']})")
                    self.data.remove(word)
                    self.save()
                    break
        else:
            raise Exception("Data is empty")
        
    def fetch_word_by_id(self, word_id):
        if self.data:
            for word in self.data:
                if word['id'] == word_id:
                    return word
        else:
            raise Exception("Data is empty")

    def update_score_in_game_queue(self, word_id, score):
        flag = False
        if self.game_queue:
            for word_index in range(len(self.game_queue)):
                if self.game_queue[word_index]['id'] == word_id:
                    self.game_queue[word_index]['score'] += score  # Add to score
                    temp = self.game_queue.pop(word_index)  # Remove from queue
                    print("update_score_in_game_queue temp after update", temp)
                    for i in range(len(self.game_queue)):
                        if self.game_queue[i]['score'] > temp['score']:
                            self.game_queue.insert(i, temp)
                            flag = True
                            break
                    break
            if not flag:
                self.game_queue.append(temp)
            self.update_score_in_db(word_id, score)
        else:
            raise Exception("Game queue is empty")
    
    def update_score_in_db(self, word_id, score):
        print("update_score_in_db word score param", score)
        if self.data:
            for word in self.data:
                if word['id'] == word_id:
                    print("update_score_in_db word before update", word)
                    word['score'] += score
                    print("update_score_in_db word after update", word)
                    self.save()
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
    
    def fetch_next_card(self):
        # Fetch the next card to study
        print("fetch_next_card", "game_queue", self.game_queue)
        if self.game_queue:
            return self.game_queue[0]
        else:
            return None
    
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
    
    def fetch_all_words_by_level(self, level):
        if self.data:
            return [word for word in self.data if word['level'] == level]
        else:
            raise Exception("Data is empty")
        
    def fetch_words_by_level(self, level, limit=None):
        if self.data:
            words = [word for word in self.data if word['level'] == level]
            if limit:
                return words[:limit]
            else:
                return words
        else:
            raise Exception("Data is empty")

    def fetch_random_by_level(self, level, limit=1):
        output = []
        for i in limit:
            output.append(random.choice(self.fetch_all_words_by_level(level)))
        return output
