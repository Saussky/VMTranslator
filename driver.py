class Driver:
    def __init__(self, file_input, file_output, parser, writer,):
        self.file_input = file_input
        self.file_output = file_output
        self.parser = parser(self.file_input)
        self.writer = writer(self.file_output)

    def run(self):
        while self.parser.has_more_commands:
            self.parser.advance()
            if self.parser.command_type == "C_PUSH" or self.parser.command_type == "C_POP":
                self.writer.write_push_pop(self.parser.current_command, self.parser.command_type, self.parser.arg1, self.parser.arg2)
            elif self.parser.command_type == "C_ARITHMETIC":
                self.writer.write_arithmetic(self.parser.current_command)

            elif self.parser.command_type == "C_FLOW":
                self.writer.write_flow(self.parser.current_command, self.parser.arg1, self.parser.arg2)
