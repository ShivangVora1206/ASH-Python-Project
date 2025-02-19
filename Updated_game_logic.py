from tkinter import *
from tkinter import ttk, font as tkFont
from tkinter.filedialog import asksaveasfilename
from tkextrafont import Font
import random
from PIL import Image, ImageTk  # For handling images
from database import Database
from beolingus import Beolingus
import configparser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = configparser.ConfigParser()
c.read_file(open('config.ini'))
db = Database(c.get("ASHConfig", "db_path"))  # Use your dataset here
b = Beolingus()
print("check ->")
b.check()

# Initialize Tkinter
root = Tk()
root.title(c.get('ASHConfig', 'root_title'))
root.geometry(c.get('ASHConfig', 'root_geometry'))  # Window size is fixed to 500x400
root.minsize(c.getint('ASHConfig', 'root_min_x'), c.getint('ASHConfig', 'root_min_y'))

custom_font1 = Font(file="Montserrat-Regular.ttf", family="Montserrat")
custom_font2 = Font(file="AlteHaasGroteskBold.ttf", family="Alte Haas Grotesk Bold")
custom_font3 = Font(file="Minecraft.ttf", family="Minecraft")

fontXL = tkFont.Font(family="Minecraft", size=48)
fontL = tkFont.Font(family="Alte Haas Grotesk Bold", size=24)
fontM = tkFont.Font(family="Montserrat", size=15)

style = ttk.Style()
style.configure("Rounded.TButton", 
                borderwidth=2, 
                relief="solid", 
                padding=5,
                background="#1ecbe1", 
                font=('Montserrat', 15),
                foreground="black")

style.configure("Custom.TButton", 
                borderwidth=1, 
                relief="solid", 
                padding=10,
                background="#c637c8", 
                font=('Montserrat', 15),
                foreground="black"
                )
# style.theme_use('clam')

style.configure("CustomNext.TButton", 
                borderwidth=2, 
                relief="solid", 
                padding=5,
                background="green", 
                font=('Montserrat', 15, 'bold'),
                foreground="black",)




# Load the background image
background_image_path = c.get('ASHConfig', 'background_image_path')
background_image = Image.open(background_image_path)
background_image = background_image.resize((c.getint("ASHConfig", "root_x"), c.getint("ASHConfig", "root_y")))  # Resize to fit the window
bg_image_tk = ImageTk.PhotoImage(background_image)

canvas_image = None
# Frames for pages
page_main = Frame(root)
page_game = Frame(root)
page_more_info = Frame(root)
page_add_card = Frame(root)
page_remove_card = Frame(root)
page_result = Frame(root)
# Current card and answer variables
current_card = None
options = []

card_label_toggle_state = False
card_label_frame = None
card_label = None
feedback_label = None
user_level_label = None
button_result = None
threshold = c.getint("ASHConfig", "threshold")
game_modes = ["Default", "Level A1", "Level A2", "Level B1", "Level B2", "Level C1", "Level C2", "Test"]
selected_game_mode = game_modes[0]
selected_game_mode_var = StringVar(value=selected_game_mode)
option_length_limit = c.getint("ASHConfig", "option_length_limit")
# Functions to handle the game logic and navigation
def show_main_menu():
    page_game.pack_forget()
    page_more_info.pack_forget()
    page_add_card.pack_forget()
    page_remove_card.pack_forget()
    page_main.pack(expand=True)

def start_game(back=False):
    global card_label_toggle_state, selected_game_mode, current_card
    selected_game_mode = selected_game_mode_var.get()
    db.set_game_mode(selected_game_mode)
    if selected_game_mode == "Test":
        button_flip.config(state=DISABLED)
    else:
        button_flip.config(state=NORMAL)
    current_card = None
    card_label_toggle_state = False
    page_main.pack_forget()
    page_more_info.pack_forget()
    page_result.pack_forget()
    page_game.pack(expand=True)
    if not back:
        load_next_card()

