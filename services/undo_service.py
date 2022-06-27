class UndoService:
    def __init__(self):
        # History of operations for undo/redo
        self.__history = []
        # Our current position in undo/redo
        self.__index = -1
        # Setting this to false stops recording operations for undo/redo
        self.__record_flag = True

    def set_record_flag(self, record_flag):
        self.__record_flag = record_flag

    def record_operation(self, operation):
        if self.__record_flag is False:
            return

        # Remove every possible redo
        self.__history = self.__history[0: self.__index + 1]

        # Add the new operation
        self.__history.append(operation)
        self.__index += 1

    def undo(self):
        self.__record_flag = False

        if self.__index >= 0:
            self.__history[self.__index].undo()
            self.__index -= 1
        else:
            raise UndoException('You cannot undo anymore!')

        self.__record_flag = True

    def redo(self):
        self.__record_flag = False

        if self.__index < len(self.__history) - 1:
            self.__index += 1
            self.__history[self.__index].redo()
        else:
            raise UndoException('You cannot redo anymore!')

        self.__record_flag = True


class Operation:
    def __init__(self, function_undo, function_redo):
        self.__function_undo = function_undo
        self.__function_redo = function_redo

    def undo(self):
        self.__function_undo.call()

    def redo(self):
        self.__function_redo.call()


class CascadedOperation:
    def __init__(self):
        self.__operations = []

    def add(self, operation):
        self.__operations.append(operation)

    def undo(self):
        for operation in self.__operations:
            operation.undo()

    def redo(self):
        for operation in self.__operations:
            operation.redo()


class FunctionCall:
    def __init__(self, function_name, *function_params):
        self.__function_name = function_name
        self.__function_params = function_params

    def call(self):
        self.__function_name(*self.__function_params)


class UndoException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "You cannot perform this operation again!"

    def __str__(self):
        return self.message
