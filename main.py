from assembly_output.main import Code_Writer
from vm_parser import VM_Parser
from driver import Driver


main = Driver("./not-python/FibonacciElement", "./not-python/FibonacciElement/FibonacciElement.asm", VM_Parser, Code_Writer)
main.run()  