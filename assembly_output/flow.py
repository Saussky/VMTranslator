class FlowWriter:
    def __init__(self, file_output):
        self.file_output = file_output
        self.call_counter = 1
        self.current_function = ""

    def write_flow(self, command, type, name, nvars=None):
        asm_command = ""
        if "label" in type:
            asm_command = self.write_label(command, name)
        elif "if-goto" in type:
            asm_command = self.write_if_goto(command, name)
        elif "goto" in type:
            asm_command = self.write_goto(command, name)
        elif "function" in type:
            asm_command = self.write_function(command, name, nvars)
        elif "call" in type:
            asm_command = self.write_call(command, name, nvars)
        elif "return" in command:
            asm_command = self.write_return(command)
        self.write_line(asm_command)

    def write_label(self, command, name):
        scoped_label = f"{self.current_function}${name}"
        return f"""
        // {command}
        ({scoped_label})
        """

    def write_goto(self, command, name):
        scoped_label = f"{self.current_function}${name}"
        return f"""
        // {command}
        @{scoped_label}
        0;JMP
        """

    def write_if_goto(self, command, name):
        print('if gotototo')
        scoped_label = f"{self.current_function}${name}"
        return f"""
        // {command}
        @SP
        AM=M-1
        D=M
        @{scoped_label}
        D;JNE
        """
        
    def write_function(self, command, function_name, n_vars):
        self.current_function = function_name
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
        return_address = f"{self.current_function}$ret.{self.call_counter}"
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
        
        // Save LCL
        @LCL
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        // Save ARG
        @ARG
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        // Save THIS
        @THIS
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        // Save THAT
        @THAT
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        
        // Reposition ARG
        @SP
        D=M
        @5
        D=D-A
        @{n_vars}
        D=D-A
        @ARG
        M=D
        
        // Reposition LCL
        @SP
        D=M
        @LCL
        M=D
        
        // Goto function
        @{function_name}
        0;JMP
        
        // (return-address)
        ({return_address})
        """
        return asm_command

    def write_return(self, command):
        frame_temp = f"{self.current_function}$frame"
        ret_temp = f"{self.current_function}$ret"
        asm_command = f"""
        // {command}
        @LCL
        D=M
        @{frame_temp}
        M=D                  // FRAME = LCL
        @5
        A=D-A
        D=M
        @{ret_temp}
        M=D                  // RET = *(FRAME-5)
        
        @SP
        AM=M-1
        D=M
        @ARG
        A=M
        M=D                  // *ARG = pop()
        
        @ARG
        D=M+1
        @SP
        M=D                  // SP = ARG+1
        
        @{frame_temp}
        A=M-1
        D=M
        @THAT
        M=D                  // THAT = *(FRAME-1)
        
        @{frame_temp}
        D=M
        @2
        D=D-A
        A=D
        D=M
        @THIS
        M=D                  // THIS = *(FRAME-2)
        
        @{frame_temp}
        D=M
        @3
        D=D-A
        A=D
        D=M
        @ARG
        M=D                  // ARG = *(FRAME-3)
        
        @{frame_temp}
        D=M
        @4
        D=D-A
        A=D
        D=M
        @LCL
        M=D                  // LCL = *(FRAME-4)
        
        @{ret_temp}
        A=M
        0;JMP                // goto RET
        """
        return asm_command

    def write_line(self, code):
        if not code:
            return
        with open(self.file_output, mode="a") as file:
            file.write(code)
