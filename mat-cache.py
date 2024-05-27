import numpy as np
import time
from functools import lru_cache

start = time.time()
print("The script has started running.")

@lru_cache(maxsize=10000)
def create_matrix(line):
    size = line.split(':')[0]
    x = size.index('x')
    rows = int(size[:x])
    columns = int(size[x + 1:])
    values = line.split(':')[1]
    index = 0
    matrix = [[-1 for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            matrix[i][j] = int(values[index])
            index = index + 1
    matrix = tuple(tuple(rows) for rows in matrix)
    return matrix, rows, columns

@lru_cache(maxsize=10000)
def count_neighboring_ones(matrix, rows, columns):
    def neighbors_coordinates(i, j):
        neighbors = []
        for x in range(max(0, i - 1), min(rows, i + 2)):
            for y in range(max(0, j - 1), min(columns, j + 2)):
                if (x != i or y != j) and matrix[x][y] == 1:
                    neighbors.append((x, y))
        return neighbors

    def mark_as_verified(i, j):
        verified.add((i, j))

    verified = set()
    iso = 0
    iso_clu2 = 0
    iso_clu3 = 0

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == 1 and (i, j) not in verified:
                nr_of_neighbors1 = neighbors_coordinates(i, j)
                if not nr_of_neighbors1:
                    iso = iso + 1
                    mark_as_verified(i, j)
                elif len(nr_of_neighbors1) == 1:
                    neighbor1_row, neighbor1_column = nr_of_neighbors1[0]
                    if (neighbor1_row, neighbor1_column) not in verified:
                        nr_of_neighbors2 = neighbors_coordinates(neighbor1_row, neighbor1_column)
                        if len(nr_of_neighbors2) == 1:
                            iso_clu2 = iso_clu2 + 1
                            mark_as_verified(i, j)
                            mark_as_verified(neighbor1_row, neighbor1_column)
                elif len(nr_of_neighbors1) == 2:
                    neighbor1_row, neighbor1_column = nr_of_neighbors1[0]
                    neighbor2_row, neighbor2_column = nr_of_neighbors1[1]
                    if (neighbor1_row, neighbor1_column) not in verified and (
                    neighbor2_row, neighbor2_column) not in verified:
                        nr_of_neighbors3_1 = neighbors_coordinates(neighbor1_row, neighbor1_column)
                        nr_of_neighbors3_2 = neighbors_coordinates(neighbor2_row, neighbor2_column)
                        if len(nr_of_neighbors3_1) == 1 and len(nr_of_neighbors3_2) == 1:
                            iso_clu3 = iso_clu3 + 1
                            neighbors_coordinates(i, j)
                            neighbors_coordinates(neighbor1_row, neighbor1_column)
                            neighbors_coordinates(neighbor2_row, neighbor2_column)

    return iso, iso_clu2, iso_clu3


def write_in_matout(iso, iso_clu2, iso_clu3):
    with open("mat.out", "a") as output:
        output.write(str(iso))
        output.write(' ')
        output.write(str(iso_clu2))
        output.write(' ')
        output.write(str(iso_clu3))
        output.write('\n')


with open("mat.in") as input:
    for line in input:
        matrix, rows, columns = create_matrix(line)
        iso, iso_clu2, iso_clu3 = count_neighboring_ones(matrix, rows, columns)
        write_in_matout(iso, iso_clu2, iso_clu3)

end = time.time()
print(f"The script ran for {end-start:.4} seconds.")