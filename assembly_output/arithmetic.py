class ArithmeticWriter:
    def __init__(self, file_output):
        self.file_output = file_output
        self.iter = 0

    def write_arithmetic(self, command):
        asm_command = ""
        if "add" in command:
            asm_command = self.write_add_or_sub('+')
        elif "sub" in command:
            asm_command = self.write_add_or_sub('-')
        elif "neg" in command:
            asm_command = self.write_neg()
        elif command in ["eq", "gt", "lt"]:
            asm_command = self.write_comparison(command)
        elif command in ["and", "or"]:
            asm_command = self.write_and_or(command)
        elif "not" in command:
            asm_command = self.write_not()
            
        self.write_line(asm_command)

    def write_add_or_sub(self, symbol):
        comment = "add" if symbol == '+' else "sub"
        return f"""
        // {comment}
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        M=M{symbol}D
        @SP
        M=M+1
        """

    def write_not(self):
        return f"""
        // not
        @SP
        A=M-1
        M=!M
        """

    def write_and_or(self, command):
        symbol = '&' if command == "and" else '|'
        return f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        M=D{symbol}M
        @SP
        M=M+1
        """

    def write_neg(self):
        return f"""
        // neg
        @SP
        A=M-1
        M=-M
        """

    def write_comparison(self, command):
        jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
        self.iter += 1
        return f"""
        // {command.upper()}
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        D=M-D
        @{command.upper()}_TRUE_{self.iter}
        D;{jump}
        @SP
        A=M
        M=0
        @END_{self.iter}
        0;JMP
        ({command.upper()}_TRUE_{self.iter})
        @SP
        A=M
        M=-1
        (END_{self.iter})
        @SP
        M=M+1
        """

    def write_line(self, code):
        if not code:
            return
        with open(self.file_output, mode="a") as file:
            file.write(code)
