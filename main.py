from assembly_output import Code_Writer
from vm_parser import VM_Parser
from driver import Driver


main = Driver("./not-python/FibonacciSeries/FibonacciSeries.vm", "./not-python/FibonacciSeries/FibonacciSeries.asm", VM_Parser, Code_Writer)
main.run()  