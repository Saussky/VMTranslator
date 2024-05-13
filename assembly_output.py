class Code_Writer:
    def __init__(self, file_output):
        self.clear_file(file_output)
        self.file_output = file_output
        self.iter = 0

    def clear_file(self, file_output):
        with open(file_output, mode="w") as file:
            file.write("")
            
    def write_push_pop(self, command, type, segment, index):
        if type == "C_PUSH":
            if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                command = self.write_normal_push(command, segment, index)
            elif segment == "constant":
                command = self.write_const_push(command, index)
            elif segment == "temp":
                command = self.write_temp_push(command, index)
            elif segment == "pointer":
                command = self.write_pointer_push(command, index)
            elif segment == "static":
                command = self.write_static_push(command, index)

        elif type == "C_POP":
            if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                command = self.write_normal_pop(command, segment, index)
            elif segment == "temp":
                command = self.write_temp_pop(command, index)
            elif segment == "pointer":
                command = self.write_pointer_pop(command, index)
            elif segment == "static":
                command = self.write_static_pop(command, index)

        self.write_line(command)
        return


    def write_arithmetic(self, command):
        if command == "add":
            command = self.write_add_or_sub('+')
        elif command == "sub":
            command = self.write_add_or_sub('-')
        elif command == "neg":
            command = self.write_neg()
        elif command == "eq" or command == "gt" or command == "lt":
            command = self.write_comparison(command)

        elif command == "and" or command == "or":
            command = self.write_and_or(command)
        elif command == "not":
            command = self.write_not()

        self.write_line(command)
        return

    def write_not(self):
        asm_command = f"""
        // not
        @SP
        A=M-1
        M=!M
        """
        return asm_command

    def write_and_or(self, command):
        symbol = ''
        if command == "and":
            symbol = "&"
        elif command == "or":
            symbol = "|"

        asm_command = f"""
        //{command}
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
        return asm_command

    def write_neg(self):
        asm_command = f"""
        // neg
        @SP
        A=M-1
        M=-M
        """
        return asm_command

    def write_comparison(self, command):
        jump = ''
        if command == "eq":
            jump = "JEQ"
        elif command == "gt":
            jump = "JGT"
        elif command == "lt":
            jump = "JLT"

        command = command.upper()

        self.iter += 1

        asm_command = f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @SP
        M=M-1
        A=M
        D=M-D
        @{command}_TRUE_{self.iter}
        D;{jump}
        @SP
        A=M
        M=0
        @END_{self.iter}
        0;JMP
        ({command}_TRUE_{self.iter})
        @SP
        A=M
        M=-1
        (END_{self.iter})
        @SP
        M=M+1 
        """
        return asm_command

    def write_add_or_sub(self, symbol):
        if symbol == '+':
            comment = "add"
        else:
            comment = "sub"

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
        
    def write_static_push(self, command, index):
        address = "StaticTest"
        asm_command = f"""
        // {command}
        @{address}.{index}
        D=M
        @SP
        M=M+1
        A=M-1
        M=D
        """
        return asm_command
    
    def write_static_pop(self, command, index):
        address = "StaticTest"
        asm_command = f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @{address}.{index}
        M=D
        """
        return asm_command
        
        
    def write_pointer_push(self, command, index):
        asm_command = f"""
        // {command}
        @{3 + int(index)}
        D=M
        @SP
        M=M+1
        A=M-1
        M=D    
        """
        return asm_command
    
    def write_pointer_pop(self, command, index):
        asm_command = f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @{3 + int(index)}
        M=D
        """
        return asm_command

    def write_temp_pop(self, command, index):
        asm_command = f"""
            // {command}
            @SP
            M=M-1
            A=M
            D=M
            @R{5 + int(index)}
            M=D
            """
        return asm_command

    def write_temp_push(self, command, index):
        asm_command = f"""
            // {command}
            @{5 + int(index)}
            D=M
            @SP
            M=M+1
            A=M-1
            M=D
            """
        return asm_command

    def write_const_push(self, command, index):
        asm_command = f"""
            // {command}
            @{index}
            D=A
            @SP
            M=M+1
            A=M-1
            M=D
            """
        return asm_command

    def write_normal_push(self, command, segment, index):
        segment_symbol = self.segment_to_symbol(segment)
        asm_command = f"""
        // {command}
        @{index}
        D=A
        @{segment_symbol}
        A=M+D
        D=M
                        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

        return asm_command

    def write_normal_pop(self, command, segment, index):
        asm_command = ""
        if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            segment_symbol = self.segment_to_symbol(segment)
            asm_command = f"""
            // {command}
            @{index}
            D=A
            @{segment_symbol}
            D=M+D
            @R13
            M=D
            
            @SP
            M=M-1
            A=M
            D=M
            @R13
            A=M
            M=D
            """

        return asm_command

    def segment_to_symbol(self, segment):
        if segment == "local":
            return "LCL"
        elif segment == "argument":
            return "ARG"
        elif segment == "this":
            return "THIS"
        elif segment == "that":
            return "THAT"
        elif segment == "temp":
            return "R5"
        elif segment == "pointer":
            return "R3"
        elif segment == "static":
            return "16"

    def write_line(self, code):
        if not code:
            return

        with open(self.file_output, mode="a") as file:
            file.write(code)
