import os


# Метод принимает имя файла в аргументе filename. Если имя файла не оканчивается на .json, то к нему добавляется
# это расширение. Затем метод с помощью функции os.path.join создает полный путь к файлу в корне проекта. В блоке
# try-except открывается файл на запись, если всё проходит успешно, то файл создается. Если возникает ошибка,
# то выбрасывается исключение с текстом ошибки.
def create_json_file(filename: str):
    if filename == '':
        raise Exception(f"Ошибка: пустое имя недопустимо")
    if not filename.upper().endswith('.JSON'):
        filename += '.JSON'

    file_path = os.path.join(os.getcwd(), filename)

    if os.path.exists(file_path):
        raise Exception(f"Ошибка: файл {filename} уже существует")

    try:
        with open(file_path, 'w') as f:
            f.write('{}')
    except Exception as e:
        raise Exception(f"Ошибка при создании файла {filename}: {e}")


# Метод возвращает список файлов с расширением .json из корневой папки проекта
def get_json_files():
    root_dir = os.getcwd()
    json_files = [file for file in os.listdir(root_dir) if file.lower().endswith('.json')]
    return json_files
