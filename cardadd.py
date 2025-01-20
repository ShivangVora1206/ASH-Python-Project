# :file: cardadd.py  --  Add a card to database.


"""Add a card to database.

This module provides functionality to add a card to our database.
A card holds data for a words

 * english meaning
 * german meaning
 * optionaly a description in a short sentence.
"""


# TODO: ??? Check user input: How? Only ASCII? No!
# TODO: ??? Enter -> next entry or add


from tkinter import *

import config


cfg = config.Config ("config.ini")
sec = "default"

headline_font = (cfg.get (sec, "headline_font","Courier"), cfg.get (sec, "headline_font_size", 14), "normal")
text_font     = (cfg.get (sec, "text_font",    "Courier"), cfg.get (sec, "text_font_size",     14), "normal")
entry_font    = (cfg.get (sec, "entry_font",   "Courier"), cfg.get (sec, "entry_font_size",    14), "normal")
button_font   = (cfg.get (sec, "button_font",  "Courier"), cfg.get (sec, "button_font_size",   14), "normal")

headline_bg = cfg.get (sec, "headline_bg", "gray")
button_bg   = cfg.get (sec, "button_bg",   "gray")
label_bg    = cfg.get (sec, "text_bg",     "gray")
page_bg     = cfg.get (sec, "page_bg",     "gray")
entry_bg    = cfg.get (sec, "entry_bg",    "gray")


# This function might be moved into class database.Database
def check (db, de, en):
        """Check if word is allready in dataset.

        Return word ID if found.
        Return None if not found.
        """
        id = None
        for w in db.data:
            if w["German"] == de:
                id = w["id"]
                break
            if w["English"] == en:
                id = w["id"]
                break
        return id

def check_word (word):
        """Check user input and remove whitespace."""
        res = word.strip()
        if (res == ""):
            res = None
        return res

def set_entry_text (e, text):
    e.delete (0,"end")
    e.insert (0,text)

def label_say (label, mess):
        label.config (text=mess)


class Page:
    """Provide a page to add a card to database."""
    db           = None
    page_addcard = None
    page_main    = None
    root         = None

    def __init__ (self, frame_main_bottom, page_main, button_style, root, db):
        """Add a button to main page that invokes adding a card."""
        self.db        = db
        self.page_main = page_main
        self.root      = root
        button_cardadd = Button (frame_main_bottom,
                                 text="Add card",
                                 command=self.show_page_cmd,
                                 font=button_style[0])
        button_cardadd.pack()

    def show_page_cmd (self):
        print ("--- show_page_cmd")
        f = Frame (self.root)
        f.configure (background = page_bg, padx=50, pady=50)
        mess_headline   = Label (f, text="Add a Card",  font=headline_font, bg=headline_bg, padx=20, pady=7)
        mess_de         = Label (f, text="German",      font=text_font,  bg=label_bg, padx=10, pady=5)
        mess_en         = Label (f, text="English",     font=text_font,  bg=label_bg, padx=10, pady=5)
        mess_desc       = Label (f, text="Description", font=text_font,  bg=label_bg, padx=10, pady=5)
        self.mess_err   = Label (f, text="<>",          font=text_font,  bg=label_bg, padx=10, pady=7)
        self.entry_de   = Entry (f, width=32,           font=entry_font, bg=entry_bg)
        self.entry_en   = Entry (f, width=32,           font=entry_font, bg=entry_bg)
        self.entry_desc = Entry (f, width=72,           font=entry_font, bg=entry_bg)
        button_add      = Button (f, text="Add",  command=self.add_word_cmd, font=button_font, bg=button_bg)
        button_back     = Button (f, text="Back", command=self.back_cmd,     font=button_font, bg=button_bg)

        # anchor defaults to nw corner of widget
        x = 50
        y = 70
        mess_headline.place     (x=x,     y=0.5*y, anchor="sw")
        mess_de.place           (x=x,     y=1*y, anchor="sw")
        self.entry_de.place     (x=x,     y=1*y, anchor="nw")
        mess_en.place           (x=x,     y=2*y, anchor="sw")
        self.entry_en.place     (x=x,     y=2*y, anchor="nw")
        mess_desc.place         (x=x,     y=3*y, anchor="sw")
        self.entry_desc.place   (x=x,     y=3*y, anchor="nw")
        button_add.place        (x=x,     y=4*y)
        button_back.place       (x=x+100, y=4*y)
        self.mess_err.place     (x=x+300, y=4*y)

        self.page_main.pack_forget()
        f.pack (expand=True, fill="both")

        self.entry_de.bind   ("<Return>", self.add_word_event)
        self.entry_en.bind   ("<Return>", self.add_word_event)
        self.entry_desc.bind ("<Return>", self.add_word_event)
        self.entry_de.bind   ("<Escape>", self.back_event)
        self.entry_en.bind   ("<Escape>", self.back_event)
        self.entry_desc.bind ("<Escape>", self.back_event)
        button_add.bind      ("<Escape>", self.back_event)
        button_back.bind     ("<Escape>", self.back_event)

        self.entry_de.focus()
        self.page_addcard = f


    def add_word_cmd(self):
        de   = self.entry_de.get ()
        en   = self.entry_en.get ()
        desc = self.entry_desc.get ()
        print ("--- add card: <",de,">  <",en,">   <",desc,">")
        de = check_word (de)
        en = check_word (en)
        id = check (self.db, de, en)
        if de == None:
            label_say (self.mess_err, "Strange input for DE.")
            self.entry_de.focus()
        if en == None:
            label_say (self.mess_err, "Strange input for EN.")
            self.entry_en.focus()
        if id != None: label_say (self.mess_err, "Word is allready in dataset. ID = "+ str(id))
        if (id == None) and (de != None) and (en != None):
            self.db.add_word (de, en, desc)
            self.db.save()
            label_say (self.mess_err, "Added   German: " + de+ "   English: "+ en+"   Description: " + desc)
            set_entry_text (self.entry_de, "")
            set_entry_text (self.entry_en, "")
            set_entry_text (self.entry_desc, "")
            self.entry_de.focus()
        else: print ("--- add_word_cmd: strange input or word already in dataset")

    def add_word_event (self, event):
        self.add_word_cmd ()

    def back_cmd(self):
        print ("--- cmd: back")
        self.page_addcard.pack_forget()
        self.page_main.pack(expand=True)

    def back_event (self, event):
        print ("--- back_event")
        self.back_cmd()


# -----------------------------------------------------------------------------
# test add card via terminal
data_file = "temp_dataset.json"
from database import Database

def add_word (db):
        """Add a word to database."""
        de   = input ("german word:  ")
        en   = input ("english word: ")
        desc = input ("description:  ")
        id = check (db, de, en)
        if id == None:
            db.add_word (de, en, desc)
        else: print ("Word is allready in dataset. ID =", id)
        db.save()

def main():
        db = Database (data_file)
        add_word (db)


if __name__ == "__main__":
        main()


# :file: END
