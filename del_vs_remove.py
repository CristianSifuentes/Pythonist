def del_demo():
    data = [10, 20, 30, 40]
    del data[1]

def remove_demo():
    data = [10, 20, 30, 40]
    data.remove(30)

import dis
import textwrap
print("Bytecode for del_demo:")
del_bc = dis.Bytecode(del_demo)
print("\n".join(f"{instr.opname:<20}{instr.argrepr}" for instr in del_bc))

print("\nBytecode for remove_demo:")
remove_bc = dis.Bytecode(remove_demo)
print("\n".join(f"{instr.opname:<20}{instr.argrepr}" for instr in remove_bc))
