def read_data(file_path: str):
    with open(file_path, encoding="utf-8") as file:
        return file.read()
