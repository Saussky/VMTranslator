from assembly_output import Code_Writer
from vm_parser import VM_Parser
from driver import Driver


main = Driver("./not-python/StaticTest.vm", "./not-python/StaticTest.asm", VM_Parser, Code_Writer)
main.run()  