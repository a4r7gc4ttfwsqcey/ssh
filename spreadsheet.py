
class SpreadSheet:

    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value) -> None:
        self._cells[cell] = value

    def evaluate(self, cell: str):
        value = self._cells.get(cell)
        if isinstance(value, int):
            return value
        elif isinstance(value, float):
            return "#Error"
        elif isinstance(value, str):
            if value.startswith("'") and value.endswith("'"):
                return value[1:-1]
            elif value.startswith("='") and value.endswith("'"):
                return value[2:-1]
            elif value.startswith("="):
                try:
                    # Evaluate the expression after '=' assuming it's a simple integer for now
                    return int(value[1:])
                except ValueError:
                    return "#Error"
        return "#Error"

