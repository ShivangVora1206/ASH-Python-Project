import json
from google import generativeai as genai
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()

initials = ['a', 'b', 'c', 'd', 'd_1', 'd_2', 'd_3', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü', 'ß']
word_count = 0
with open('dataset.json', 'rb') as f:
    data = json.load(f)
    for initial in initials:
        chunk = []
        for i in data:
            if i['German'][0].lower() == initial:
                chunk.append(i)
                word_count += 1
        with open(f'chunks\\chunk_{initial}.json', 'w') as f:
            f.write(json.dumps(chunk))
print(word_count) #output: 953


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

for initial in initials:
    print("------------- Iteration:", initial, "-------------")
    chunk = ""

    with open(f'chunks\\chunk_{initial}.json', 'r') as f:
        chunk = f.read()

    if len(chunk) > 2:

        prompt = '''You are a German Language expert who is CEFR certified. Your task is to identify and label German words into CEFR categories. The categories are A1, A2, B1, B2, C1, and C2. You are given a json dictionary of words and your task is to identfy the CEFR level of the German word and return the same object with an extra field labelled level with the CEFR level. 
        example: input:{ "id": 0, "German": "abends", "English": "in the evening", "score": 0 }, output: { "id": 0, "German": "abends", "English": "in the evening", "score": 0, "level": "A1" }
        note: The output should be only a json object or list nothing else, do not encapsulate the output in anything else.
        input:
        '''+chunk

        try:
            response = model.generate_content(prompt)
            # print('response:', response.text)
            output = json.loads(response.text[8:-4])
            print(output[0])
            with open(f'outputs\\output_{initial}.json', 'w') as f:
                f.write(json.dumps(output))
        except Exception as e:
            print("Error:", e)
            print("Response:", response.text[8:-4])
    else:
        print("No data for this initial")

consolidated = []
for initial in initials:
    try:
        with open(f'outputs\\output_{initial}.json', 'r') as f:
            chunk = json.load(f)
            consolidated.extend(chunk)
    except Exception as e:
        print("Error:", e)
        print("No data for this initial")
    print("Length of consolidated:", len(consolidated))

with open('consolidated.json', 'w') as f:
    f.write(json.dumps(consolidated))