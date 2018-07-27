def parse_matrix(file):
    raw_lines = open(file).read()
    raw_matrices = raw_lines.split('#')

    inputs = []

    for i in raw_matrices:
        matrix_range = list(filter(('').__ne__, i.split('\n')))
        matrix = []

        for row in matrix_range[:-1]:
            matrix.append([ int(i) for i in row.split(',') ])

        num_range = [ int(i) for i in matrix_range[-1].split('-') ]

        inputs.append((matrix, num_range))

    return inputs
