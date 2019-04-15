import os
import json
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
    def validate_int(prompt_string):
        entered_string = prompt(prompt_string)
        while entered_string
    
    def __init__(self, path="./db.json"):
        try:
            self._file = open(path, "r+")
            self._dict = json.load(self._file)
        except FileNotFoundError:
            self._file = open(path, "w+")
            self._file.write("{}")
            self._dict = {}

    def __iter__(self):
        return iter(self._dict.items())

    def set(self, key, value):
        self._dict[key] = value

    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        return None

    def save(self):
        json.dump(self._dict, self._file)

    def close(self):
        self._file.close()

    def shutdown(self):
        self.save()
        self.close()

    # START OF COMMANDS SECTION

''''''
    def config_command(self, args):
        status = "config"
        self.set("next-id", validate_int("next receipt number?"))

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

print(motd)
db = DB()

try:
    while True:
        db.command(prompt("ready"))
except KeyboardInterrupt:
    db.shutdown()