def show_more_info():
    page_game.pack_forget()
    page_main.pack_forget()
    page_more_info.pack(expand=True)
    more_info_german_label.config(text=current_card['German'])
    more_info_content_label.config(text=load_more_info(current_card))

def show_add_card():
    page_main.pack_forget()
    page_add_card.pack(expand=True)

def show_remove_card():
    page_main.pack_forget()
    page_remove_card.pack(expand=True)

def show_result_page():
    result = db.evaluate_result(selected_game_mode)
    if result:
        result_predicted_level.config(text=f"Predicted Level: {result['predicted_level']}")
        result_total_score.config(text=f"Total Score: {result['total_score']}")
        result_scores.config(text=f"Scores by Level: {result['scores']}")
    page_game.pack_forget()
    page_result.pack(expand=True)


def update_canvas_binding(event):
    global canvas_image
    global card_label_toggle_state
    global card_label_frame
    # print("Image scale updated")
    canvas_width = event.width
    canvas_height = event.height

    # Resize the image to fit the canvas
    bg_image_resized = background_image.resize((canvas_width, canvas_height))
    bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
    canvas_game.create_image(0, 0, anchor=NW, image=bg_image_tk)
    canvas_image = bg_image_tk

    canvas_game.create_window(canvas_width * 0.30, canvas_height * 0.45, window=option_buttons[0])
    canvas_game.create_window(canvas_width * 0.70, canvas_height * 0.45, window=option_buttons[1])
    canvas_game.create_window(canvas_width * 0.30, canvas_height * 0.55, window=option_buttons[2])
    canvas_game.create_window(canvas_width * 0.70, canvas_height * 0.55, window=option_buttons[3])

    canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.25, window=card_label_frame)

    # if card_label_frame and card_label_toggle_state:
    #     canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.50, window=card_label_frame)

    if feedback_label:
        # print("feedback label ->", feedback_label)
        canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.75, window=feedback_label)
    
    if user_level_label:
        canvas_game.create_window(canvas_width * 0.50, canvas_height * 0.65, window=user_level_label)

    canvas_game.create_window(canvas_width * 0.22, canvas_height * 0.85, window=button_back)
    canvas_game.create_window(canvas_width * 0.42, canvas_height * 0.85, window=button_flip)
    canvas_game.create_window(canvas_width * 0.62, canvas_height * 0.85, window=button_next)
    canvas_game.create_window(canvas_width * 0.82, canvas_height * 0.85, window=button_more_info)

def update_more_info_binding(event):
    # frame_more_info.config(width=page_width, height=page_height)
    more_info_content_label.config(wraplength=root.winfo_width()-20)

def load_next_card():
    global current_card, options, feedback_label, card_label, user_level_label, threshold, option_length_limit, button_result, selected_game_mode
    if feedback_label:
        feedback_label.destroy()
        feedback_label = None
    if user_level_label:
        user_level_label.destroy()
        user_level_label = None
    if button_next:
        button_next.config(state=DISABLED, style="Rounded.TButton")
    if button_result:
        button_result.destroy()
        button_result = None

    card_data = db.fetch_next_card(selected_game_mode) # Fetch a random card from the database
    
    if not card_data and selected_game_mode == "Test":
        feedback_label = Label(canvas_game, text="Test completed! Check your result!", font=fontM, fg="green", bg="#5c0001")
        canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.75, window=feedback_label)
        button_result = ttk.Button(canvas_game, text="Result", command=show_result_page, style="Rounded.TButton")
        canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.65, window=button_result)
        #TODO temp db eval check
        # db.evaluate_result(selected_game_mode)
        return
    elif not card_data and selected_game_mode != "Test":    
        feedback_label = Label(canvas_game, text="No more cards available!", font=fontM, fg="red", bg="#5c0001")
        canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.75, window=feedback_label)
        return
    
    if selected_game_mode != "Test":
        user_level_label = Label(canvas_game, text="", font=fontM, fg='black', bg="#5c0001")
        if threshold < card_data['score']:
            user_level_label.config(text="You are doing great with this word!", fg="green")
        elif threshold-2 <= card_data['score'] <= threshold:
            user_level_label.config(text="You are learning fast!", fg="orange")
        else:
            user_level_label.config(text="This word is still new to you!", fg="red")
        canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.65, window=user_level_label)

    current_card = card_data
    card_label.config(text=current_card['German'])  # Display the German word

    correct_answer = current_card['English']  # The correct answer is the English meaning
    if len(correct_answer) > option_length_limit:
        correct_answer = correct_answer[:option_length_limit] + "..."
        current_card['English'] = correct_answer
    options = [correct_answer]

    # Populate remaining options with random meanings
    while len(options) < 4:
        random_option = db.fetch_random_meaning()  # Fetch a random meaning
        if random_option not in options:
            if len(random_option) > option_length_limit:
                random_option = random_option[:option_length_limit] + "..."
            options.append(random_option)

    max_len = max([len(opt) for opt in options])
    random.shuffle(options)

    # Update option buttons
    for idx, option in enumerate(options):
        option_buttons[idx].config(text=option, command=lambda opt=option: check_answer(opt), width=max_len)

