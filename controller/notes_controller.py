from datetime import datetime

import model
from model import Note

notebook = model.NotesRepository()


def create_new_notebook(filename: str):
    model.create_json_file(filename)
    global notebook
    notebook = model.NotesRepository()
    notebook.file_name = filename


def get_json_files():
    return model.get_json_files()


def get_opened_file():
    return notebook.file_name


def load_notebook(filename: str):
    global notebook
    notebook = model.NotesRepository()
    notebook.load_notes(filename)


def get_all_notes(sorting_key=None):
    return notebook.get_all_notes(sorting_key)


def get_note(idx: int):
    return notebook.get_note(idx)


def delete_note(note):
    notebook.delete_note(note.id)


def update(note: Note, idx=None, title=None, body=None):
    if idx is not None:
        note.id = idx
    if title is not None:
        note.title = title
    if body is not None:
        note.body = body
    if any(x is not None for x in [idx, title, body]):
        note.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_new_id():
    all_notes = notebook.get_all_notes()
    max_id = 0
    for note in all_notes:
        if note.id > max_id:
            max_id = note.id
    return max_id + 1


def add_new_note(title: str, body: str):
    new_id = get_new_id()
    update_time = datetime.now()
    new_note = Note(new_id, title, body, update_time)
    notebook.add_note(new_note)


def save_file():
    notebook.save_notes()
