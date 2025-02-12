# from database import Database

# db = Database("temp_dataset.json")
# # print(db.fetch_word(1))
# # db.update_score(1, 1)
# # print(db.fetch_word(1))
# # print(db.fetch_all())
# # print(db.fetch_sorted())
# # print(db.fetch_reverse_sorted(limit=5))
# # db.save()
# print(db.fetch_random(3))

# from beolingus import Beolingus
# b = Beolingus()
# print("check ->")
# b.check()
# # print("info ->")
# # b.info("Haus")
# # print("show query ->", b.show_query("Haus", de=True, en=True, first=False, apart=False, ignorecase=True))
# # print(b.dict[10][0])
# # print(b.dict[10][1])
# print("show query ->")

# #to get reduced and only relevant responses matching only the first word instead of every subsequence in all words
# print(b.show_query("Einfach", de=True, en=True, first=True, apart=True, ignorecase=True)) 

import configparser

c = configparser.ConfigParser()
c.read_file(open('config.ini'))
print(c.get('beodict', 'win_title'))