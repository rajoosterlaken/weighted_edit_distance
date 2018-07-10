from collections import Counter


class OperationOccurrenceCounter(object):
    def __init__(self):
        self.data = {}


    def create_path(self, operation_type, chars):
        if operation_type not in self.data:
            self.data[operation_type] = {}
            
        if chars not in self.data[operation_type]:
            self.data[operation_type][chars] = Counter()


    def add(self, operation_type, chars, context, value):
        self.create_path(operation_type, chars)
        self.data[operation_type][chars][context] += value


    def get(self, operation_type, chars, context):
        if operation_type not in self.data:
            return 0
        
        if chars not in self.data[operation_type]:
            return 0

        return self.data[operation_type][chars][context]
