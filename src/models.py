"""Модели данных для УВМ."""

from dataclasses import dataclass


@dataclass
class Command:
    """Промежуточное представление команды УВМ."""

    opcode: int
    field_a: int
    field_b: int = 0
    field_c: int = 0

    def __str__(self) -> str:
        """Форматирование для тестового вывода."""
        return (
            f"A={self.field_a:<3} "
            f"B={self.field_b:<3} "
            f"C={self.field_c:<3}"
        )