from collections import Counter
from edit_distance import optimal_string_alignment_distance
from models.timer import Timer
from operations import Match
from path_collapser import collapse_path
from path_tracer import PathTracer
from operation_occurrence_counter import OperationOccurrenceCounter
from string import punctuation, digits
from operations import Transposition

class CostModel(object):

    # =============
    # Setup Section
    # =============
    def __init__(self, name_pair_class, csv_processor, input_file_path):
        self.timer = Timer()
        self.name_pair_class = name_pair_class
        self.invalid_characters = punctuation + digits
        self.invalid_name_pair_rows = 0
        self.normalized_pairs = 0
        self.equivalent_variants = 0
        name_pair_mapping = csv_processor.map_to_csv(input_file_path, self.convert_row_to_name_pair)
        self.name_pairs = list(filter(None, name_pair_mapping))
        self.operation_occurrence_counter = OperationOccurrenceCounter()
        self.substring_reference_counter = Counter()
        self.max_substring_length = 2
        self.max_substring_str = []
        print(f"[CM] Cost model initialized: {len(self.name_pairs)} name pairs loaded ({self.invalid_name_pair_rows} invalid | {self.normalized_pairs} normalized | {self.equivalent_variants} equal).")


    def is_invalid_name_pair(self, name_pair):
        is_variant1_invalid = any(map(lambda c: c in self.invalid_characters, name_pair.variant1))
        is_variant2_invalid = any(map(lambda c: c in self.invalid_characters, name_pair.variant2))
        return is_variant1_invalid or is_variant2_invalid


    def convert_row_to_name_pair(self, row):
        name_pair = self.name_pair_class(*row)
        if self.is_invalid_name_pair(name_pair):
            self.invalid_name_pair_rows += 1
            return None
        if name_pair.altered_variant1 or name_pair.altered_variant2:
            self.normalized_pairs += 1
        if name_pair.variant1 == name_pair.variant2:
            self.equivalent_variants += 1
        return name_pair


    def count_operation_occurrences(self, name_pair):
        source, target = name_pair.variant1, name_pair.variant2
        pair_occurrences = name_pair.n_paar
        matrix = optimal_string_alignment_distance(source, target)
        shortest_paths = PathTracer(matrix, source, target).trace()
        for path in shortest_paths:
            collapsed_path = collapse_path(path)
            seen_operations = set()
            for operation in filter(lambda operation: type(operation) != Match, collapsed_path):
                if operation not in seen_operations:
                    chars = operation.chars
                    reference_lookup_length = len(chars[0]) + 2 if type(chars) == tuple else len(chars) + 2
                    context = operation.source_context
                    if reference_lookup_length >= self.max_substring_length:
                        if reference_lookup_length > self.max_substring_length and len(self.max_substring_str) > 0:
                            self.max_substring_str = []
                        maxstring = context[0] + (chars[0] if type(chars) == tuple else chars) + context[1]
                        self.max_substring_str.append(maxstring)
                        self.max_substring_length = reference_lookup_length
                    value = pair_occurrences / len(shortest_paths)
                    self.operation_occurrence_counter.add(type(operation), chars, context, value)
                    seen_operations.add(operation)



    def count_substring_references(self, name_pair, variant_attribute_name="variant1"):
        padded_name = "#" + getattr(name_pair, variant_attribute_name) + "#"
        pair_occurrences = name_pair.n_paar
        for size in range(2, self.max_substring_length + 1):
            substrings = [padded_name[i:i + size] for i in range(len(padded_name) - size + 1)]
            for substring in filter(lambda s: len(s) == size, substrings):
                self.substring_reference_counter[substring] += pair_occurrences


    def map_to_name_pairs(self, function, description):
        name_pairs_processed = 0
        total_name_pairs = len(self.name_pairs)
        name_pair_number_length = len(str(len(self.name_pairs)))
        for name_pair in self.name_pairs:
            function(name_pair)
            name_pairs_processed += 1
            processed_out_of_total = f"{name_pairs_processed:0>{name_pair_number_length}} / {total_name_pairs}"
            fraction_processed = name_pairs_processed / total_name_pairs
            n_loading_bar_pieces = int(fraction_processed * 10)
            loading_bar = ("#" * n_loading_bar_pieces) + ("=" * (10 - n_loading_bar_pieces))
            end_token = "\n" if name_pairs_processed == len(self.name_pairs) else ""
            print(f"[CM] {description}: [{loading_bar}] {processed_out_of_total} ({fraction_processed:.2%})\r", end=end_token)


    def train(self):
        print(f"[CM] Training costs model")
        self.timer.start()

        self.map_to_name_pairs(self.count_operation_occurrences, "Counting operation occurrences")
        print(f"[CM] Maximum substring reference length needed: {self.max_substring_length}")
        self.map_to_name_pairs(self.count_substring_references, "Counting substring references")

        minutes_spend, seconds_spend = self.timer.stop(reset=True)
        print(f"[CM] Training completed ({minutes_spend}min {seconds_spend}sec)")
