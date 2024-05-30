class FlowWriter:
    def __init__(self, file_output):
        self.file_output = file_output

    def write_flow(self, command, type, name):
        asm_command = ""
        if "label" in type:
            asm_command = self.write_label(command, name)
        elif "goto" in type:
            asm_command = self.write_goto(command, name)
        elif "if-goto" in type:
            asm_command = self.write_if_goto(command, name)
        self.write_line(asm_command)

    def write_label(self, command, name):
        return f"""
        // {command}
        ({name})
        """

    def write_goto(self, command, name):
        return f"""
        // {command}
        @{name}
        0;JMP
        """

    def write_if_goto(self, command, name):
        return f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @{name}
        D;JNE
        """

    def write_line(self, code):
        if not code:
            return
        with open(self.file_output, mode="a") as file:
            file.write(code)
