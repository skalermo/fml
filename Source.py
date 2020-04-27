from Token import TokenType


class Source:
    def __init__(self, text_generator):
        self._iterator = iter(text_generator)
        self.current_char = next(self._iterator)

        self.line = 1
        self.column = 1
        self._pos = 1

        # start of new fun definition or statement
        self._last_context_start_pos = 1

    def move_to_next_char(self):
        try:
            self.current_char = next(self._iterator)
        except StopIteration:
            self.current_char = TokenType.ETX.value
            return

        self.column += 1
        self._pos += 1

        if self.current_char == '\n':
            self.line += 1
            self.column = 0

    def get_last_context(self):
        pass

    def update_context_start(self):
        self._last_context_start_pos = self._pos


class FileSource(Source):
    def __init__(self, filename):
        self._file = open(filename)
        text_generator = FileSource._read_in_chars(self._file)
        super().__init__(text_generator)

    def __del__(self):
        self._file.close()

    def get_last_context(self):
        offset = self._pos - self._last_context_start_pos
        self._file.seek(self._last_context_start_pos, 0)
        return self._file.read(offset)

    @staticmethod
    def _read_in_chars(file_object, chunk_size=1024):
        """
        Lazy function (generator) to read a file piece by piece,
        and then a piece char by char.
        Default chunk size: 1k.
        """
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                break
            for char in chunk:
                yield char


class StringSource(Source):
    def __init__(self, string):
        self.string = string
        text_generator = (char for char in string)
        super().__init__(text_generator)

    def get_last_context(self):
        offset = self._pos-self._last_context_start_pos
        return self.string[-offset:]
