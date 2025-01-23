# beolingus-tk.py  --  Try to use beolingus.py from tk.


# TODO
# * a lot
# parse config (ini)

import tkinter
import tkinter.scrolledtext

from beolingus import Beolingus
import config

cfg = config.Config ("config.ini")

win_title      = cfg.get    ("beodict", "win_title", "<TITLE>")

win_width      = cfg.getint ("beodict", "win_width",      600)
win_height     = cfg.getint ("beodict", "win_height",     300)
win_xpos       = cfg.getint ("beodict", "win_xpos",       200)
win_ypos       = cfg.getint ("beodict", "win_ypos",       200)
win_width_min  = cfg.getint ("beodict", "win_width_min",  600)
win_height_min = cfg.getint ("beodict", "win_height_min", 150)

entry_font   = ("Courier",         18, "normal")
button_font  = ("Arial",           18, "bold")
message_font = ("Times New Roman", 16, "normal")
text_box_font= ("Times New Roman", 16, "normal")

dict            = Beolingus()
word_hist       = ["Anaconda", "Desire", "Netzpython"]
word_hist_index = 0
ignore_case     = True


def w_next():
    global word_hist_index
    if word_hist_index < len(word_hist) - 1:
        word_hist_index += 1
    else: word_hist_index = 0
    return word_hist_index

def w_prev():
    global word_hist_index
    if word_hist_index > 0:
        word_hist_index -= 1
    else: word_hist_index = len(word_hist) - 1
    return word_hist_index

def w_insert (word):
    word_hist.append (word)

def get_word (entry):
    word = entry.get()
    w_insert (word)
    return word


def text_box_say (widget, mess):
    widget.delete ("1.0","end")
    widget.insert ("insert", mess)


def go_fiap():
    word = get_word (word_entry)
    res = dict.show_query (word, True, True,   True, True, ignore_case)
    text_box_say (text_box, res)

def go_first():
    word = get_word (word_entry)
    res = dict.show_query (word, True, True,   True, False, ignore_case)
    text_box_say (text_box, res)

def go_apart():
    word = get_word (word_entry)
    res = dict.show_query (word, True, True, False, True, ignore_case)
    text_box_say (text_box, res)

def go_any():
    word = get_word (word_entry)
    res = dict.show_query (word, True, True, False, False, ignore_case)
    text_box_say (text_box, res)

def toggle_case():
    global ignore_case
    ignore_case = not ignore_case
    if ignore_case:
        case_button["text"] = "_case_"
    else: case_button["text"] = "+CASE+"

def go_on_return (event):
    go_any()

def set_entry_text (e, text):
    e.delete (0,"end")
    e.insert (0,text)

def entry_up (event):
    print ("entry_up")
    print (w_prev())
    set_entry_text (word_entry, word_hist[word_hist_index])

def entry_down (event):
    print ("entry_down")
    print (w_next())
    set_entry_text (word_entry, word_hist[word_hist_index])

def halt():
    print ("------------  quit")
    quit()

# win = tkinter.Tk()
# win.title (win_title)
# win.geometry (f"{win_width}x{win_height}+{win_xpos}+{win_ypos}")
# win.minsize (width=win_width_min, height=win_height_min)

# bf = tkinter.Frame(win)
# bf.pack (side="top", fill="x")
# quit_button          = tkinter.Button (bf, text="Quit",   command=halt,        font=button_font)
# go_any_button        = tkinter.Button (bf, text="Any",    command=go_any,      font=button_font)
# go_fiap_button       = tkinter.Button (bf, text="Fiap",   command=go_fiap,     font=button_font)
# go_first_button      = tkinter.Button (bf, text="First",  command=go_first,    font=button_font)
# go_apart_button      = tkinter.Button (bf, text="Apart",  command=go_apart,    font=button_font)
# case_button          = tkinter.Button (bf, text="_case_", command=toggle_case, font=button_font)


# quit_button.pack (side="left", anchor="n", fill="x")
# case_button.pack (side="left", anchor="n", fill="x")

# go_any_button.pack (side="right", anchor="n", fill="x")
# go_apart_button.pack (side="right", anchor="n", fill="x")
# go_first_button.pack (side="right", anchor="n", fill="x")
# go_fiap_button.pack (side="right", anchor="n", fill="x")

# word_entry = tkinter.Entry (width=32, font=entry_font)
# set_entry_text (word_entry, word_hist[word_hist_index])
# word_entry.bind ("<Return>", go_on_return)
# word_entry.bind ("<Up>",     entry_up)
# word_entry.bind ("<Down>",   entry_down)
# word_entry.pack(side="top", anchor="w")

# text_box = tkinter.scrolledtext.ScrolledText (font=text_box_font)
# text_box.insert  ("insert", "Nothing to say...")
# text_box.pack(fill="both", expand=True)

class UpdateWindow:
    def __init__ (self, root, frame_main_bottom, button_style, current_word):
        print ("--- __init__  current_word=", current_word)
        button_update = tkinter.Button (frame_main_bottom, text="beoli", command=self.update_window, font=button_font)
        button_update.pack()


    def update_window (self):
        print ("--- update_window")


# def main():
#     print ("============  beolingus-tk")
#     win.mainloop()
#     print ("============  done")

# if __name__ == "__main__":
#         main()

# file END

