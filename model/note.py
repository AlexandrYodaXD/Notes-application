from datetime import datetime


class Note:

    def __init__(self, idx: int, title: str, body: str, updated_at: str = None):
        # noinspection PyPropertyAccess
        self.id = idx
        self.title = title
        self.body = body
        self.updated_at = updated_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if len(value) > 255:
            raise ValueError("Заголовок слишком длинный")
        self._title = value

    @property
    def body(self) -> str:
        return self._content

    @body.setter
    def body(self, value: str):
        self._content = value

    @property
    def updated_at(self) -> datetime:
        return self._modification_time

    @updated_at.setter
    def updated_at(self, value: datetime):
        self._modification_time = value or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'body': self.body,
                'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }

    def __str__(self):
        if len(self.title) > 20:
            title = self.title[:17] + '...'
        else:
            title = self.title
        return str(self.id).ljust(4) + \
            self.updated_at.strftime('%Y-%m-%d %H:%M:%S').ljust(22) + \
            title.ljust(22)
