# main.py  --  Using ini files.

import os
import configparser


class Config:
    """Read configuration file of ASHCards project.

    This class uses Python's 'configparser' module.


    File format is 'ini'.
    """
    file   = None
    """Configuration file."""
    parser = None
    """Configuration Parser."""

    def __init__(self, file):
        """ Hallo?<???> Where am i?"""
        self.file = file
        if os.path.exists (self.file):
            self.parser = configparser.ConfigParser()
            try:
                with open (self.file) as fd:
                    self.parser.read_file (fd)
                print ("--- config loaded: ", self.file, f" with sections: {self.parser.sections()}")
            except:
                 self.parser = None
                 print ("--- config load failed: ", self.file)
        else: print ("--- config file not found:", self.file)

    def get (self, section, key, default):
        """Return key form section. A default value is mandatory."""
        res = default
        if self.parser:
            if self.parser.has_section (section):
                try: res = self.parser.get (section, key)
                except: print ("--- config: key not found: ", key)
            else: print ("--- config: no such section: ", section)
        else: print ("--- config: parser == None")
        return res

    def getint (self, section, key, default):
        """Return key form section. A default value is mandatory.

        Return key as integer, if possible.

        Return key as string, if is is not an integer.
        """
        res = default
        v = self.get (section, key, default)
        if v:
            try: res = int(v)
            except: print ("--- config: not an integer")
        return res

    def dump (self):
        """For testing of this module."""
        print ("------------  Config.dump")
        print (self.file)
        if self.parser:
            for s in self.parser.sections():
                print (s)
                print (self.parser.items (s))
        else: print ("parser is None")
        print ("------------")
        print ()


# -----------------------------------------------------------------------------
# def main():
#         print ("============  main")
#         cfg = Config()
#         cfg.dump()
#         print ("--- test: ", cfg.get ("names", "name"))
#         print ("--- test: ", cfg.get ("names", "otto"))
#         print ("--- test: ", cfg.get ("names", "max"))
#         print ("--- test: ", cfg.getint ("window", "win_height", 1000))
#         print ("--- test: ", cfg.getint ("window", "win_width"))
#         print ()
#         print ("--- test: ", cfg.getint ("window", "win_size", 1200))
#         print ("--- test: ", cfg.getint ("window", "win_max"))
#         print ()
#         print ("--- test: ", cfg.get ("names", "maxx"))
#         print ("--- test: ", cfg.get ("names", "maxx", "names-maxx"))
#         print ("--- test: ", cfg.getint ("windoww", "win_width", 1000))
#         print ("--- test: ", cfg.getint ("window", "win_widthg", 1000))
#         print ()
#         print ("============  done")

# if __name__ == "__main__":
#     main()


# -----------------------------------------------------------------------------
# :file: END
