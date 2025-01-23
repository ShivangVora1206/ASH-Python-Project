# beolingus-tk.py  --  Using beolingus.py from tk.


# TODO make it working (try&test)
# TODO make it user friendly
# TODO make it nice
# TODO clean up the mess


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

def set_entry_text (e, text):
    e.delete (0,"end")
    e.insert (0,text)


class Window:
    current_word      = None
    ignore_case       = True
    win               = None

    def __init__ (self):
        print ("--- __init__")

    def update(self, current_word):
        print ("--- update current_word=", current_word)
        if (self.win == None) or ((self.win != None) and (len (self.win.children) == 0)):
            print ("--- update open")
            self.open()
        else:
            print ("--- already open")
        set_entry_text (self.word_entry, current_word)
        self.go_first()

    def open (self):
        print ("--- open")
        self.win = tkinter.Toplevel()
        self.win.title (win_title)
        self.win.geometry (f"{win_width}x{win_height}+{win_xpos}+{win_ypos}")
        self.win.minsize (width=win_width_min, height=win_height_min)

        bf = tkinter.Frame(self.win)
        bf.pack (side="top", fill="x")
        self.close_button    = tkinter.Button (bf, text="Close",  command=self.close,       font=button_font)
        self.go_any_button   = tkinter.Button (bf, text="Any",    command=self.go_any,      font=button_font)
        self.go_fiap_button  = tkinter.Button (bf, text="Fiap",   command=self.go_fiap,     font=button_font)
        self.go_first_button = tkinter.Button (bf, text="First",  command=self.go_first,    font=button_font)
        self.go_apart_button = tkinter.Button (bf, text="Apart",  command=self.go_apart,    font=button_font)
        self.case_button     = tkinter.Button (bf, text="_case_", command=self.toggle_case, font=button_font)


        self.close_button.pack (side="left", anchor="n", fill="x")
        self.case_button.pack (side="left", anchor="n", fill="x")

        self.go_any_button.pack (side="right", anchor="n", fill="x")
        self.go_apart_button.pack (side="right", anchor="n", fill="x")
        self.go_first_button.pack (side="right", anchor="n", fill="x")
        self.go_fiap_button.pack (side="right", anchor="n", fill="x")

        self.word_entry = tkinter.Entry (self.win, width=32, font=entry_font)
        set_entry_text (self.word_entry, word_hist[word_hist_index])
        self.word_entry.bind ("<Return>", self.go_on_return)
        self.word_entry.bind ("<Up>",     self.entry_up)
        self.word_entry.bind ("<Down>",   self.entry_down)
        self.word_entry.pack(side="top", anchor="w")

        self.text_box = tkinter.scrolledtext.ScrolledText (self.win, font=text_box_font)
        self.text_box.insert  ("insert", "Nothing to say...")
        self.text_box.pack(fill="both", expand=True)
        self.is_open = True


    def go_fiap(self):
        word = get_word (self.word_entry)
        res = dict.show_query (word, True, True,   True, True, self.ignore_case)
        text_box_say (self.text_box, res)

    def go_first(self):
        word = get_word (self.word_entry)
        res = dict.show_query (word, True, True,   True, False, self.ignore_case)
        text_box_say (self.text_box, res)

    def go_apart (self):
        word = get_word (self.word_entry)
        res = dict.show_query (word, True, True, False, True, self.ignore_case)
        text_box_say (self.text_box, res)

    def go_any (self):
        word = get_word (self.word_entry)
        res = dict.show_query (word, True, True, False, False, self.ignore_case)
        text_box_say (self.text_box, res)

    def toggle_case (self):
        self.ignore_case = not self.ignore_case
        if self.ignore_case:
            self.case_button["text"] = "_case_"
        else: self.case_button["text"] = "+CASE+"

    def go_on_return (self, event):
        self.go_any()

    def entry_up (self, event):
        print ("entry_up")
        print (w_prev())
        set_entry_text (self.word_entry, word_hist[word_hist_index])

    def entry_down (self, event):
        print ("entry_down")
        print (w_next())
        set_entry_text (self.word_entry, word_hist[word_hist_index])

    def close (self):
        if (self.win != None) and (self.win.state() == 'normal'):
            self.win.destroy()
            print ("--- close")
        else: print ("--- no win open")


# :file: END

