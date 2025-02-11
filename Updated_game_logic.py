from tkinter import *
from tkinter import ttk, font as tkFont
from tkextrafont import Font
import random
from PIL import Image, ImageTk  # For handling images
from database import Database
from beolingus import Beolingus


db = Database("temp_dataset.json")  # Use your dataset here
b = Beolingus()
print("check ->")
b.check()

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
page_more_info = Frame(root)
# Current card and answer variables
current_card = None
options = []

card_label_toggle_state = False
card_label_frame = None
card_label = None
feedback_label = None
# Functions to handle the game logic and navigation
# Functions to handle the game logic and navigation
def show_main_menu():
    page_game.pack_forget()
    page_more_info.pack_forget()
    page_main.pack(expand=True)

def start_game(back=False):
    page_main.pack_forget()
    page_more_info.pack_forget()
    page_game.pack(expand=True)
    if not back:
        load_next_card()

def show_more_info():
    page_game.pack_forget()
    page_main.pack_forget()
    page_more_info.pack(expand=True)
    more_info_german_label.config(text=current_card['German'])
    more_info_content_label.config(text=load_more_info(current_card))


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
    global card_label_toggle_state
    global card_label_frame
    # print("Image scale updated")
    canvas_width = event.width
    canvas_height = event.height

    canvas_game.create_window(canvas_width * 0.35, canvas_height * 0.45, window=option_buttons[0])
    canvas_game.create_window(canvas_width * 0.65, canvas_height * 0.45, window=option_buttons[1])
    canvas_game.create_window(canvas_width * 0.35, canvas_height * 0.55, window=option_buttons[2])
    canvas_game.create_window(canvas_width * 0.65, canvas_height * 0.55, window=option_buttons[3])

    canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.25, window=card_label_frame)

    # if card_label_frame and card_label_toggle_state:
    #     canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.50, window=card_label_frame)

    if feedback_label:
        canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.80, window=feedback_label)
    canvas_game.create_window(canvas_width * 0.42, canvas_height * 0.85, window=button_back)
    canvas_game.create_window(canvas_width * 0.47, canvas_height * 0.85, window=button_flip)
    canvas_game.create_window(canvas_width * 0.52, canvas_height * 0.85, window=button_next)
    canvas_game.create_window(canvas_width * 0.57, canvas_height * 0.85, window=button_more_info)

    # Resize the image to fit the canvas
    bg_image_resized = background_image.resize((canvas_width, canvas_height))
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
    canvas_game.create_image(0, 0, anchor=NW, image=bg_image_tk)
    canvas_image = bg_image_tk

def load_next_card():
    global current_card, options, feedback_label, card_label
    if feedback_label:
        feedback_label.destroy()
    if button_next:
        button_next.config(state=DISABLED)
    card_data = db.fetch_random_card()  # Fetch a random card from the database
    if not card_data:
        feedback_label.config(text="No more cards available!", fg="red")
        return

    current_card = card_data
    card_label.config(text=current_card['German'])  # Display the German word

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

def load_more_info(card):
    print("card", card)
    if card:
        word = card['German']
        return b.show_query(word, de=True, en=True, first=True, apart=True, ignorecase=True)
    else:
        return "Not found"

def card_label_toggle():
    global card_label_toggle_state
    global card_label
    print("toggle state", card_label_toggle_state)
    if card_label_toggle_state:
        card_label.config(text=current_card['German'])
        card_label_toggle_state = False
    else:
        #TODO instead of label make it a frame
        # card_label_frame = Frame(canvas_game, bg='white', padx=10, pady=10)
        # card_label = Label(card_label_frame, text="temp", font=fontM, fg='black')
        # card_label.pack(expand=True)
        # canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.50, window=card_label_frame)
        card_label.config(text=current_card['German']+'\n'+current_card['English'])
        card_label_toggle_state = True
    button_next.config(state=NORMAL)


def check_answer(selected_option):
    global current_card
    global feedback_label
    if feedback_label:
        feedback_label.destroy()
    feedback_label = Label(canvas_game, text="", font=fontM, fg='red', bg="#5c0001")
    if selected_option == current_card['English']:  # Check against the correct answer (English meaning)
        
        feedback_label.config(text="Congratulations, Correct Answer", fg="green", bg="#ffffff")
        canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.80, window=feedback_label)

        db.update_score(current_card['id'], score=1)  # Increment score by 1 for correct answer
    else:
        feedback_label.config(text="Wrong Answer. Try Again!", fg="red", bg="#ffffff")
        canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.80, window=feedback_label)
        db.update_score(current_card['id'], score=-1)  # Decrement score by 1 for wrong answer
    button_next.config(state=NORMAL)
    # Delay before loading the next card
    # root.after(1000, load_next_card)  # 1 second delay before loading the next card

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
# word_label = Label(canvas_game, text="", font=fontL, fg='black', bg="#ffffff")
# canvas_game.create_window(250, 90, window=word_label)

option_buttons = [Button(canvas_game, text="", font=fontM, bg="#ffffff") for _ in range(4)]
for idx, btn in enumerate(option_buttons):
    canvas_game.create_window(250, 150 + idx* 40, window=btn)

# canvas_game.create_window(250, 310, window=feedback_label)

button_back = Button(canvas_game, text="Exit", font=fontM, command=show_main_menu, bg="#ffffff")
canvas_game.create_window(250, 350, window=button_back)

button_flip = Button(canvas_game, text="Flip", font=fontM, command=card_label_toggle, bg="#ffffff")
canvas_game.create_window(250, 390, window=button_flip)

button_next = Button(canvas_game, text="Next", font=fontM, state=DISABLED, command=load_next_card, bg="#ffffff")
canvas_game.create_window(250, 430, window=button_next)

button_more_info = Button(canvas_game, text="More", font=fontM, command=show_more_info, bg="#ffffff")
canvas_game.create_window(250, 470, window=button_more_info)


# card_label = Label(canvas_game, text="Flipped!", font=fontM, fg='black', bg='yellow')
# canvas_game.create_window(250, 430, window=card_label)
card_label_frame = Frame(canvas_game, bg='white', padx=40, pady=40)
card_label = Label(card_label_frame, text="", font=fontL, fg='black')
card_label.pack(expand=True)

# Create buttons to control the visibility of the label
# button_toggle = Button(canvas_game, text="Toggle Card Label", command=card_label_toggle, bg="#ffffff")
# canvas_game.create_window(250, 470, window=button_toggle)

# Update button positions when the window is resized
# canvas_game.bind("<Configure>", update_image_scale)

# More Info Page
frame_more_info = Frame(page_more_info, bg='white', padx=10, pady=10)
frame_more_info.pack(expand=True)

more_info_german_label = Label(frame_more_info, text="", font=fontL, fg='black')
more_info_german_label.pack(expand=True)

more_info_content_label = Label(frame_more_info, text="", font=fontM, fg='black')
more_info_content_label.pack(expand=True)
more_info_back_button = Button(frame_more_info, text="Back", font=fontM, command=lambda: start_game(True), bg="#ffffff")
more_info_back_button.pack(expand=True)

# canvas_game.create_window(250, 470, window=more_info_back_button)


canvas_game.bind("<Configure>", update_canvas_binding)

# Initial Setup
show_main_menu()
# update_button_positions(None)
root.mainloop()
