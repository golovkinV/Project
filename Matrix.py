class Matrix:
    # A
    def __init__(self, data):
        self.data = data.copy()

    def __str__(self):
        matrix_str = ""
        for rows in self.data:
            matrix_str += '\t'.join(str(row) for row in rows) + '\n'
        return matrix_str[:-1]

    def size(self):
        if len(self.data) == 0:
            return 0, 0
        return len(self.data), len(self.data[0])

    # B
    def __add__(self, other):
        if self.size() != other.size():
            raise MatrixError(self, other)

        main_data = self.data
        other_data = other.data
        result_data = [[main_data[i][j] + other_data[i][j] for j in range(len(main_data[0]))]
                       for i in range(len(main_data))]
        return Matrix(result_data)

    def __mul__(self, other):
        main_data = self.data
        result_data = [[main_data[i][j] * other for j in range(len(main_data[0]))]
                       for i in range(len(main_data))]
        return Matrix(result_data)

    def __rmul__(self, other):
        return self * other

    # C
    def transpose(self):
        self.data = self.__transpose_data()

    @staticmethod
    def transposed(matrix):
        data = matrix.__transpose_data()
        return Matrix(data)

    def __transpose_data(self):
        main_data = self.data
        return [[main_data[j][i] for j in range(len(main_data))]
                for i in range(len(main_data[0]))]


# C
class MatrixError(Exception):

    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


# A
m = Matrix([[1, 0], [0, 1]])
print(m)
print(m.size())
m = Matrix([[2, 0, 0], [0, 1, 10000]])
print(m)
print(m.size())
m = Matrix([[-10, 20, 50, 2443], [-5235, 12, 4324, 4234]])
print(m)
print(m.size())

# B
m1 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
m2 = Matrix([[0, 1, 0], [20, 0, -1], [-1, -2, 0]])
print(f"Результат сложения:\n{m1 + m2}")
print(f"Результат умножения на скаляр:\n{m1 * 10}")
print(f"Результат умножения на скаляр (аргумент справа):\n{10 * m1}")

# C
m2 = Matrix([[0, 1, 0], [20, 0, -1]])
try:
    m = m1 + m2
    print('WA\n' + str(m))
except MatrixError as e:
    print(f"\n{e.matrix1}\n")
    print(e.matrix2)

m2.transpose()
print(f"Результат transpose():\n{m2}")

m3 = Matrix.transposed(m2)
print(f"Результат transposed():\n{m3}")

