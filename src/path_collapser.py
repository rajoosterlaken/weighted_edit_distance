from edit_distance import optimal_string_alignment_distance as osa
from operations import Deletion, Insertion, Substitution, Match, Transposition
from path_tracer import PathTracer


def combine_operations(operations):
    if operations:
        combination = operations[0]
        for i in range(1, len(operations[1:]) + 1):
            combination = combination.extend(operations[i])
        return combination


def split_path(path, seperator=Match):
    splits = []
    current_split = []
    for operation in path:
        if type(operation) == seperator:
            if current_split:
               splits.append(current_split)
            splits.append([operation])
            current_split = []
        else:
            current_split.append(operation)
    
    if current_split:
        splits.append(current_split)

    return splits


def collapse_path(path):
    new_path = []
    splitted_path = split_path(path)
    for split in splitted_path:
        new_operation = combine_operations(split)
        new_path.append(new_operation)
    return new_path
