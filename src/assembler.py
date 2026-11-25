"""Ассемблер УВМ: YAML -> промежуточное представление -> машинный код."""

import sys
import struct
from typing import List

import yaml

from src.models import Command

OPCODES = {
    "LOAD_CONST": 5,
    "READ_MEM": 83,
    "WRITE_MEM": 78,
    "UNARY_MINUS": 90,
}

COMMAND_SIZE = 8


def parse_yaml(filepath: str) -> List[dict]:
    """Чтение и валидация YAML-файла."""
    with open(filepath, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, list):
        raise ValueError("YAML должен содержать список команд.")
    return data


def translate_to_ir(yaml_data: List[dict]) -> List[Command]:
    """Трансляция YAML в промежуточное представление (IR)."""
    ir_program = []
    for item in yaml_data:
        op_name = item.get("op")
        if op_name not in OPCODES:
            raise ValueError(f"Неизвестная операция: {op_name}")

        opcode = OPCODES[op_name]

        
        field_b = 0
        field_c = 0

        if op_name == "LOAD_CONST":
            field_b = item.get("value", 0)
        elif op_name == "WRITE_MEM":
            field_b = item.get("addr", 0)
        elif op_name == "UNARY_MINUS":
            field_b = item.get("offset", 0)  
            field_c = item.get("addr", 0)    
        

        cmd = Command(
            opcode=opcode,
            field_a=opcode,
            field_b=field_b,
            field_c=field_c,
        )
        ir_program.append(cmd)
    return ir_program


def generate_machine_code(ir_program: List[Command]) -> bytes:
    """Трансляция IR в машинный код (байты)."""
    binary_data = bytearray()

    for cmd in ir_program:
        
        val = 0
       
        val |= (cmd.field_a & 0x7F) << 0
       
        val |= (cmd.field_b & 0xFF) << 7
        
        val |= (cmd.field_c & 0x1FFFFFF) << 12
        
        packed_command = struct.pack("<Q", val)
        binary_data.extend(packed_command)

    return bytes(binary_data)


def print_hex_dump(binary_data: bytes) -> None:
    """Вывод машинного кода в hex-формате (как в тестах)."""
    print(f"Размер двоичного файла: {len(binary_data)} байт")
    
    for i in range(0, len(binary_data), 8):
        chunk = binary_data[i:i+8]
        hex_str = ", ".join(f"0x{b:02X}" for b in chunk)
        print(hex_str)


def main() -> None:
    """Точка входа CLI ассемблера."""
    if len(sys.argv) < 3:
        print("Использование: python -m src.assembler <src.yaml> <dst.bin> [--test]")
        sys.exit(1)

    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    test_mode = "--test" in sys.argv

    try:
        yaml_data = parse_yaml(src_path)
        ir_program = translate_to_ir(yaml_data)
        
        
        binary_data = generate_machine_code(ir_program)

        
        with open(dst_path, "wb") as file:
            file.write(binary_data)

        if test_mode:
            print(f"--- Успешно скомпилировано: {src_path} ---")
            print_hex_dump(binary_data)
        else:
            print(f"Успешно скомпилировано {len(ir_program)} команд. Файл {dst_path} создан.")

    except Exception as error:
        print(f"Ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()