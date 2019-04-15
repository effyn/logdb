import os
import json
import hashlib
from traceback import format_exc

motd = """                                                      _
                                                     (_)
   __ _ _ __ ___    _ __   ___    _ __ ___ _ __   __ _ _ _ __
  / _` | '__/ __|  | '_ \ / __|  | '__/ _ \ '_ \ / _` | | '__|
 | (_| | | | (__   | |_) | (__   | | |  __/ |_) | (_| | | |
  \__, |_|  \___|  | .__/ \___|  |_|  \___| .__/ \__,_|_|_|
   __/ |           | |                    | |
  |___/            |_|                    |_|"""
os_clear = "cls" if os.name == "nt" else "clear"

prompt = lambda s: input(f"\n {s} > ")
error = lambda s: print(f"\n ! {s}")
report = lambda s: print(f"\n - {s}")

class DB:
    @staticmethod
    def validate_int(prompt_string: str):
        entered_string = prompt(prompt_string)
        while not entered_string.isdigit():
            error("not a number")
            entered_string = prompt(prompt_string)
        return int(entered_string)

    @staticmethod
    def hash_password(password: str):
        return hashlib.sha512(password.encode("utf-8")).hexdigest()

    @staticmethod
    def validate_password(prompt_string: str):
        password = prompt(prompt_string)
        password2 = prompt(f"{prompt_string} again")
        while password != password2:
            error("passwords do not match")
            password = prompt(prompt_string)
            password2 = prompt(f"{prompt_string} again")
        return DB.hash_password(password)

    def __init__(self, path="./db.json"):
        self.path = path
        try:
            with open(path) as f:
                self._dict = json.load(f)
        except FileNotFoundError:
            with open(path, "w") as f:
                f.write("{}")
            self._dict = {}

    def __contains__(self, key):
        return key in self._dict

    def __iter__(self):
        return iter(self._dict.items())

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return repr(self._dict)

    def set(self, key, value):
        self._dict[key] = value

    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        return None

    def save(self):
        with open(self.path, "w") as f: 
            json.dump(self._dict, f)

    def admin_password(self):
        password = prompt("enter the admin password")
        return DB.hash_password(password) == self.get("admin")

    # START OF COMMANDS SECTION

    def config_command(self, args):
        if "admin" not in self:
            self.set("admin", DB.validate_password("enter an admin password"))
        elif self.admin_password():
            self.set("next-id", DB.validate_int("next receipt number?"))
            self.save()
        else:
            error("invalid admin password")

    def motd_command(self, args):
        print(motd)

    def clear_command(self, args):
        os.system(os_clear)

    def eval_command(self, args):
        try:
            report(eval(" ".join(args)))
        except:
            error(format_exc())

    # END OF COMMANDS SECTION

    _commands = {
        "config": config_command,
        "motd": motd_command,
        "clear": clear_command,
        "eval": eval_command
    }

    def command(self, command: str):
        args = command.split()
        commands = self._commands
        if args:
            if args[0] in commands:
                commands[args[0]](self, args[1:])
            else: error("no such command")

db = DB()
db.motd_command(None)

try:
    while True:
        db.command(prompt("ready"))
except KeyboardInterrupt:
    db.save()