def load_more_info(card):
    # print("card", card)
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
    button_next.config(state=NORMAL, style="CustomNext.TButton")


def check_answer(selected_option):
    global current_card
    global feedback_label, selected_game_mode
    if feedback_label:
        feedback_label.destroy()
    feedback_label = Label(canvas_game, text="", font=fontM, fg='red', bg="#5c0001", wraplength=400)
    if selected_option == current_card['English']:  # Check against the correct answer (English meaning)
        if selected_game_mode != 'Test':
            feedback_label.config(text="Congratulations, Correct Answer", fg="green", bg="#ffffff")
            canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.75, window=feedback_label)

        db.update_score_in_game_queue(current_card['id'], score=1, game_mode=selected_game_mode)  # Increment score by 1 for correct answer
    
    else:
        if selected_game_mode != 'Test':
            feedback_label.config(text="Wrong Answer. Try Again!", fg="red", bg="#ffffff")
            canvas_game.create_window(canvas_game.winfo_width() * 0.50, canvas_game.winfo_height() * 0.75, window=feedback_label)
        
        if selected_game_mode == "Test":
            db.update_score_in_game_queue(current_card['id'], score=0, game_mode=selected_game_mode)  # No decrement in test mode wrong answer
        else:
            db.update_score_in_game_queue(current_card['id'], score=-1, game_mode=selected_game_mode)  # Decrement score by 1 for wrong answer
    
    
    button_next.config(state=NORMAL, style='CustomNext.TButton')
    # Delay before loading the next card
    # root.after(1000, load_next_card)  # 1 second delay before loading the next card

def generate_pdf():
    result = db.evaluate_result(selected_game_mode)
    if not result:
        return

        # Open a file dialog to choose the location and filename for the PDF
    pdf_filename = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not pdf_filename:
        return  # User cancelled the file dialog

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Add a logo at the top
    logo_path = "logo.png"  # Replace with the path to your logo
    c.drawImage(logo_path, x=width/2 - 50, y=height - 100, width=100, height=100)

    # Add the scores and predicted level
    y_position = height - 150
    c.setFont("Helvetica", 12)
    c.drawString(100, y_position, f"Predicted Level: {result['predicted_level']}")
    y_position -= 20
    c.drawString(100, y_position, f"Total Score: {result['total_score']}")
    y_position -= 20

    for level, score in result['scores'].items():
        y_position -= 20
        c.drawString(100, y_position, f"Score for {level}: {score}")

    c.save()
    print(f"PDF generated: {pdf_filename}")


frame_main_top = Frame(page_main)
frame_main_top.pack(expand=True, fill='both', side='top')

frame_main_bottom = Frame(page_main, pady=20)
frame_main_bottom.pack(expand=True, fill='both')

