# beolingus.py  --  Get additional info from Beolingus dictionary.


###############################################################################
# For the wordlist used by this python file the following copyrights hold:
#
# Copyright (c) :: Frank Richter <frank.richter.tu-chemnitz.de>,
# 1995 - 2024
# License :: GPL Version 2 or later; GNU General Public License
# URL :: https://dict.tu-chemnitz.de/
#
###############################################################################


# in order to try this out from Linux command line see 'def main()' and say:
#     python beolingus.py


# in order to try this out in Python repl say:
#     open ("beolingus.py")
#     from beolingus import Beolingus
#     dict = Beolingus()
#     dict.help()
#     dict.info ("Desire", ignorecase=False)
#     dict.info ("Python")


# TODO
# * DOWNLOAD NOT WORKING: Get the download to work or find an other solution
#       download with firefox ok, download with wget did not return anything
# * make an interface for tkinter
# * play with it and improve
# * add a touch of color and style (tkinter ?)


# re regexpr in Python
# use raw strings


import os
import re

import urllib
# import requests
# import requests_ftp                             # pip install requests_ftp
# import urllib.request


class Beolingus:
    dict = []
    file = "de-en.txt"
    url  = "https://ftp.tu-chemnitz.de/pub/Local/urz/ding/de-en-devel/de-en.txt"
    is_loaded = False

    def __init__(self):
        if self.exists ():
            print ("--- Beolingus dictionary file found:", self.file)
        else: print ("--- No Beolingus dictionary file found.")

    def exists (self):
        return os.path.exists (self.file)

    def download (self):
        if self.exists ():
            print ("There is already an dict file: ", self.file)
            return
        print ()
        print ("downloading dictionary: ", self.url)
        print ("to file:                ", self.file)
        filename = "<filename>"
        headers  = "<headers>"
        filename,headers = urllib.request.urlretrieve (self.url, self.file)
        print ("download returned with ")
        print ("    ",filename)
        print ("    ",headers)

    def do_load(self):
        self.dict = []
        with open (self.file, "r", encoding='utf-8') as f:
           for l in f:
               if not l.startswith ("# "):      # ignore dictionary files comments
                   pos = l.find (" :: ")        # ' :: ' separates de and en
                   de  = l[0:pos]
                   en  = l[pos+4:-1]            # load without trailing newline
                   self.dict.append ([de,en])
        self.is_loaded = True


    def load (self):
        if not self.exists():
            self.download()
        if (not self.is_loaded) and self.exists():
            self.do_load()
        return self.is_loaded


    def check (self):
        if self.is_loaded:
            return True
        else: return self.load()


    def dump (self):
        n = 3
        print ("=======  Beolingus dump")
        if not self.check():
            print ("#######  self.check failed")
        for i in range (0,n):
            print (self.dict[i][0])
            print (self.dict[i][1])
            print ()
        print ("-----------")
        for i in range (-n,0):              # range: -n ... -3 -2 -1
            print (self.dict[i][0])
            print (self.dict[i][1])
            print ()


    def help (self):
        print ("=======  Beolingus help:")
        print ("    dict.help()")
        print ("    dict.info (word, de=True, en=True, first=False, apart=False, ignorecase=True)")
        print ()


    def show_flags (self, flags):
        flags_text = ["de", "en", "first", "apart", "ignorecase"]
        if len(flags) != len(flags_text):
           print ("#######  show_flags: flags don't match")
           quit
        res = ""
        for i in range (0, len(flags)):
           t = flags_text[i]
           if flags[i] == True:
              t = "+" + t.upper()
           else: t = "-" + t
           res += t + " "
        return res

    def is_match (self, pattern, text):
        return None != re.search (pattern, text)

    def show_entry (self, entry):
        res = ""
        res += entry[0] +"\n"
        res += "==> "+ entry[1] + "\n\n"
        return res

    def show_query (self, word, de, en, first, apart, ignorecase):
        if not self.check():
            return "<dict-not-available>"
        pattern = word
        flags   = 0
        if first: pattern = "^" + pattern
        if apart:
            if first: pattern = pattern + " "
            else:     pattern = " "+ pattern +" "
        if ignorecase: flags += re.IGNORECASE
        r = re.compile (pattern, flags)
        res = ""
        print ("searching...")
        for deen in self.dict:
            if    (de and self.is_match (r, deen[0]))   \
               or (en and self.is_match (r, deen[1])):
                res += self.show_entry (deen)
        print ("...!")
        return res



    def info (self, word, de=True, en=True, first=False, apart=False, ignorecase=True):
        flags_mess = self.show_flags ([de,en,first,apart,ignorecase])
        if self.check():
            print ("========================================================")
            print ("=======  Beolingus:   ",word,"  ",flags_mess)
            print ()
            print (self.show_query (word, de,en,first,apart,ignorecase))
        else: print ("Sorry, the Beolingus dictionary is currently not available.")
        print()
        print()


def main():
        print ("============  beolingus")
        # dict = Beolingus()
        # dict.dump()
        # print()
        # dict.info ("Sehnsucht", de = True, ignorecase=False)
        # dict.info ("Sehnsucht", de = True, apart=True, ignorecase=False)
        # dict.info ("Sehnsucht", de = True, first=True, ignorecase=False)
        # dict.info ("Desire", de=False, ignorecase=False)
        # dict.info ("Desire", apart=True)
        # dict.info ("Desire", first=True)
        # dict.info ("Desire", ignorecase=False)
        # dict.info ("Desire", first=True, apart=True)
        # print()
        print ("============  done")


if __name__ == "__main__":
        main()


# file END.
