"""Интерпретатор УВМ."""

import sys
import struct
import xml.etree.ElementTree as ET
from typing import List

COMMAND_SIZE = 8
MEMORY_SIZE = 1024


class VM:
    """Виртуальная машина."""

    def __init__(self) -> None:
        """Инициализация памяти и стека."""
        self.program_memory: bytes = b""
        self.data_memory: List[int] = [0] * MEMORY_SIZE
        self.stack: List[int] = []
        self.pc: int = 0

    def load_program(self, filepath: str) -> None:
        """Загрузка бинарного файла в память команд."""
        with open(filepath, "rb") as f:
            self.program_memory = f.read()

    def fetch_and_decode(self) -> tuple:
        """Чтение и декодирование 8 байт команды."""
        if self.pc >= len(self.program_memory):
            return None

        chunk = self.program_memory[self.pc:self.pc + COMMAND_SIZE]
        val = struct.unpack("<Q", chunk)[0]

        
        field_a = val & 0x7F  
        
        
        field_b = (val >> 7) & 0x1F          
        
        
        field_c = (val >> 12) & 0x1FFFFFF    

        self.pc += COMMAND_SIZE
        return field_a, field_b, field_c

    def execute(self) -> None:
        """Основной цикл интерпретации."""
        while True:
            cmd = self.fetch_and_decode()
            if cmd is None:
                break

            opcode, field_b, field_c = cmd

            if opcode == 5:  
                self.stack.append(field_b)
            elif opcode == 83:  
                addr = self.stack.pop()
                val = self.data_memory[addr]
                self.stack.append(val)
            elif opcode == 78:  
                val = self.stack.pop()
                addr = field_b
                self.data_memory[addr] = val
            elif opcode == 90:  
                base_addr = self.stack.pop()
                addr = base_addr + field_b
                val = self.data_memory[addr]
                self.data_memory[field_c] = -val 
            else:
                raise ValueError(f"Неизвестный опкод: {opcode}")

    def dump_memory(self, filepath: str, start_addr: int, end_addr: int) -> None:
        """Сохранение дампа памяти в XML."""
        root = ET.Element("memory")
        for addr in range(start_addr, end_addr + 1):
            if addr < len(self.data_memory):
                cell = ET.SubElement(root, "cell")
                cell.set("address", str(addr))
                cell.text = str(self.data_memory[addr])
        
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(filepath, encoding="utf-8", xml_declaration=True)


def main() -> None:
    """Точка входа CLI интерпретатора."""
    if len(sys.argv) < 5:
        print("Использование: python -m src.interpreter <bin> <xml> <start> <end>")
        sys.exit(1)

    vm = VM()
    vm.load_program(sys.argv[1])
    vm.execute()
    vm.dump_memory(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    print(f"Выполнение завершено. Дамп сохранен в {sys.argv[2]}")


if __name__ == "__main__":
    main()