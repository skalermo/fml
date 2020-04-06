from Token import TokenType


class Source:
    def __init__(self, text_generator):
        self._iterator = iter(text_generator)
        self._text = next(self._iterator)
        self._pos = 0

        self.current_char = self._text[self._pos]
        self.line = 1
        self.column = 1

    def move_to_next_char(self):
        # Check if text piece is over.
        # If so get next piece.
        if self._pos > len(self._text) - 1:
            try:
                self._text = next(self._iterator)
            except StopIteration:
                self.current_char = TokenType.ETX.value
                return
            else:
                self._pos = 0

        self.current_char = self._text[self._pos]
        self.column += 1

        # Move to the move_to_next_char character
        # Set current_char
        if self.current_char == '\n':
            self.line += 1
            self.column = 0

        self._pos += 1


class FileSource(Source):
    def __init__(self, filename):
        self._file = open(filename)
        text_generator = FileSource.read_in_chunks(self._file)
        super().__init__(text_generator)

    def __del__(self):
        self._file.close()

    @staticmethod
    def read_in_chunks(file_object, chunk_size=1024):
        """
        Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k.
        """
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
