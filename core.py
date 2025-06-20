import dis, textwrap

def del_demo():
    data = [10, 20, 30, 40]
    del data[1]

def remove_demo():
    data = [10, 20, 30, 40]
    data.remove(30)

print("Bytecode for del_demo:")
disassembled_del = dis.Bytecode(del_demo)
print(textwrap.indent('\n'.join(f"{instr.opname:<20}{instr.argrepr}" for instr in disassembled_del), "  "))

print("\nBytecode for remove_demo:")
disassembled_remove = dis.Bytecode(remove_demo)
print(textwrap.indent('\n'.join(f"{instr.opname:<20}{instr.argrepr}" for instr in disassembled_remove), "  "))
