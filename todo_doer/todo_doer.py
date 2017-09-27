import sys
import argparse
import inspect


def main():
    todo_list = _init_from_file('../TODO.md')
    parser = get_parser()
    args = parser.parse_args()
    print(sys.argv)
    todo_list.save()


def get_parser():
    parser = argparse.ArgumentParser(
        prog='tododoer',
        description='manage your project todos pain-free')

    todo_list_methods = [getattr(TodoList, func) for func in dir(TodoList)
                         if callable(getattr(TodoList, func))
                         and not func.startswith('_')]
    subparsers = parser.add_subparsers()

    for method in todo_list_methods:
        subparser = subparsers.add_parser(method.__name__,
                                          help=inspect.getdoc(method))
        for param_name, param in inspect.signature(method).parameters.keys():
            if param_name == 'self':
                continue
            subparser.add_argument(param_name, type=param.annotation)

    return parser


def _print(todo_list):
    return '\n'.join('{0}. {1}'.format(number, str(item))
            for number, item in todo_list._enumerate())


def _print_raw(todo_list):
    return '\n'.join('{0}. {1}'.format(number, repr(item))
            for number, item in todo_list._enumerate())


def _init_from_file(filename):
    todo_list = []
    with open(filename) as todo_file:
        line = todo_file.readline().strip()
        while line:
            todo_regex = '^- \[(?P<checkbox>[\ x])\] (?P<todo_item>.+)$'
            todo_regex_match = re.match(todo_regex, line)
            if todo_regex_match:
                todo_text = todo_regex_match.group('todo_item')
                completed = (todo_regex_match.group('checkbox') == 'x')
                todo_list.append(TodoItem(todo_text, completed))
            else:
                # line is not a valid todo item
                pass
            line = todo_file.readline().strip()
    return todo_list


def _save_to_file(todo_list, filename=None):
    filename = filename if filename else todo_list.filename
    with open(filename, 'w') as todo_file:
        for item in todo_list:
            todo_file.write('- {}\n'.format(repr(item)))


def _enumerate(todo_list):
    for index, item in enumerate(todo_list):
        yield (index + 1, item)


def add(todo_list, todo_text: str, completed: bool = False, number: int = -1):
    new_item = TodoItem(todo_text, completed)
    if number > 0:
        todo_list.insert(number - 1, new_item)
    else:
        todo_list.append(new_item)


def do(todo_list, number: int):
    todo_list[number - 1].completed = True


def undo(todo_list, number: int):
    todo_list[number - 1].completed = False


def delete(todo_list, number: int):
    todo_list.pop(number - 1)


def search(todo_list, search_string: str = '', include_completed: bool = True):
    for number, item in _enumerate(todo_list):
        if ((not item.completed or include_completed)
            and search_string in item.text):
            yield (number, item)


if __name__ == '__main__':
    main()
