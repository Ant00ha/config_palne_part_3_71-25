"""Модульные тесты для ассемблера."""

import unittest

from src.assembler import translate_to_ir


class TestAssembler(unittest.TestCase):
    """Тесты трансляции команд."""

    def test_load_const(self) -> None:
        """Тест LOAD_CONST (A=5, B=70)."""
        data = [{"op": "LOAD_CONST", "value": 70}]
        ir = translate_to_ir(data)
        self.assertEqual(ir[0].field_a, 5)
        self.assertEqual(ir[0].field_b, 70)

    def test_read_mem(self) -> None:
        """Тест READ_MEM (A=83)."""
        data = [{"op": "READ_MEM"}]
        ir = translate_to_ir(data)
        self.assertEqual(ir[0].field_a, 83)

    def test_write_mem(self) -> None:
        """Тест WRITE_MEM (A=78, B=215)."""
        data = [{"op": "WRITE_MEM", "addr": 215}]
        ir = translate_to_ir(data)
        self.assertEqual(ir[0].field_a, 78)
        self.assertEqual(ir[0].field_b, 215)

    def test_unary_minus(self) -> None:
        """Тест UNARY_MINUS (A=90, C=145)."""
        data = [{"op": "UNARY_MINUS", "addr": 145}]
        ir = translate_to_ir(data)
        self.assertEqual(ir[0].field_a, 90)
        self.assertEqual(ir[0].field_c, 145)


if __name__ == "__main__":
    unittest.main()