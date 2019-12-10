import time
import imaplib
import email
import os
import pkgutil

##########################################

# Add your gmail username and password here

username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

##########################################

class ControlException(Exception):
    pass


class Control():
    def __init__(self, username, password, out_q):
        # print("------------------------------------------------------")
        # print("-                    SIRI CONTROL                    -")
        # print("-           Created by Sanjeet Chatterjee            -")
        # print("-      Website: https://medium.com/@thesanjeetc      -")
        # print("------------------------------------------------------")

        try:
            self.last_checked = -1
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(username, password)
            self.mail.list()
            self.mail.select("Notes")
            self.out_q = out_q

            # Gets last Note id to stop last command from executing
            result, uidlist = self.mail.search(None, "ALL")
            try:
                self.last_checked = uidlist[0].split()[-1]
            except IndexError:
                pass

            self.load()
            self.handle()
        except imaplib.IMAP4.error:
            print("Your username and password is incorrect")
            print("Or IMAP is not enabled.")
    
    # MFM 12/7/19
    def interpret_command(self,command,s,index):
        """
        Author: Matthew McEneaney
        Convert the command word specifying a parameter value to a float
        and send it to a queue.
        """
        result = ""
        words = ["point","zero","one","two","three","four","five","six","seven",
            "eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen",
            "sixteen","seventeen","eighteen","nineteen","twenty","thirty","forty","fifty"]
        replacements = [".","0","1","2","3","4","5","6","7","8","9","10",
            "11","12","13","14","15","16","17","18","19","20","30","40","50"]
        command = command.replace(" ","")
        if command.find(s) != -1:
            print("FOUND COMMAND:",command)
            interpreted_command = command[index + len(s):]
            print(interpreted_command)
            for n in range(len(words)):
                interpreted_command = interpreted_command.replace(words[n],replacements[n])
                print(interpreted_command)
            for c in interpreted_command:
                if c.isdecimal() or c == ".":
                    result += c
                else:
                    break
            if result != "":
                new_s = float(result)
                self.out_q.put([s,new_s])

    def check_command(self,command):
        """
        Author: Matthew McEneaney
        Convert the command words specifying length and frequency values to floats
        and send them to a queue.
        """
        l_len = len("length")
        f_len = len("frequency")
        l_index = command.find("length")
        f_index = command.find("frequency")
        self.interpret_command(command,"length",l_index)
        self.interpret_command(command,"frequency",f_index)

    def load(self):
        """Try to load all modules found in the modules folder"""
        print("\n")
        print("Loading modules...")
        self.modules = []
        path = os.path.join(os.path.dirname(__file__), "modules")
        directory = pkgutil.iter_modules(path=[path])
        for finder, name, ispkg in directory:
            try:
                loader = finder.find_module(name)
                module = loader.load_module(name)
                if hasattr(module, "commandWords") \
                        and hasattr(module, "moduleName") \
                        and hasattr(module, "execute"):
                    self.modules.append(module)
                    print("The module '{0}' has been loaded, "
                          "successfully.".format(name))
                else:
                    print("[ERROR] The module '{0}' is not in the "
                          "correct format.".format(name))
            except:
                print("[ERROR] The module '" + name + "' has some errors.")
        print("\n")

    def fetch_command(self):
        """Retrieve the last Note created if new id found"""
        self.mail.list()
        self.mail.select("Notes")

        result, uidlist = self.mail.search(None, "ALL")
        try:
            latest_email_id = uidlist[0].split()[-1]
        except IndexError:
            return

        if latest_email_id == self.last_checked:
            return

        self.last_checked = latest_email_id
        result, data = self.mail.fetch(latest_email_id, "(RFC822)")
        voice_command = email.message_from_string(data[0][1].decode('utf-8'))
        return str(voice_command.get_payload()).lower().strip()

    def handle(self):
        """Handle new commands

        Poll continuously every second and check for new commands.
        """
        print("Fetching commands...")
        print("\n")

        while True:
            try:
                command = self.fetch_command()
                if not command:
                    raise ControlException("No command found.")

                print("The word(s) '" + command + "' have been said")
                # MFM 12/7/19
                self.check_command(command)

                for module in self.modules:
                    foundWords = []
                    for word in module.commandWords:
                        if str(word) in command:
                            foundWords.append(str(word))
                    if len(foundWords) == len(module.commandWords):
                        try:
                            module.execute(command)
                            print("The module {0} has been executed "
                                  "successfully.".format(module.moduleName))
                        except:
                            print("[ERROR] There has been an error "
                                  "when running the {0} module".format(
                                      module.moduleName))
                    else:
                        print("\n")
            except (TypeError, ControlException):
                pass
            except Exception as exc:
                print("Received an exception while running: {exc}".format(
                    **locals()))
                print("Restarting...")
            time.sleep(1)

def siri_control(out_q):
    Control(username, password, out_q)
