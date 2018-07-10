from copy import copy
from edit_distance import default_costs
from queue import Queue
from operations import Deletion, Insertion, Match, Substitution, Transposition


class PathTracer(object):

    def __init__(self, matrix, source, target, costs=None):
        self.paths = []
        self.paths_to_process = Queue()
        self.matrix = matrix
        self.source = source
        self.target = target
        self.costs = costs if costs else default_costs
        self.reset_head()


    def reset_head(self):
        self.i = len(self.matrix) - 1
        self.j = len(self.matrix[-1]) - 1


    def move_head(self, operation):
        operation_type = type(operation)
        if operation_type == Deletion:
            self.i -= 1
        elif operation_type == Insertion:
            self.j -= 1
        elif operation_type == Match or operation_type == Substitution:
            self.i -= 1
            self.j -= 1
        elif operation_type == Transposition:
            self.i -= 2
            self.j -= 2


    def get_value(self, i_offset = 0, j_offset = 0):
        return self.matrix[self.i + i_offset][self.j + j_offset]
    

    def char_s(self, index_offset=0):
        index = self.i - 1 + index_offset
        if index < 0 or index >= len(self.source):
            return "#"
        else:
            return self.source[index]


    def char_t(self, index_offset=0):
        index = self.j - 1 + index_offset
        if index < 0 or index >= len(self.target):
            return "#"
        else:
            return self.target[index]


    def deletion_operation(self, value, pos_after, operations):
        if self.i > 0 and self.get_value(-1, 0) + self.costs["deletion"] == value:
            source_context = (self.char_s(-1), self.char_s(1))
            target_context = (self.char_t(), self.char_t(1))
            operation = Deletion(self.char_s(), source_context, target_context)
            operation.position = pos_after
            operations.append(operation)


    def insertion_operation(self, value, pos_after, operations):
        if self.j > 0 and self.get_value(0, -1) + self.costs["insertion"] == value:
            source_context = (self.char_s(), self.char_s(1))
            target_context = (self.char_t(-1), self.char_t(1))
            operation = Insertion(self.char_t(), source_context, target_context)
            operation.position = pos_after
            operations.append(operation)


    def substitution_operation(self, value, pos_after, operations):
        if self.i > 0 and self.j > 0:
            char_s = self.char_s()
            char_t = self.char_t()
            source_context = (self.char_s(-1), self.char_s(1))
            target_context = (self.char_t(-1), self.char_t(1))
            if char_s == char_t and self.get_value(-1, -1) == value:
                operation = Match(char_s, source_context, target_context)
                operation.position = pos_after
                operations.append(operation)
            elif self.get_value(-1, -1) + self.costs["substitution"] == value:
                operation = Substitution((char_s, char_t), source_context, target_context)
                operation.position = pos_after
                operations.append(operation)


    def transposition_operation(self, value, pos_after, operations):
        if self.i > 1 and self.j > 1:
            char_s = self.char_s()
            char_t = self.char_t()
            costs_match = self.get_value(-2, -2) + self.costs["transposition"] == value
            char_swap = char_s == self.target[self.j-2]
            char_swap = char_swap and char_t == self.source[self.i-2]
            if costs_match and char_swap:
                source_context = (self.char_s(-2), self.char_s(1))
                target_context = (self.char_t(-2), self.char_t(1))
                operation = Transposition(char_t + char_s, source_context, target_context)
                operation.position = pos_after
                operations.append(operation)


    def get_possible_operations(self):
        current_value = self.get_value()
        pos_after = (self.i, self.j)
        operations = []
        self.deletion_operation(current_value, pos_after, operations)
        self.insertion_operation(current_value, pos_after, operations)
        self.substitution_operation(current_value, pos_after, operations)
        self.transposition_operation(current_value, pos_after, operations)
        return operations


    def queue_alternate_paths(self, source_path, operations):
        for operation in operations:
            alternate_path = copy(source_path)
            alternate_path.insert(0, operation)
            self.paths_to_process.put(alternate_path)


    def trace_path(self, path):
        if len(path) == 0: 
            raise ValueError(path)

        possible_operations = self.get_possible_operations()
        amount_of_possible_operations = len(possible_operations)
        self.queue_alternate_paths(copy(path), possible_operations[1:])

        if amount_of_possible_operations >= 1:
            first_possible_operation = possible_operations[0]
            path.insert(0, first_possible_operation)
            self.move_head(first_possible_operation)


    def trace(self):
        possible_paths = [[operation] for operation in self.get_possible_operations()]

        for path in possible_paths:
            self.paths_to_process.put(path)

        while not self.paths_to_process.empty():
            current_path = self.paths_to_process.get()

            self.reset_head()
            for operation in current_path:
                self.move_head(operation)
            
            while (self.i, self.j) != (0, 0):
                self.trace_path(current_path)

            self.paths.append(current_path)

        return self.paths


def test(source, target):
    from edit_distance import optimal_string_alignment_distance as osa
    matrix = osa(source, target)
    print(f"{matrix}")
    print(f"edit_distance({source}, {target}) = {matrix[-1][-1]}", end="\n\n")
    tracer = PathTracer(matrix, source, target)
    paths = tracer.trace()
    for path_index, path in enumerate(paths):
        print(f"Path {path_index} for osa({source},{target}):")
        for operation in path:
            print(f"> {operation}")	
        print()


def main():
    test("VEREMANS", "VEERMAN")


if __name__ == '__main__':
    main()
