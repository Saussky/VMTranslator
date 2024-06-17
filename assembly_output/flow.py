class FlowWriter:
    def __init__(self, file_output):
        self.file_output = file_output
        self.call_counter = 1

    def write_flow(self, command, type, name, nvars=None):
        asm_command = ""
        if "label" in type:
            asm_command = self.write_label(command, name)
        elif "goto" in type:
            asm_command = self.write_goto(command, name)
        elif "if-goto" in type:
            asm_command = self.write_if_goto(command, name)
        elif "function" in type:
            asm_command = self.write_function(command, name, nvars)
        elif "call" in type:
            asm_command = self.write_call(command, name, nvars)
        elif "return" in command:
            asm_command = self.write_return(command)
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
        
    def write_function(self, command, function_name, n_vars):
        asm_command = f"""
        // {command}
        ({function_name})
        """
        for i in range(int(n_vars)):
            asm_command += """
            @0
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
        
        return asm_command
    
    def write_call(self, command, function_name, n_vars):
        return_address = f"RETURN_{self.call_counter}"
        self.call_counter += 1
        asm_command = f"""
        // {command}
        @{return_address}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        @LCL
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        @ARG
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        @THIS
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        @THAT
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        @SP
        D=M
        @5
        D=D-A
        @{n_vars}
        D=D-A
        @ARG
        M=D
        
        @SP
        D=M
        @LCL
        M=D
        
        @{function_name}
        0;JMP
        
        ({return_address})
        """
        return asm_command

    def write_return(self, command):
        asm_command = f"""
        // {command}
        @LCL
        D=M
        @R13
        M=D                  // FRAME = LCL
        @5
        A=D-A
        D=M
        @R14
        M=D                  // RET = *(FRAME-5)
        
        @SP
        A=M-1
        D=M
        @ARG
        A=M
        M=D                  // *ARG = pop()
        
        @ARG
        D=M+1
        @SP
        M=D                  // SP = ARG+1
        
        @R13
        AM=M-1
        D=M
        @THAT
        M=D                  // THAT = *(FRAME-1)
        
        @R13
        AM=M-1
        D=M
        @THIS
        M=D                  // THIS = *(FRAME-2)
        
        @R13
        AM=M-1
        D=M
        @ARG
        M=D                  // ARG = *(FRAME-3)
        
        @R13
        AM=M-1
        D=M
        @LCL
        M=D                  // LCL = *(FRAME-4)
        
        @R14
        A=M
        0;JMP                // goto RET
        """
        return asm_command

    def write_line(self, code):
        if not code:
            return
        with open(self.file_output, mode="a") as file:
            file.write(code)

