from edit_distance import optimal_string_alignment_distance as osa
from path_tracer import PathTracer
from os import makedirs
from os.path import sep
from path_collapser import collapse_path

header_command = "\\matrixheader"
cell_command = "\\matrixcell"
result_command = "\\matrixresult"
path_command = "\\matrixpath"
output_folder = ".." + sep + "latex" + sep


def to_latex_string(latex_matrix_cell):
    value, command = latex_matrix_cell
    return command + "{" + str(value) + "}"


def create_file(latex_matrix, source, target):
    makedirs(output_folder, exist_ok=True)
    latex_file_path = output_folder + "osa_" + source.lower() + "_" + target.lower() + ".tex"
    with open(latex_file_path, "w") as latex_file:
        latex_file.write("\\begin{figure}\n")
        latex_file.write("    \\ttfamily\n")
        latex_file.write("    \\centering\n")
        latex_file.write("    \\small\n")
        column_definitions = "|" + "|".join("c" * len(latex_matrix[0])) + "|"
        latex_file.write("    \\begin{tabular}{" + column_definitions + "}\n        \\hline\n")
        for row_index in range(len(latex_matrix)):
            row = map(to_latex_string, latex_matrix[row_index])
            line = "        " + " & ".join(row) + " \\\\ \\hline\n"
            latex_file.write(line)
        latex_file.write("    \\end{tabular}\n")
        source_f = source[0] + "".join([character.lower() for character in source[1:]])
        target_f = target[0] + "".join([character.lower() for character in target[1:]])
        latex_file.write("    \\caption{O.s.a. distance between \\variant{" + source_f + "} and \\variant{" + target_f +"}.}\n")
        latex_file.write("    \\label{fig:osa_" + source.lower() + "_" + target.lower() + "}\n")
        latex_file.write("\\end{figure}")


def transpose(matrix):
    rows, columns = len(matrix), len(matrix[-1])
    transposed_matrix = []
    for j in range(columns):
        transposed_matrix.append([])
        for i in range(rows):
            transposed_matrix[j].append([])
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix


def tag_cells(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        new_matrix.append([])
        for j in range(len(matrix[i])):
            new_matrix[i].append((matrix[i][j], "\\matrixcell"))
    return new_matrix


def tag_matrix(matrix, source, target):
    matrix.insert(0, [(c, header_command) for c in " " + source])
    target = "  " + target
    for i in range(len(matrix)):
        matrix[i].insert(0, (target[i], header_command))
    return matrix


def paint_paths(tagged_matrix, path_tracer):
    paths = path_tracer.trace()
    
    for m, ppp in enumerate(paths):
        print(f"PATH {m}:")
        for n, op in enumerate(ppp):
            print(f"{n} - {op}")
        print("")
    print("")

    for m, ppp in enumerate(paths):
        print(f"PATH {m}:")
        for n, op in enumerate(collapse_path(ppp)):
            print(f"{n} - {op}")
        print("")


    positions = {operation.position for p in paths for operation in p}
    positions.add((0,0))
    positions.add((1,1))
    for i in range(len(tagged_matrix)):
        for j in range(len(tagged_matrix[i])):
            if (i,j) in positions:
                tagged_matrix[i][j] = (tagged_matrix[i][j][0], path_command)
    tagged_matrix[-1][-1] = (tagged_matrix[-1][-1][0], result_command)


if __name__ == '__main__':
    source, target = "BARTHOLOMEE", "MEEUWIS"
    matrix = osa(source, target)
    tagged_matrix = tag_cells(matrix)
    path_tracer = PathTracer(matrix, source, target)
    paint_paths(tagged_matrix, path_tracer)
    transposed_matrix = transpose(tagged_matrix)
    latex_matrix = tag_matrix(transposed_matrix, source, target)
    create_file(latex_matrix, source, target)