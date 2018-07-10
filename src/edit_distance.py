from copy import copy


default_costs = {"insertion": 1, "deletion": 1, "substitution": 1, "transposition": 1}


def create_matrix(m, n, costs):
    matrix = [[0 for _ in range(0, n)] for _ in range(0, m)]
    for i in range(0, m):
        matrix[i][0] = i * costs["deletion"]
    for j in range(0, n):
        matrix[0][j] = j * costs["insertion"]
    return matrix


def optimal_string_alignment_distance(source, target, costs=None):
    if costs == None:
        costs = default_costs

    matrix = create_matrix(len(source) + 1, len(target) + 1, costs)

    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):
            ops = [matrix[i-1][j] + costs["deletion"]]
            ops.append(matrix[i][j-1] + costs["insertion"])
            ops.append(matrix[i-1][j-1])

            char_s, char_t = source[i-1], target[j-1]
            if char_s != char_t:
                ops[2] += costs["substitution"]
            
            if i > 1 and j > 1:
                prev_char_s, prev_char_t = source[i-2], target[j-2]
                if char_s == prev_char_t and char_t == prev_char_s:
                    ops.append(matrix[i-2][j-2] + costs["transposition"])
            
            matrix[i][j] = min(ops)
    
    return matrix
