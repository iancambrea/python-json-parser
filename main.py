class JSONParser:
    def __init__(self):
        self.json_str = None
        self.index = 0

    def _skip_whitespace(self):
        while self.index < len(self.json_str) and self.json_str[self.index].isspace():
            self.index += 1

    def _parse_value(self):
        self._skip_whitespace()

        match self.json_str[self.index]:
            case "{":
                return self._parse_object()
            case "[":
                return self._parse_array()
            case '"':
                return self._parse_string()
            case "t":
                self.index += 4
                return True
            case "f":
                self.index += 5
                return False
            case "n":
                self.index += 4
                return None
            case _:
                return self._parse_number()

    def _parse_string(self):
        self.index += 1
        start = self.index
        while self.index < len(self.json_str) and self.json_str[self.index] != '"':
            self.index += 1
        if self.index < len(self.json_str) and self.json_str[self.index] == '"':
            self.index += 1
            return self.json_str[start : self.index - 1]
        else:
            raise ValueError("JSON string is not properly terminated.")

    def _parse_number(self):
        start = self.index
        while self.index < len(self.json_str) and (
            self.json_str[self.index].isdigit()
            or self.json_str[self.index] in ["-", ".", "e", "E"]
        ):
            self.index += 1
        return float(self.json_str[start : self.index])

    def _parse_array(self):
        self.index += 1
        self._skip_whitespace()
        result = []
        while self.json_str[self.index] != "]":
            value = self._parse_value()
            result.append(value)
            self._skip_whitespace()
            if self.json_str[self.index] == ",":
                self.index += 1
                self._skip_whitespace()
        self.index += 1
        return result

    def _parse_object(self):
        self.index += 1
        self._skip_whitespace()
        result = {}
        while self.json_str[self.index] != "}":
            key = self._parse_string()
            self._skip_whitespace()
            if self.json_str[self.index] != ":":
                raise ValueError("Invalid JSON format.")
            self.index += 1
            value = self._parse_value()
            result[key] = value
            self._skip_whitespace()
            if self.json_str[self.index] == ",":
                self.index += 1
                self._skip_whitespace()
        self.index += 1
        return result

    @staticmethod
    def parse(json_str):
        instance = JSONParser()
        instance.json_str = json_str
        return instance._parse_value()
