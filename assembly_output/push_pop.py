import os

class PushPopWriter:
    def __init__(self, file_output, file_name):
        self.file_output = file_output
        self.file_name = os.path.splitext(os.path.basename(file_name))[0]  # Extract just the file name without path
        self.current_function = ""
                
    def set_filename(self, file_name):
        self.file_name = os.path.splitext(os.path.basename(file_name))[0]  # Extract just the file name without path
        
    def write_push_pop(self, command, type, segment, index):
        asm_command = ""
        if type == "C_PUSH":
            if segment in ["local", "argument", "this", "that"]:
                asm_command = self.write_normal_push(command, segment, index)
            elif "constant" in segment:
                asm_command = self.write_const_push(command, index)
            elif "temp" in segment:
                asm_command = self.write_temp_push(command, index)
            elif "pointer" in segment:
                asm_command = self.write_pointer_push(command, index)
            elif "static" in segment:
                asm_command = self.write_static_push(command, index)
        elif type == "C_POP":
            if segment in ["local", "argument", "this", "that"]:
                asm_command = self.write_normal_pop(command, segment, index)
            elif "temp" in segment:
                asm_command = self.write_temp_pop(command, index)
            elif "pointer" in segment:
                asm_command = self.write_pointer_pop(command, index)
            elif "static" in segment:
                asm_command = self.write_static_pop(command, index)
        self.write_line(asm_command)

    def write_normal_push(self, command, segment, index):
        segment_symbol = self.segment_to_symbol(segment)
        return f"""
        // {command}
        @{segment_symbol}
        D=M
        @{index}
        A=D+A
        D=M
        @SP
        M=M+1
        A=M-1
        M=D
        """

    def write_const_push(self, command, index):
        return f"""
        // {command}
        @{index}
        D=A
        @SP
        M=M+1
        A=M-1
        M=D
        """

    def write_temp_push(self, command, index):
        return f"""
        // {command}
        @{5 + int(index)}
        D=M
        @SP
        M=M+1
        A=M-1
        M=D
        """

    def write_pointer_push(self, command, index):
        return f"""
        // {command}
        @{3 + int(index)}
        D=M
        @SP
        M=M+1
        A=M-1
        M=D
        """

    def write_static_push(self, command, index):
        return f"""
        // {command}
        @{self.file_name}.{index}
        D=M
        @SP
        M=M+1
        A=M-1
        M=D
        """

    def write_normal_pop(self, command, segment, index):
        segment_symbol = self.segment_to_symbol(segment)
        unique_temp_var = f"{self.current_function}$temp"
        return f"""
        // {command}
        @{index}
        D=A
        @{segment_symbol}
        D=M+D
        @{unique_temp_var}
        M=D
        @SP
        AM=M-1
        D=M
        @{unique_temp_var}
        A=M
        M=D
        """

    def write_temp_pop(self, command, index):
        return f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @R{5 + int(index)}
        M=D
        """

    def write_pointer_pop(self, command, index):
        return f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @{3 + int(index)}
        M=D
        """

    def write_static_pop(self, command, index):
        return f"""
        // {command}
        @SP
        M=M-1
        A=M
        D=M
        @{self.file_name}.{index}
        M=D
        """

    def segment_to_symbol(self, segment):
        return {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            "temp": "R5",
            "pointer": "R3",
            "static": "16"
        }[segment]

    def write_line(self, code):
        if not code:
            return
        with open(self.file_output, mode="a") as file:
            file.write(code)
