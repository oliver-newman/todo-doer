from .todo_list import TodoList


if __name__ == '__main__':
    todo_list = TodoList(filename='../TODO.md')
    print(todo_list)
    import pdb; pdb.set_trace()
    todo_list.save()
