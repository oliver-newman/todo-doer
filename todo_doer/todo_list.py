import sys
import re


def checkbox_symbol(with_check):
    return u'\u2713' if with_check else u'\u25FB'


class TodoItem:
    def __init__(self, text, completed=False):
        self.text = text
        self.completed = completed

    def __str__(self):
        return '{0} {1}'.format(checkbox_symbol(self.completed), self.text)

    def __repr__(self):
        return '[{0}] {1}'.format('x' if self.completed else ' ', self.text)


class TodoList:
    def __init__(self, todos=None, from_file=True, filename='TODO.md'):
        self.items = []
        self.filename = filename
        if from_file:
            self.init_from_file(filename)

    def __str__(self):
        return '\n'.join('{0}. {1}'.format(index, str(item))
                for index, item in self.enumerate_items())

    def __repr__(self):
        return '\n'.join('{0}. {1}'.format(index, repr(item))
                for index, item in self.enumerate_items())

    def init_from_file(self, filename):
        with open(filename) as todo_file:
            line = todo_file.readline().strip()
            while line:
                todo_regex = '^- \[(?P<checkbox>[\ x])\] (?P<todo_item>.+)$'
                todo_regex_match = re.match(todo_regex, line)
                if todo_regex_match:
                    todo_text = todo_regex_match.group('todo_item')
                    completed = (todo_regex_match.group('checkbox') == 'x')
                    self.items.append(TodoItem(todo_text, completed))
                else:
                    # line is not a valid todo item
                    pass
                line = todo_file.readline().strip()

    def add(self, todo_text, completed=False, number=-1):
        new_item = TodoItem(todo_text, completed)
        if number > 0:
            self.items.insert(number - 1, new_item)
        else:
            self.items.append(new_item)

    def do(self, index):
        self.items[index - 1].completed = True

    def undo(self, index):
        self.items[index - 1].completed = False

    def delete(self, index):
        self.items.pop(index - 1)

    def search(self, search_string='', include_completed=True):
        for number, item in self.enumerate_items():
            if ((not item.completed or include_completed)
                and search_string in item.text):
                yield (number, item)

    def enumerate_items(self):
        for index, item in enumerate(self.items):
            yield (index + 1, item)

    def save(self, filename=None):
        filename = filename if filename else self.filename
        with open(filename, 'w') as todo_file:
            for item in self.items:
                todo_file.write('- {}\n'.format(repr(item)))
