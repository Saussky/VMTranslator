import os

class Driver:
    def __init__(self, file_input, file_output, parser, writer,):
        self.file_input = file_input
        self.file_output = file_output
        self.parser_class = parser
        self.writer = writer(self.file_output)

    def check_dir_or_file(self, input_path):
        if os.path.isdir(input_path):
            print('ahah')
            return [
                os.path.join(input_path, file)
                for file in os.listdir(input_path)
                if file.endswith(".vm")
            ]
        else:
            return [input_path]
        
    def run(self):
        vm_files = self.check_dir_or_file(self.file_input)
        
        for vm_file in vm_files:
            self.parser = self.parser_class(vm_file)
            self.writer.set_filename(vm_file)
            
            while self.parser.has_more_commands:
                self.parser.advance()
                
                if self.parser.command_type == "C_PUSH" or self.parser.command_type == "C_POP":
                    self.writer.write_push_pop(self.parser.current_command, self.parser.command_type, self.parser.arg1, self.parser.arg2)
                
                elif self.parser.command_type == "C_ARITHMETIC":
                    self.writer.write_arithmetic(self.parser.current_command)

                elif self.parser.command_type == "C_FLOW":
                    self.writer.write_flow(self.parser.current_command, self.parser.arg1, self.parser.arg2)
                    
                elif self.parser.command_type == "C_FUNCTION":
                    self.writer.write_flow(self.parser.current_command, self.parser.arg1, self.parser.arg2, self.parser.arg3)
                
                elif self.parser.command_type == "C_RETURN":
                    self.writer.write_flow(self.parser.current_command, self.parser.arg1, self.parser.arg2)

                    
