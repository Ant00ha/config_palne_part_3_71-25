"""Ассемблер УВМ: YAML -> промежуточное представление."""

import sys
from typing import List

import yaml

from src.models import Command

OPCODES = {
    "LOAD_CONST": 5,
    "READ_MEM": 83,
    "WRITE_MEM": 78,
    "UNARY_MINUS": 90,
}


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
        field_b = item.get("value", item.get("addr", 0))
        field_c = item.get("addr", 0) if op_name == "UNARY_MINUS" else 0

        cmd = Command(
            opcode=opcode,
            field_a=opcode,
            field_b=field_b,
            field_c=field_c,
        )
        ir_program.append(cmd)
    return ir_program


def main() -> None:
    """Точка входа CLI ассемблера."""
    if len(sys.argv) < 4:
        print("Использование: python -m src.assembler <src> <dst> --test")
        sys.exit(1)

    src_path = sys.argv[1]
    dst_path = sys.argv[2]
    test_mode = "--test" in sys.argv

    try:
        yaml_data = parse_yaml(src_path)
        ir_program = translate_to_ir(yaml_data)

        if test_mode:
            print(f"--- Внутреннее представление ({src_path}) ---")
            for idx, cmd in enumerate(ir_program):
                print(f"CMD {idx}: {cmd}")
        else:
            print(f"Успешно обработано команд: {len(ir_program)}")

    except Exception as error:
        print(f"Ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()