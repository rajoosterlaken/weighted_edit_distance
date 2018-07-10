from cost_model import CostModel
from models.name_pairs import FirstNamePair, LastNamePair
from os import makedirs, listdir, sep
from os.path import isdir, isfile, join
from files.csv_processor import CsvProcessor
from files.timestamp import generate_timestamp
from pickle import dump, load
import sys
from operations import Deletion, Insertion, Substitution, Transposition


def get_input_file_paths(input_folder_path=f"..{sep}input"):
    input_file_paths = []
    for input_file_name in listdir(input_folder_path):
        input_file_path = input_folder_path + sep + input_file_name
        if isfile(input_folder_path + sep + input_file_name):
            input_file_paths.append(input_file_path)
            print(f"[INPUT] Added '{input_file_path}' to input paths.")
    return input_file_paths


def generate_output_folder():
    timestamp = generate_timestamp()
    output_folder_path = f"..{sep}output{sep}{timestamp}"
    if not isdir(output_folder_path):
        makedirs(output_folder_path, exist_ok=True)
    print(f"[OUTPUT] Created output folder: {output_folder_path}")
    return output_folder_path


def filter_pickle_folder_path():
    pickle_folder_path = None
    for arg in sys.argv[1:]:
        if isdir(arg):
            file_names = listdir(arg)
            if all([name[-4:] == ".pkl" for name in file_names]):
                pickle_folder_path = arg
                break
    return pickle_folder_path


def get_name_pair_class(input_file_path):
    name_pair_class_dict = {"first_name": FirstNamePair, "last_name": LastNamePair}
    for key in name_pair_class_dict:
        if key in input_file_path:
            return name_pair_class_dict[key]
    return None


def create_model(csv_processor, input_file_path):
    name_pair_class = get_name_pair_class(input_file_path)
    if not name_pair_class:
        return None
    model = CostModel(name_pair_class, csv_processor, input_file_path)
    model.train()
    return model


def pickle_model(model, pickle_file_path):
    with open(pickle_file_path, mode="wb") as pickle_file:
        dump(model, pickle_file)


def create_models(models, csv_processor, output_folder_path):
    input_file_paths = get_input_file_paths()

    for input_file_path in input_file_paths:
        model_name = input_file_path.split(sep)[-1][:-4]

        print(f"[MAIN] Creating cost model '{model_name}'")
        models[model_name] = create_model(csv_processor, input_file_path)
        print("[MAIN] Cost model created")

        print(f"[MAIN] Pickling cost model '{model_name}'")
        pickle_model(models[model_name], join(output_folder_path, f"{model_name}.pkl"))
        print(f"[MAIN] Pickle created.")


def load_models(pickle_folder_path, models):
    print(f"[MAIN] len(models) models from pickles at '{pickle_folder_path}' loaded")
    for file_name in listdir(pickle_folder_path):
        model_name = file_name[:-4]
        print(f"[MAIN] Loading pickled model '{model_name}'")
        with open(join(pickle_folder_path, file_name), mode="rb") as pickle_file:
            models[model_name] = load(pickle_file)


def init_models(csv_processor, output_folder_path):
    models = {}
    pickles_loaded = False
    if len(sys.argv) > 1:
        print(f"[MAIN] Attempting pickle folder load...")
        pickle_folder_path = filter_pickle_folder_path()
        if pickle_folder_path:
            load_models(pickle_folder_path, models)
            pickles_loaded = True
        else:
            print(f"[MAIN] Pickle folder deemed invalid; creating models instead")
    if not pickles_loaded:
        create_models(models, csv_processor, output_folder_path)
    return models


def print_loading_bar(message, processed, total):
    chars_percentage_processed = processed / total
    completion_data = f"{processed} / {total} ({chars_percentage_processed:.2%})"
    bar_pieces = int(chars_percentage_processed * 10)
    loading_bar = "#" * bar_pieces + "_" * (10 - bar_pieces)
    end_token = "\n" if processed == total else ""
    print(f"[MAIN] - {message}: [{loading_bar}] {completion_data}\r", end=end_token)


def build_context_key(operation_type, chars, context):
    if operation_type == Insertion:
        return context[0] + context[1]
    elif operation_type == Deletion:
        return context[0] + chars + context[1]
    elif operation_type == Substitution:
        return context[0] + chars[0] + context[1]
    elif operation_type == Transposition:
        return context[0] + chars + context[1]
    else:
        return "???"


def add_fraction_row(model, operation_type, chars, context):
    operation_occurrences = model.operation_occurrence_counter.get(operation_type, chars, context)
    substring_key = build_context_key(operation_type, chars, context)  # context[0] + (chars if type(chars) != tuple else chars[0]) + context[1]
    context_references = model.substring_reference_counter[substring_key]
    if context_references == 0:
        print(f"[{operation_type}][{chars}][{context}] -> substring = {substring_key}")
        return [chars, context, operation_occurrences, context_references, 0]
    fraction = operation_occurrences / context_references
    if operation_occurrences / context_references > 1.0:
        print(f"[Fraction would have been higher than 1 ({fraction})] {operation_type} {chars} {context}")
    capped_fraction = min(max(fraction, 0.0), 1.0)
    return [chars, context, operation_occurrences, context_references, capped_fraction]


def sort_rows(rows):
    sorted_rows = sorted(rows, key=lambda row: row[4], reverse=True)
    return sorted_rows


def create_top_100s(models, csv_processor, output_folder_path):
    for model_name in models:
        print(f"[MAIN] Creating counts for the '{model_name}' model:")
        model = models[model_name]
        for operation_type in model.operation_occurrence_counter.data:
            operation_name = operation_type.__name__
            rows = []
            entries_done, entries_total = 0, len(model.operation_occurrence_counter.data[operation_type])
            for chars in model.operation_occurrence_counter.data[operation_type]:
                for context in model.operation_occurrence_counter.data[operation_type][chars]:
                    rows.append(add_fraction_row(model, operation_type, chars, context))
                entries_done += 1
                print_loading_bar(operation_name, entries_done, entries_total)
            file_name = f"{model_name}-{operation_name}-counts.csv"
            output_file_path = join(output_folder_path, file_name)
            csv_processor.write_csv_rows(output_file_path, sort_rows(rows))


def main():
    csv_processor = CsvProcessor()
    output_folder_path = generate_output_folder()

    global models
    models = init_models(csv_processor, output_folder_path)

    create_top_100s(models, csv_processor, output_folder_path)


def unique_name_pairs(model):
    not_found = []
    deleted = 0
    i = 1
    for name_pair1 in model.name_pairs:
        v1, v2 = name_pair1.variant1, name_pair1.variant2
        pair_tuple = (v1,v2) if v1<v2 else (v2,v1)
        if pair_tuple not in not_found:
            not_found.append(pair_tuple)
        else:
            tuple_index = not_found.index(pair_tuple)
            del not_found[tuple_index]
            deleted += 1
        print(f"{i} - len: {len(not_found)} - dels: {deleted}          \r", end="")
        i += 1
    return not_found


if __name__ == '__main__':
    main()
