import curses

import controller


class Menu:
    ITEMS_PER_PAGE = 6

    def __init__(self):
        self.menu_stack = []
        self.menu_items = []
        self.errors_list = []
        self.stdscr = None
        self.errors = None

    def main(self, stdscr):
        self.stdscr = stdscr
        # Устанавливаем цветовые пары
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Устанавливаем цвет заднего фона
        stdscr.bkgd(curses.color_pair(1))

        # Получаем размеры окна
        height, width = self.stdscr.getmaxyx()

        # Добавляем разметку для информационных сообщений
        self.errors = curses.newwin(2, width, height - 2, 0)

        # Убираем курсор
        curses.curs_set(0)

        selected = 0
        page = 0

        while True:
            stdscr.clear()
            stdscr.refresh()
            self.print_title()
            self.print_menu_title()
            self.print_menu(selected, page)
            self.print_forward_back(page)
            self.print_errors()
            key = stdscr.getch()
            if len(self.errors_list) == 0:
                try:
                    if key == curses.KEY_UP:
                        selected = max(selected - 1, 0)
                        while self.menu_items[1][selected][0] == "" and selected > 0:
                            selected = max(selected - 1, 0)
                    elif key == curses.KEY_DOWN:
                        selected = min(selected + 1, min(len(self.menu_items[1]) - 1, Menu.ITEMS_PER_PAGE - 1))
                        while self.menu_items[1][selected][0] == "" and selected < len(self.menu_items[1]):
                            selected = min(selected + 1, min(len(self.menu_items[1]) - 1, Menu.ITEMS_PER_PAGE - 1))
                    elif key == curses.KEY_LEFT:
                        page = max(0, page - 1)
                        selected = 0
                    elif key == curses.KEY_RIGHT:
                        page = min((len(self.menu_items[1]) - 1) // Menu.ITEMS_PER_PAGE, page + 1)
                        selected = 0
                    elif key == 27:
                        self.go_back()
                    elif key == ord('\n'):
                        command = self.menu_items[1][page * Menu.ITEMS_PER_PAGE + selected][1]
                        if callable(command):
                            command()
                        elif isinstance(command, tuple) and callable(command[0]):
                            func, args = command[0], command[1:]
                            func(*args)
                        else:
                            raise TypeError('Ошибка: на исполнение передана невызываемая команда')
                        selected = 0
                        page = 0
                except Exception as e:
                    self.errors_list.append(str(e))

    def print_title(self):
        title_items = [
            "      ::::    :::     ::::::::   :::::::::::   ::::::::::   ::::::::",
            "     :+:+:   :+:    :+:    :+:      :+:       :+:         :+:    :+:",
            "    :+:+:+  +:+    +:+    +:+      +:+       +:+         +:+        ",
            "   +#+ +:+ +#+    +#+    +:+      +#+       +#++:++#    +#++:++#++  ",
            "  +#+  +#+#+#    +#+    +#+      +#+       +#+                +#+   ",
            " #+#   #+#+#    #+#    #+#      #+#       #+#         #+#    #+#    ",
            "###    ####     ########       ###       ##########   ########      "
        ]

        # Определяем начальные координаты заголовка
        height, width = self.stdscr.getmaxyx()
        title_height = len(title_items) + 1
        title_width = max(len(x) for x in title_items)
        title_y = max(height // 2 - title_height // 2 - Menu.ITEMS_PER_PAGE - 5,
                      0)
        title_x = width // 2 - (title_width // 2)

        title_scr = curses.newwin(title_height, title_width + 1, title_y, title_x)

        # Рисуем заголовок
        for i, item in enumerate(title_items):
            title_scr.addstr(i, 0, item, curses.color_pair(3))
        title_scr.refresh()

    def print_menu(self, selected, page):
        menu_item_max_len = max(len(x[0]) for x in self.menu_items[1])
        height, width = self.stdscr.getmaxyx()
        menu_y = height // 2 - 3
        menu_x = width // 2 - menu_item_max_len // 2

        menu_height = min(len(self.menu_items[1]) + 1, Menu.ITEMS_PER_PAGE + 1)

        # Создаем объект меню
        menu = curses.newwin(menu_height, menu_item_max_len, menu_y, menu_x)

        # Устанавливаем начальный цвет для пунктов меню
        menu.bkgd(curses.color_pair(3))

        # Рисуем пункты меню
        start = page * Menu.ITEMS_PER_PAGE
        end = start + Menu.ITEMS_PER_PAGE
        for i, item in enumerate(self.menu_items[1][start:end]):
            if i == selected:
                menu.addstr(i, 0, item[0].center(menu_item_max_len), curses.color_pair(2))
            else:
                menu.addstr(i, 0, item[0].center(menu_item_max_len))

        # Отображаем меню и заголовок на экране
        menu.refresh()

    def print_forward_back(self, page):
        height, width = self.stdscr.getmaxyx()
        menu_width = max(18, max([len(x) for x in self.menu_items[1]]))
        menu_y = int(height / 2) - min(int(len(self.menu_items[1]) / 2),
                                       Menu.ITEMS_PER_PAGE // 2) + Menu.ITEMS_PER_PAGE + 1
        menu_x = width // 2 - menu_width // 2
        forward_back = curses.newwin(1, menu_width, menu_y, menu_x)
        forward_back.bkgd(curses.color_pair(1))

        back = '<<'
        forward = '>>'
        middle = f'стр. {page + 1}/{len(self.menu_items[1]) // Menu.ITEMS_PER_PAGE + 1}'

        if len(self.menu_items[1]) > Menu.ITEMS_PER_PAGE:
            forward_back.addstr(0, menu_width // 2 - len(middle) // 2, middle)
            if page > 0:
                forward_back.addstr(0, 0, back, curses.color_pair(3))
            if page < len(self.menu_items[1]) // Menu.ITEMS_PER_PAGE:
                forward_back.addstr(0, menu_width - len(back) - 1, forward, curses.color_pair(3))

        forward_back.refresh()

    def print_menu_title(self):
        menu_title_data = self.menu_items[0]
        if isinstance(menu_title_data, tuple):
            main_title = menu_title_data[0]
            additional_title = menu_title_data[1]
        elif isinstance(menu_title_data, str):
            main_title = menu_title_data
            additional_title = ''
        else:
            raise Exception('Ошибка: неверный тип данных для заголовка меню')

        height, width = self.stdscr.getmaxyx()
        menu_width = width
        menu_y = height // 2 - 6
        menu_x = 0
        menu_title = curses.newwin(3, menu_width, menu_y, menu_x)
        menu_title.bkgd(curses.color_pair(1))

        menu_title.addstr(0, menu_width // 2 - len(main_title) // 2, main_title, curses.color_pair(3))
        menu_title.addstr(1, menu_width // 2 - len(main_title) // 2, ('‾' * len(main_title)))

        if additional_title:
            menu_title.addstr(2, menu_width // 2 - len(additional_title) // 2, additional_title, curses.color_pair(4))

        menu_title.refresh()

    def go_back(self):
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            self.menu_items = self.menu_stack[-1]

    def add_menu(self, menu: list):
        self.menu_stack.append(menu)
        self.menu_items = self.menu_stack[-1]

    def load_file(self):
        file_list = controller.get_json_files()
        all_notebooks = ['Все записные книжки', []]
        if len(file_list) == 0:
            self.errors_list.append('Не найдено ни одной записной книжки')
        else:
            all_notebooks[1] += [(x, (self.open_notebook, x)) for x in file_list]

        all_notebooks[1] += [('Назад', self.go_back)]
        self.add_menu(all_notebooks)

    def print_errors(self):
        if len(self.errors_list) == 1:
            text = str(self.errors_list.pop())
            self.errors.clear()
            self.errors.addstr(1, 0, text)
            self.errors.refresh()
        elif len(self.errors_list) > 1:
            text = str(self.errors_list.pop())
            self.errors.clear()
            self.errors.addstr(0, 0, text)
            self.errors.addstr(1, 0, 'Нажмите любую клавишу чтобы продолжить...')
            self.errors.refresh()

    def open_notebook(self, filename: str):
        controller.load_notebook(filename)
        self.add_menu([f'{filename}',
                       [('Создать заметку', self.note_creation_menu),
                        ('Показать все заметки (сортировка по ID)', self.show_all_notes),
                        ('Показать все заметки (сортировка по дате)', (self.show_all_notes, 'updated_at')),
                        ('Сохранить файл', self.save_file),
                        ('',),
                        ('Назад', self.go_back)]])

    def show_all_notes(self, sorting_key=None):
        notes_list = controller.get_all_notes(sorting_key)
        additional_title = 'id'.ljust(4) + \
                           'дата изменения'.ljust(22) + \
                           'заголовок'.ljust(22)
        all_notes = [('Все записи', additional_title), []]
        if len(notes_list) == 0:
            self.errors_list.append('Не найдено ни одной записи')
        else:
            all_notes[1] += [(str(note), (self.open_note, note)) for note in notes_list]
            all_notes[1] += [('Назад', self.go_back)]
            self.add_menu(all_notes)

    def open_note(self, note):
        self.stdscr.clear()
        self.stdscr.refresh()
        height, width = self.stdscr.getmaxyx()

        left_side = curses.newwin(5, width // 2, height // 2 - 2, 0)
        left_side.addstr(0, 0, 'id:'.rjust(width // 2), curses.color_pair(2))
        left_side.addstr(1, 0, 'Заголовок:'.rjust(width // 2), curses.color_pair(2))
        left_side.addstr(2, 0, 'Дата и время изменения:'.rjust(width // 2), curses.color_pair(2))
        left_side.addstr(3, 0, f'Текст:'.rjust(width // 2), curses.color_pair(2))

        right_side = curses.newwin(height, width // 2, 0, width // 2)
        right_side.bkgd(curses.color_pair(1))
        right_side.addstr(height // 2 - 2, 0, str(note.id))
        right_side.addstr(height // 2 - 1, 0, str(note.title))
        right_side.addstr(height // 2, 0, str(note.updated_at))
        right_side.addstr(height // 2 + 1, 0, str(note.body))

        left_side.refresh()
        right_side.refresh()

        right_side.keypad(True)
        user_input = str(note.body)
        while True:
            self.errors_list.append('Esc для возврата, Delete для удаления заметки')
            self.print_errors()

            key = right_side.getch()
            if key == 27:  # Esc
                if note.body != user_input:
                    controller.update(note, body=user_input)
                break
            elif key in (curses.KEY_DC, 46):  # Delete
                try:
                    controller.delete_note(note)
                    self.go_back()
                    self.show_all_notes()
                    self.errors_list.append('Заметка удалена')
                    break
                except Exception as e:
                    self.errors_list.append(str(e))

    def save_file(self):
        try:
            controller.save_file()
            self.errors_list.append('Файл успешно сохранен!')
        except Exception as e:
            self.errors_list.append(str(e))

    def input_menu(self, title: str):
        # Очищаем экран
        self.stdscr.clear()

        # Получаем размеры окна
        height, width = self.stdscr.getmaxyx()

        # Отображаем заголовок
        self.stdscr.addstr(height // 2, 0, title.rjust(width // 2), curses.color_pair(2))
        self.stdscr.refresh()

        # Создаем поле для ввода
        input_field = curses.newwin(1, width // 2, height // 2, width // 2)
        input_field.addstr(0, 0, "")
        input_field.refresh()

        # Получаем введенные данные из поля для ввода
        curses.echo()
        curses.curs_set(1)
        input_field.keypad(True)
        user_input = ""
        while True:
            self.errors_list.append('(Enter для подтверждения, Esc для отмены)')
            self.print_errors()
            key = input_field.getch()
            if key == curses.KEY_ENTER or key == 10:  # Enter
                try:
                    curses.noecho()
                    curses.curs_set(0)
                    return user_input
                except Exception as e:
                    self.errors.addstr(0, 0, str(e))
                    self.errors.refresh()
            elif key == 27:  # Esc
                curses.noecho()
                curses.curs_set(0)
                break
            elif key == curses.KEY_LEFT:
                y, x = input_field.getyx()
                input_field.move(y, max(0, x - 1))
            elif key == curses.KEY_RIGHT:
                y, x = input_field.getyx()
                input_field.move(y, min(len(user_input), x + 1))
            elif key == curses.KEY_BACKSPACE or key == ord('\b'):  # Backspace
                y, x = input_field.getyx()
                input_field.delch(y, x)
                user_input = user_input[:-1]
            elif key == curses.KEY_DC:
                y, x = input_field.getyx()
                input_field.delch(y, x)
                user_input = user_input[:x] + user_input[x + 1:]
            else:
                user_input += chr(key)

    def note_creation_menu(self):
        note_title = self.input_menu('Введите заголовок:')
        note_body = self.input_menu('Введите текст заметки:')
        try:
            controller.add_new_note(note_title, note_body)
            self.errors_list.append('Заметка добавлена')
        except Exception as e:
            self.errors_list.append(str(e))

    def notebook_creation_menu(self):
        file_name = self.input_menu('Введите название для новой записной книжки:')
        if file_name:
            try:
                controller.create_new_notebook(file_name)
                self.errors_list.append(f'Новая записная книжка {file_name} создана')
            except Exception as e:
                self.errors_list.append(str(e))

    def about(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        self.stdscr.addstr(height // 2 - 3, 0, 'Автор: Александр Аношкин aka YodaXD'.center(width))
        self.stdscr.addstr(height // 2 - 1, 0, 'Данная программа является моим пет - проектом'.center(width))
        self.stdscr.addstr(height // 2 + 0, 0, 'в рамках промежуточной контрольной работы'.center(width))
        self.stdscr.addstr(height // 2 + 1, 0, 'по блоку "специализация" в GeekBrains'.center(width))
        self.stdscr.addstr(height // 2 + 3, 0, '(Нажмите любую клавишу для возврата)'.center(width))
        self.stdscr.refresh()
        self.stdscr.getch()


def run():
    start_menu = Menu()
    start_menu_items = ['Главное меню',
                        [('Новая записная книжка', start_menu.notebook_creation_menu),
                         ('Загрузить', start_menu.load_file),
                         ('Об авторе', start_menu.about),
                         ('',),
                         ('Выход', exit)]]

    start_menu.add_menu(start_menu_items)
    curses.wrapper(start_menu.main)


run()
