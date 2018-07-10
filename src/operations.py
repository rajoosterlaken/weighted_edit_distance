class Operation(object):
    def __init__(self, chars, source_context, target_context):
        self.chars = chars
        self.source_context = source_context
        self.target_context = target_context

    def __repr__(self):
        return f"{type(self).__name__}(chars = {self.chars}, src_context = {self.source_context})"

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        full_tuple_hash = hash((self.chars, self.source_context[0], self.source_context[1]))
        return full_tuple_hash

    def extend(self, operation):
        if type(operation) == Deletion:
            return self.extend_with_deletion(operation)
        elif type(operation) == Insertion:
            return self.extend_with_insertion(operation)
        elif type(operation) == Substitution:
            return self.extend_with_substitution(operation)
        elif type(operation) == Transposition:
            return self.extend_with_transposition(operation)
        elif type(operation) == Match:
            return operation
        else:
            print(f"Could not find the operation type for {operation}.")
            return operation

    def extend_with_deletion(self, operation):
        print(f"Method 'extend_with_deletion' not implemented!")

    def extend_with_insertion(self, operation):
        print(f"Method 'extend_with_insertion' not implemented!")

    def extend_with_substitution(self, operation):
        print(f"Method 'extend_with_substitution' not implemented!")

    def extend_with_transposition(self, operation):
        print(f"Method 'extend_with_transposition' not implemented!")


class Deletion(Operation):
    def __init__(self, chars, source_context, target_context):
        super().__init__(chars, source_context, target_context)

    def extend_with_deletion(self, deletion):
        chars = self.chars + deletion.chars
        source_context = self.source_context[0], deletion.source_context[1]
        target_context = self.target_context[0], deletion.target_context[1]
        return Deletion(chars, source_context, target_context)

    def extend_with_insertion(self, insertion):
        chars = self.chars, insertion.chars
        source_context = self.source_context[0], insertion.source_context[1]
        target_context = self.target_context[0], insertion.target_context[1]
        return Substitution(chars, source_context, target_context)

    def extend_with_substitution(self, substitution):
        chars = self.chars + substitution.chars[0], substitution.chars[1]
        source_context = self.source_context[0], substitution.source_context[1]
        target_context = self.target_context[0], substitution.target_context[1]
        return Substitution(chars, source_context, target_context)

    def extend_with_transposition(self, transposition):
        chars = self.chars + transposition.chars, transposition.chars[::-1]
        source_context = self.source_context[0], transposition.source_context[1]
        target_context = self.target_context[0], transposition.target_context[1]
        return Substitution(chars, source_context, target_context)


class Insertion(Operation):
    def __init__(self, chars, source_context, target_context):
        super().__init__(chars, source_context, target_context)

    def extend_with_deletion(self, deletion):
        chars = self.chars, deletion.chars
        source_context = self.source_context[0], deletion.source_context[1]
        target_context = self.target_context[0], deletion.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_insertion(self, insertion):
        chars = self.chars + insertion.chars
        source_context = self.source_context[0], insertion.source_context[1]
        target_context = self.target_context[0], insertion.target_context[1]
        return Insertion(chars, source_context, target_context)
        
    def extend_with_substitution(self, substitution):
        chars = substitution.chars[0], self.chars + substitution.chars[1]
        source_context = self.source_context[0], substitution.source_context[1]
        target_context = self.target_context[0], substitution.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_transposition(self, transposition):
        chars = transposition.chars, self.chars + transposition.chars[::-1]
        source_context = self.source_context[0], transposition.source_context[1]
        target_context = self.target_context[0], transposition.target_context[1]
        return Substitution(chars, source_context, target_context)


class Match(Operation):
    def __init__(self, chars, source_context, target_context):
        super().__init__(chars, source_context, target_context)


class Substitution(Operation):
    def __init__(self, chars, source_context, target_context):
        super().__init__(chars, source_context, target_context)

    def extend_with_deletion(self, deletion):
        chars = self.chars[0] + deletion.chars, self.chars[1]
        source_context = self.source_context[0], deletion.source_context[1]
        target_context = self.target_context[0], deletion.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_insertion(self, insertion):
        chars = self.chars[0], self.chars[1] + insertion.chars
        source_context = self.source_context[0], insertion.source_context[1]
        target_context = self.target_context[0], insertion.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_substitution(self, substitution):
        chars = self.chars[0] + substitution.chars[0], self.chars[1] + substitution.chars[1]
        source_context = self.source_context[0], substitution.source_context[1]
        target_context = self.target_context[0], substitution.target_context[1]
        return Substitution(chars, source_context, target_context)

    def extend_with_transposition(self, transposition):
        chars = self.chars[0] + transposition.chars, self.chars[1] + transposition.chars[::-1]
        source_context = self.source_context[0], transposition.source_context[1]
        target_context = self.target_context[0], transposition.target_context[1]
        return Substitution(chars, source_context, target_context)


class Transposition(Operation):
    def __init__(self, chars, source_context, target_context):
        super().__init__(chars, source_context, target_context)

    def extend_with_deletion(self, deletion):
        chars = self.chars + deletion.chars, self.chars[::-1]
        source_context = self.source_context[0], deletion.source_context[1]
        target_context = self.target_context[0], deletion.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_insertion(self, insertion):
        chars = self.chars, self.chars[::-1] + insertion.chars
        source_context = self.source_context[0], insertion.source_context[1]
        target_context = self.target_context[0], insertion.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_substitution(self, substitution):
        chars = self.chars + substitution.chars[0], self.chars + substitution.chars[1]
        source_context = self.source_context[0], substitution.source_context[1]
        target_context = self.target_context[0], substitution.target_context[1]
        return Substitution(chars, source_context, target_context)
        
    def extend_with_transposition(self, transposition):
        chars = self.chars + transposition.chars, self.chars[::-1] + transposition.chars[::-1]
        source_context = self.source_context[0], transposition.source_context[1]
        target_context = self.target_context[0], transposition.target_context[1]
        return Substitution(chars, source_context, target_context)
