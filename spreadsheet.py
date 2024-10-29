
class SpreadSheet:

    def __init__(self):
        self._cells = {}
        self._evaluating = set()

    def set(self, cell: str, value) -> None:
        self._cells[cell] = value

    def evaluate(self, cell: str):
        if cell in self._evaluating:
            return "#Circular"
        self._evaluating.add(cell)
        
        value = self._cells.get(cell)
        if isinstance(value, int):
            result = value
        elif isinstance(value, float):
            result = "#Error"
        elif isinstance(value, str):
            if value.startswith("'") and value.endswith("'"):
                result = value[1:-1]
            elif value.startswith("='") and value.endswith("'"):
                result = value[2:-1]
            elif value.startswith("="):
                try:
                    # Evaluate the expression after '=' assuming it's a simple integer or a reference to another cell
                    if value[1:].isdigit():
                        result = int(value[1:])
                    elif "+" in value:
                        parts = value[1:].split('+')
                        result = sum(int(part) for part in parts)
                    else:
                        result = self.evaluate(value[1:])
                except ValueError:
                    result = "#Error"
            else:
                result = "#Error"
        else:
            result = "#Error"
        
        self._evaluating.remove(cell)
        return result

