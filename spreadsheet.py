
class SpreadSheet:

    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value) -> None:
        self._cells[cell] = value

    def evaluate(self, cell: str):
        value = self._cells[cell]
        if isinstance(value, int):
            return value
        elif isinstance(value, str) and value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        else:
            return "#Error"

