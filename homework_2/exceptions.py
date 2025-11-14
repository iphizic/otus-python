class InvalidFileException(Exception):
    def __init__(self):
        super().__init__(f"Файл поврежден.")
