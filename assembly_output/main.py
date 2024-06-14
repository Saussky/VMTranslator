import os

from assembly_output.arithmetic import ArithmeticWriter
from assembly_output.flow import FlowWriter
from assembly_output.push_pop import PushPopWriter


class Code_Writer:
    def __init__(self, file_output):
        self.file_output = file_output
        self.clear_file(self.file_output)
        self.write_init(self.file_output)
        self.file_name = os.path.splitext(os.path.basename(self.file_output))[0]
        self.arithmetic_writer = ArithmeticWriter(self.file_output)
        self.flow_writer = FlowWriter(self.file_output)
        self.push_pop_writer = PushPopWriter(self.file_output, self.file_name)
        
    def set_filename(self, file_name):
        self.file_name = file_name
        self.push_pop_writer.set_filename(file_name)

    def clear_file(self, file_output):
        with open(file_output, mode="w") as file:
            file.write("")
    
    def write_init(self, file_output):
        asm_command = """
        @256
        D=A
        @SP
        M=D
        """
        with open(file_output, mode="a") as file:
            file.write(asm_command)

    def write_push_pop(self, command, type, segment, index):
        self.push_pop_writer.write_push_pop(command, type, segment, index)

    def write_arithmetic(self, command):
        self.arithmetic_writer.write_arithmetic(command)

    def write_flow(self, command, type, name, nvars=None):
        self.flow_writer.write_flow(command, type, name, nvars)
