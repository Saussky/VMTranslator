import os

class VM_Parser:
    def __init__(self, file):
        self.file = file
        
        self.current_command = None
        self.command_type = None
        self.has_more_commands = None
        
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None
        
        self.lines = self.read_file(self.file)
        self.check_for_command()

    def read_file(self, file):
        with open(file, encoding="utf-8") as file:
            lines = file.readlines()

        return self.clean_lines(lines)

    def clean_lines(self, lines):
        lines = [
            line.strip() for line in lines if not line.startswith("//") and line != "\n"
        ]
        return lines

    def check_for_command(self):
        if len(self.lines) > 0:
            self.has_more_commands = True
        else:
            self.command_type = None
            self.has_more_commands = False
            
    def advance(self):
        self.check_for_command()

        if self.has_more_commands:
            self.current_command = self.lines.pop(0)
            self.get_type(self.current_command)
            self.get_args()
        else:
            self.current_command = None

    def get_type(self, command):
        command_arr = command.split(" ")
        for word in command_arr:
            if word == "push":
                self.command_type = "C_PUSH"
                return
            elif word == "pop":
                self.command_type = "C_POP"
                return
            elif word == "add" or word == "sub" or word == "eq" or word == "lt" or word == "gt" or word == "neg" or word == "and" or word == "or" or word == "not":
                self.command_type = "C_ARITHMETIC"
                return
            elif word == "label" or word == "goto" or word == "if-goto":
                self.command_type = "C_FLOW"
                return
            elif word == "function" or word == "call":
                self.command_type = "C_FUNCTION"
                return
            elif word == "return":
                self.command_type = "C_RETURN"
                
    def get_args(self):
        if self.command_type == "C_RETURN":
            return
        elif self.command_type == "C_ARITHMETIC":
            self.arg1 = self.current_command
            self.arg2 = None
            return
        elif self.command_type == "C_FLOW":
            command_arr = self.current_command.split(" ")
            self.arg1 = command_arr[0]
            self.arg2 = command_arr[1]
            return
        elif self.command_type == "C_FUNCTION":
            command_arr = self.current_command.split(" ")
            self.arg1 = command_arr[0]
            self.arg2 = command_arr[1]
            self.arg3 = command_arr[2]
            return
        
        command_arr = self.current_command.split(" ")
        self.arg1 = command_arr[1]
        self.arg2 = command_arr[2]

