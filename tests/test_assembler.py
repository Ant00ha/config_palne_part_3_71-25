"""Модульные тесты для ассемблера."""

import unittest

from src.assembler import translate_to_ir, generate_machine_code


class TestAssembler(unittest.TestCase):
    """Тесты трансляции команд."""

    def test_load_const(self) -> None:
        """Тест LOAD_CONST (A=5, B=70)."""
        data = [{"op": "LOAD_CONST", "value": 70}]
        ir = translate_to_ir(data)
        binary = generate_machine_code(ir)
        # Спецификация: 0x05, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        self.assertEqual(binary.hex(), "0523000000000000")

    def test_read_mem(self) -> None:
        """Тест READ_MEM (A=83)."""
        data = [{"op": "READ_MEM"}]
        ir = translate_to_ir(data)
        binary = generate_machine_code(ir)
        # Спецификация: 0x53, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        self.assertEqual(binary.hex(), "5300000000000000")

    def test_write_mem(self) -> None:
        """Тест WRITE_MEM (A=78, B=215)."""
        data = [{"op": "WRITE_MEM", "addr": 215}]
        ir = translate_to_ir(data)
        binary = generate_machine_code(ir)
        # Спецификация: 0xCE, 0x6B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        self.assertEqual(binary.hex(), "ce6b000000000000")

    def test_unary_minus(self) -> None:
        """Тест UNARY_MINUS (A=90, B=13, C=145)."""
        data = [{"op": "UNARY_MINUS", "addr": 145, "offset": 13}]
        ir = translate_to_ir(data)
        binary = generate_machine_code(ir)
        self.assertEqual(binary.hex(), "da16090000000000")


if __name__ == "__main__":
    unittest.main()