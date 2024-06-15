import pickle

class Commands:
    def __init__(self, file = 'docs/command_descript.pkl'):
        self.file = file
        self.commands = {}
        self.__load_commands()

    def __load_commands(self):
        try:
            with open(self.file, 'rb') as f:
                self.commands = pickle.load(f)
        except FileNotFoundError:
            print('command_descript file not found')
            self.commands = {}

    def save_commands(self, commands: dict):
        with open(self.file, 'wb') as f:
            pickle.dump(commands, f)
    
    def get_command_dict(self) -> dict:
        if not self.commands:
            self.__load_commands()
        return self.commands