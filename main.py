from assembly_output.main import Code_Writer
from vm_parser import VM_Parser
from driver import Driver


main = Driver("./not-python/SimpleFunction/SimpleFunction.vm", "./not-python/SimpleFunction/SimpleFunction.asm", VM_Parser, Code_Writer)
main.run()  