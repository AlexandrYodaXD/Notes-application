import json
from datetime import datetime

from model.note import Note


class NotesRepository:
    def __init__(self):
        self.notes = dict()
        self.file_name = ''

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    def add_note(self, note: Note):
        self.notes[note.id] = note

    def get_note(self, note_id: int):
        if note_id in self.notes:
            return self.notes.get(note_id)
        else:
            raise Exception("Ошибка: заметки с указанным id не существует")

    def get_all_notes(self, sorting_key=None):
        if sorting_key is None:
            # return [self.notes.get(x) for x in sorted(self.notes.keys())]
            return sorted(self.notes.values(), key=lambda x: self.notes.keys())
        return sorted(self.notes.values(), key=lambda x: getattr(x, sorting_key))

    def update_note(self, note_id: int, new_title: str, new_content: str, new_modification_time: datetime):
        note = self.get_note(note_id)
        note.title = new_title
        note.content = new_content
        note.modification_time = new_modification_time

    def delete_note(self, note_id: int):
        if note_id in self.notes:
            del self.notes[note_id]
        else:
            raise Exception("Ошибка: заметки с указанным id не существует")

    # Метод load_notes принимает путь к файлу с заметками, открывает его и загружает данные в переменную data. Затем для
    # каждого элемента из data создается объект Note и добавляется в словарь notes с помощью метода add_note.
    def load_notes(self, filename: str):
        try:
            with open(filename, "r", encoding='utf-8') as f:
                notes_data = json.load(f)
        except FileNotFoundError:
            raise Exception(f"Ошибка: файл {filename} не найден")
        except json.JSONDecodeError:
            raise Exception(f"Ошибка: файл {filename} имеет некорректный формат данных")
        self.file_name = filename
        for note_data in notes_data:
            note = Note(
                idx=int(note_data["id"]),
                title=note_data["title"],
                body=note_data["body"],
                updated_at=datetime.strptime(note_data["updated_at"], '%Y-%m-%d %H:%M:%S'),
            )
            self.add_note(note)

    # Метод save_notes принимает путь к файлу, создает список data из словарей, полученных из атрибута __dict__
    # каждого объекта Note в словаре notes. Затем метод открывает файл и записывает данные в него с помощью метода dump.
    def save_notes(self):
        data = [note.to_dict() for note in self.notes.values()]
        try:
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Ошибка при сохранении заметок в файл {self.file_name}: {e}")
