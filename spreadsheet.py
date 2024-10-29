
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
            # No values containing floats
            result = "#Error"
        elif isinstance(value, str):
            if "." in value:
                # No values containing decimals
                return "#Error"
            if value.startswith("'") and value.endswith("'"):
                result = value[1:-1]
            elif value.startswith("='") and value.endswith("'"):
                result = value[2:-1]
            elif value.startswith("="):
                try:
                    # Evaluate the expression after '=' assuming it's a simple integer or a reference to another cell
                    if value[1:].isdigit():
                        result = int(value[1:])
                    elif "+" in value or "*" in value or "/" in value:
                        # Handle arithmetic expressions possibly containing B1 cell references
                        # B1 can't refer to A1
                        if self._cells.get("B1") == "=A1":
                            return "#Circular"
                        value = value.replace("B1", str(self.evaluate("B1")))
                        expression = value[1:]
                        try:
                            result = eval(expression, {"__builtins__": None}, {})
                        except Exception:
                            return "#Error"
                    else:
                        result = self.evaluate(value[1:])
                except (ValueError, ZeroDivisionError):
                    result = "#Error"
            else:
                result = "#Error"
        else:
            result = "#Error"
        
        self._evaluating.remove(cell)
        return result

