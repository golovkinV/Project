import functools


class _Matrix(object):
    def __init__(self, data):
        self.data = data.copy()


class Matrix(_Matrix):

    # A

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

    # D
    @functools.singledispatchmethod
    def __mul__(self, other):
        return NotImplemented

    @__mul__.register(float)
    def _(self, other):
        return self.__mul_scalar(other)

    @__mul__.register(int)
    def _(self, other):
        return self.__mul_scalar(other)

    @__mul__.register(_Matrix)
    def _(self, other):
        main_size = self.size()
        other_size = other.size()
        if main_size[1] != other_size[0]:
            raise MatrixError(self, other)

        main_data = self.data
        other_data = other.data
        result = []
        for i in range(main_size[0]):
            result_row = []
            for j in range(other_size[1]):
                cell_sum = 0
                for k in range(other_size[0]):
                    cell_sum += main_data[i][k] * other_data[k][j]
                result_row.append(cell_sum)
            result.append(result_row)

        return Matrix(result)

    def __rmul__(self, other):
        return self * other

    # C
    def transpose(self):
        self.data = self.__transpose_data()

    @staticmethod
    def transposed(matrix):
        data = matrix.__transpose_data()
        return Matrix(data)

    def __mul_scalar(self, other):
        main_data = self.data
        result_data = [[main_data[i][j] * other for j in range(len(main_data[0]))]
                       for i in range(len(main_data))]
        return Matrix(result_data)

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
print(f"Результат m1 + m2:\n{m1 + m2}")
print(f"Результат m1 * 10:\n{m1 * 10}")
print(f"Результат 10 * m1:\n{10 * m1}")

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

# D - check 1
mid = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
print(f"\nРезультат mid * m1:\n{mid * m1}")
print(f"\nРезультат mid * m2:\n{mid * m2}")
print(f"\nРезультат m2 * m1:\n{m2 * m1}")

try:
    m = m1 * m2
    print("WA It should be error")
except MatrixError as e:
    print(f"\n{e.matrix1}\n")
    print(e.matrix2)

# D - check 2
mid = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
print(f"\nРезультат 0.5 * m2:\n{0.5 * m2}")
print(f"\nРезультат m2 * (0.5 * mid * m1):\n{m2 * (0.5 * mid * m1)}")

# D - check 3
mid = Matrix([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
print(f"\nРезультат 5 * m2:\n{5 * m2}")
print(f"\nРезультат m2 * (120 * mid * m1):\n{m2 * (120 * mid * m1)}")