frame_main_middle = Frame(page_main)
frame_main_middle.pack(expand=True, fill='both', side='bottom')

label_main = Label(frame_main_top, text="ASH Cards", font=fontXL, fg='#1ecbe1', bg='white')
label_main.pack(expand=True, anchor='center')

button_start = ttk.Button(frame_main_bottom, text="Start Game",  command=start_game, style="Rounded.TButton")
button_start.pack(expand=True, anchor='center')

button_add_card = ttk.Button(frame_main_bottom, text="Add Card", command=show_add_card, style="Rounded.TButton")
button_add_card.pack(expand=True, anchor='center')

button_remove_card = ttk.Button(frame_main_bottom, text="Remove Card", command=show_remove_card, style="Rounded.TButton")
button_remove_card.pack(expand=True, anchor='center')       

button_exit = ttk.Button(frame_main_bottom, text="Exit", command=root.quit, style="Rounded.TButton")
button_exit.pack(expand=True, anchor='center')

game_mode_label = Label(frame_main_middle, text="Select Game Mode:", font=fontM, fg='black', bg='white')
game_mode_label.pack(expand=True, anchor='center')

game_mode_frame = Frame(frame_main_middle, bg='white')
game_mode_frame.pack(expand=True, anchor='center')

for i, mode in enumerate(game_modes):
    radio_button = Radiobutton(game_mode_frame, text=mode, variable=selected_game_mode_var, value=mode, font=fontM, fg='black', bg='white')
    radio_button.grid(column=i//2, row=i%2, sticky=W)


# Game Page
canvas_game = Canvas(page_game, width=c.getint("ASHConfig", "root_x"), height=c.getint("ASHConfig", "root_y"))
canvas_game.pack(fill="both", expand=True)

# Add the background image to the canvas
canvas_image = canvas_game.create_image(0, 0, anchor=NW, image=bg_image_tk)

# Place widgets over the canvas
# word_label = Label(canvas_game, text="", font=fontL, fg='black', bg="#ffffff")
# canvas_game.create_window(250, 90, window=word_label)

option_buttons = [ttk.Button(canvas_game, text="", style="Custom.TButton") for _ in range(4)]
for idx, btn in enumerate(option_buttons):
    canvas_game.create_window(250, 150 + idx* 40, window=btn)

# canvas_game.create_window(250, 310, window=feedback_label)

button_back = ttk.Button(canvas_game, text="Exit", command=show_main_menu, style="Rounded.TButton")
canvas_game.create_window(250, 350, window=button_back)

if selected_game_mode == "Test":
    button_flip = ttk.Button(canvas_game, text="Flip", command=card_label_toggle, state=DISABLED, style="Rounded.TButton")
else:
    button_flip = ttk.Button(canvas_game, text="Flip", command=card_label_toggle, style="Rounded.TButton")
canvas_game.create_window(250, 390, window=button_flip)

button_next = ttk.Button(canvas_game, text="Next", state=DISABLED, command=load_next_card, style="Rounded.TButton")
canvas_game.create_window(250, 430, window=button_next)

button_more_info = ttk.Button(canvas_game, text="More", command=show_more_info, style="Rounded.TButton")
canvas_game.create_window(250, 470, window=button_more_info)


# card_label = Label(canvas_game, text="Flipped!", font=fontM, fg='black', bg='yellow')
# canvas_game.create_window(250, 430, window=card_label)
card_label_frame = Frame(canvas_game, bg='white', padx=40, pady=40, borderwidth=2, relief="solid")
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

more_info_content_label = Label(frame_more_info, text="", font=fontM, fg='black', wraplength=900)
more_info_content_label.pack(expand=True)
more_info_back_button = ttk.Button(frame_more_info, text="Back", command=lambda: start_game(True), style="Rounded.TButton")
more_info_back_button.pack(expand=True)

# Add Card Page
page_add_card_frame = Frame(page_add_card, bg='white', padx=10, pady=10)
page_add_card_frame.pack(expand=True)

page_add_card_label_german = Label(page_add_card_frame, text="Enter German word:", font=fontL, fg='#1ecbe1', bg='white')
page_add_card_label_german.pack(expand=True)
page_add_card_entry_german = Entry(page_add_card_frame, font=fontM, width=30)
page_add_card_entry_german.pack(expand=True)
page_add_card_label_english = Label(page_add_card_frame, text="Enter English word:", font=fontL, fg='#1ecbe1', bg='white')
page_add_card_label_english.pack(expand=True)
page_add_card_entry_english = Entry(page_add_card_frame, font=fontM, width=30)
page_add_card_entry_english.pack(expand=True)
page_add_card_label_level = Label(page_add_card_frame, text="Enter CEFR Level:", font=fontL, fg='#1ecbe1', bg='white')
page_add_card_label_level.pack(expand=True)
page_add_card_entry_level = Entry(page_add_card_frame, font=fontM, width=30)
page_add_card_entry_level.pack(expand=True)

def submit_add_card():
    new_card_text_german = page_add_card_entry_german.get()
    new_card_text_english = page_add_card_entry_english.get()
    new_card_text_level = page_add_card_entry_level.get()
    print(f"New card german: {new_card_text_german}, english: {new_card_text_english}, level: {new_card_text_level}")
    db.add_word(new_card_text_german, new_card_text_english, new_card_text_level)
    page_add_card_entry_german.delete(0, END)
    page_add_card_entry_english.delete(0, END)
    page_add_card_entry_level.delete(0, END)

page_add_card_submit_button = ttk.Button(page_add_card_frame, text="Submit", command=submit_add_card, style="Rounded.TButton")
page_add_card_submit_button.pack(expand=True)
page_add_card_back_button = ttk.Button(page_add_card_frame, text="Back", command=show_main_menu, style="Rounded.TButton")
page_add_card_back_button.pack(expand=True)


# Remove Card Page

page_remove_card_frame = Frame(page_remove_card, bg='white', padx=10, pady=10)
page_remove_card_frame.pack(expand=True)

page_remove_card_label = Label(page_remove_card_frame, text="Enter card id to remove:", font=fontL, fg='#1ecbe1', bg='white')
page_remove_card_label.pack(expand=True)

page_remove_card_entry = Entry(page_remove_card_frame, font=fontM, width=30)
page_remove_card_entry.pack(expand=True)

def submit_remove_card():
    remove_card_text = page_remove_card_entry.get()
    # Add logic to handle the removal of the card
    print(f"Card to remove: {remove_card_text}")
    db.remove_word(int(remove_card_text))
    page_remove_card_entry.delete(0, END)  # Clear the entry field after submission

page_remove_card_submit_button = ttk.Button(page_remove_card_frame, text="Submit", command=submit_remove_card, style="Rounded.TButton")
page_remove_card_submit_button.pack(expand=True)
page_remove_card_back_button = ttk.Button(page_remove_card_frame, text="Back", command=show_main_menu, style="Rounded.TButton")
page_remove_card_back_button.pack(expand=True)

result_predicted_level = Label(page_result, text="", font=fontL, fg='black')
result_predicted_level.pack(expand=True)

result_total_score = Label(page_result, text="", font=fontM, fg='black')
result_total_score.pack(expand=True)

result_scores = Label(page_result, text="", font=fontM, fg='black')
result_scores.pack(expand=True)

button_generate_pdf = ttk.Button(page_result, text="Generate PDF", command=generate_pdf, style="Rounded.TButton")
button_generate_pdf.pack(expand=True)

button_back_to_game = ttk.Button(page_result, text="Back to Game", command=lambda : start_game(True), style="Rounded.TButton")
button_back_to_game.pack(expand=True)

canvas_game.bind("<Configure>", update_canvas_binding)
page_more_info.bind("<Configure>", update_more_info_binding)
# Initial Setup
show_main_menu()
# update_button_positions(None)
root.mainloop()
