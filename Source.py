class Source:
    def __init__(self, text_generator):
        self._iterator = iter(text_generator)
        self._text = next(self._iterator)
        self._pos = 0

        # Only these fields should be used outside
        self.current_char = self._text[self._pos]
        self.line = 1
        self.column = 1

    def move_to_next_char(self):
        # Check if text piece is over.
        # If so get next piece.
        if self._pos > len(self._text) - 1:
            self._text = next(self._iterator)
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
        file = open(filename)
        text_generator = FileSource.read_in_chunks(file)

        if text_generator is not None:
            super().__init__(text_generator)
            self.file = file
        else:
            # File is empty
            file.close()
            # todo
            pass

    def __del__(self):
        self.file.close()

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
