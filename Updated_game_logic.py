from tkinter import *
from tkinter import ttk, font as tkFont
from tkextrafont import Font
import random
from PIL import Image, ImageTk  # For handling images
from database import Database

import beolingusTk

db = Database("temp_dataset.json")  # Use your dataset here

# Initialize Tkinter
root = Tk()
root.title("Anki Flashcards")
root.geometry("1280x720")  # Window size is fixed to 500x400
root.minsize(200, 150)

custom_font = Font(family="Times")
fontL = tkFont.Font(family="Times", size=20)
fontM = tkFont.Font(family="Times", size=15)

style = ttk.Style()
style.configure("Rounded.TButton", 
                borderwidth=1, 
                relief="solid", 
                padding=10,
                background="#cc0000", 
                font=(fontM, 12),
                foreground="black",
                )

# Load the background image
background_image_path = r"Final_Card_Font.jpg"
background_image = Image.open(background_image_path)
background_image = background_image.resize((1280, 720))  # Resize to fit the window
bg_image_tk = ImageTk.PhotoImage(background_image)

canvas_image = None
# Frames for pages
page_main = Frame(root)
page_game = Frame(root)

# Current card and answer variables
current_card = None
options = []

# Functions to handle the game logic and navigation
def show_main_menu():
    page_game.pack_forget()
    page_main.pack(expand=True)

def start_game():
    page_main.pack_forget()
    page_game.pack(expand=True)
    load_next_card()

# def update_button_positions(event):
#     # Get the current size of the canvas
#     canvas_width = event.width
#     canvas_height = event.height

#     # Calculate the positions of the buttons as fractions of canvas size
#     canvas_game.create_window(canvas_width * 0.25, canvas_height * 0.25, window=option_buttons[0])
#     canvas_game.create_window(canvas_width * 0.75, canvas_height * 0.25, window=option_buttons[1])
#     canvas_game.create_window(canvas_width * 0.25, canvas_height * 0.75, window=option_buttons[2])
#     canvas_game.create_window(canvas_width * 0.75, canvas_height * 0.75, window=option_buttons[3])

#     update_image_scale(event)

# def update_image_scale(event):
#     global canvas_image
#     # print("Image scale updated")
#     canvas_width = event.width
#     canvas_height = event.height

#     # Resize the image to fit the canvas
#     bg_image_resized = background_image.resize((canvas_width, canvas_height))
#     bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
#     canvas_game.create_image(0, 0, anchor=NW, image=bg_image_tk)
#     canvas_image = bg_image_tk

def update_canvas_binding(event):
    global canvas_image
    # print("Image scale updated")
    canvas_width = event.width
    canvas_height = event.height

    canvas_game.create_window(canvas_width * 0.35, canvas_height * 0.35, window=option_buttons[0])
    canvas_game.create_window(canvas_width * 0.65, canvas_height * 0.35, window=option_buttons[1])
    canvas_game.create_window(canvas_width * 0.35, canvas_height * 0.65, window=option_buttons[2])
    canvas_game.create_window(canvas_width * 0.65, canvas_height * 0.65, window=option_buttons[3])

    canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.10, window=word_label)
    canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.80, window=feedback_label)
    canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.85, window=button_back)

    # Resize the image to fit the canvas
    bg_image_resized = background_image.resize((canvas_width, canvas_height))
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
    canvas_game.create_image(0, 0, anchor=NW, image=bg_image_tk)
    canvas_image = bg_image_tk

def load_next_card():
    global current_card, options
    
    card_data = db.fetch_random_card()  # Fetch a random card from the database
    if not card_data:
        feedback_label.config(text="No more cards available!", fg="red")
        return

    current_card = card_data
    word_label.config(text=current_card['German'])  # Display the German word

    correct_answer = current_card['English']  # The correct answer is the English meaning
    options = [correct_answer]

    # Populate remaining options with random meanings
    while len(options) < 4:
        random_option = db.fetch_random_meaning()  # Fetch a random meaning
        if random_option not in options:
            options.append(random_option)

    random.shuffle(options)

    # Update option buttons
    for idx, option in enumerate(options):
        option_buttons[idx].config(text=option, command=lambda opt=option: check_answer(opt))

def check_answer(selected_option):
    global current_card

    if selected_option == current_card['English']:  # Check against the correct answer (English meaning)
        feedback_label.config(text="Congratulations, Correct Answer", fg="green", bg="#ffffff")
        db.update_score(current_card['id'], score=1)  # Increment score by 1 for correct answer
    else:
        feedback_label.config(text="Wrong Answer. Try Again!", fg="red", bg="#ffffff")
        db.update_score(current_card['id'], score=-1)  # Decrement score by 1 for wrong answer

    # Delay before loading the next card
    root.after(1000, load_next_card)  # 1 second delay before loading the next card

frame_main_top = Frame(page_main)
frame_main_top.pack(expand=True, fill='both', side='top')

frame_main_bottom = Frame(page_main, pady=20)
frame_main_bottom.pack(expand=True, fill='both', side='bottom')

label_main = Label(frame_main_top, text="Anki Flashcards", font=fontL, fg='blue', bg='white')
label_main.pack(expand=True, anchor='center')

button_start = ttk.Button(frame_main_bottom, text="Start Game",  command=start_game, style="Rounded.TButton")
button_start.pack(expand=True, anchor='center')

button_exit = Button(frame_main_bottom, text="Exit", font=fontM, command=root.quit)
button_exit.pack(expand=True, anchor='center')

# Game Page
canvas_game = Canvas(page_game, width=1800, height=1200)
canvas_game.pack(fill="both", expand=True)

# Add the background image to the canvas
canvas_image = canvas_game.create_image(0, 0, anchor=NW, image=bg_image_tk)

# Place widgets over the canvas
word_label = Label(canvas_game, text="", font=fontL, fg='black', bg="#ffffff")
canvas_game.create_window(250, 90, window=word_label)

option_buttons = [Button(canvas_game, text="", font=fontM, bg="#ffffff") for _ in range(4)]
for idx, btn in enumerate(option_buttons):
    canvas_game.create_window(250, 150 + idx* 40, window=btn)

feedback_label = Label(canvas_game, text="", font=fontM, fg='red', bg="#5c0001")
canvas_game.create_window(250, 310, window=feedback_label)

button_back = Button(canvas_game, text="Back to Menu", font=fontM, command=show_main_menu, bg="#ffffff")
canvas_game.create_window(250, 350, window=button_back)

# Update button positions when the window is resized
# canvas_game.bind("<Configure>", update_image_scale)
canvas_game.bind("<Configure>", update_canvas_binding)



# Integrate beolingus, which does a window of it's own.
# Add a button somewhere here
# that opens a new window with beolingus info.
# Find a way to update info in beolingus window.

def update_beoli():
    global current_card
    if current_card == None:
        word = "Python"
    else: word = current_card["German"]
    beoli.update (word)

beoli = beolingusTk.Window()
button_beoli= Button (frame_main_bottom, text="beoli", command=update_beoli, font=fontM)
button_beoli.pack()



# Initial Setup
show_main_menu()
# update_button_positions(None)
root.mainloop()
