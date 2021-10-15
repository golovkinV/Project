import functools
import copy


# Help class for task E
class CramerRule:

    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector

    def calc(self):
        n = self.matrix.size()[0]
        origin_deter = self.__determinant(self.matrix.data, n)
        result = []
        if origin_deter > 0:
            for i in range(n):
                line = copy.deepcopy(self.matrix.data)
                for j in range(n):
                    line[j][i] = self.vector[j]
                line_det = self.__determinant(line, n)
                result.append(line_det / origin_deter)
        else:
            raise Exception
        return result

    def __determinant(self, matrix, n):
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        elif n == 3:
            return matrix[0][0] * matrix[1][1] * matrix[2][2] \
                   - matrix[0][0] * matrix[1][2] * matrix[2][1] \
                   - matrix[0][1] * matrix[1][0] * matrix[2][2] \
                   + matrix[0][1] * matrix[1][2] * matrix[2][0] \
                   + matrix[0][2] * matrix[1][0] * matrix[2][1] \
                   - matrix[0][2] * matrix[1][1] * matrix[2][0]
        else:
            c = 0
            for i in range(n):
                new_matrix = copy.deepcopy(matrix)
                new_matrix.pop(0)
                for j in range(n - 1):
                    new_matrix[j].pop(i)
                c += (-1) ** i * matrix[0][i] * self.__determinant(new_matrix, n - 1)
            return c


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

    # E - решение методом Крамера
    def solve(self, vector):
        return CramerRule(self, vector).calc()


# D
class SquareMatrix(Matrix):

    def __pow__(self, power, modulo=None):
        if power == 0:
            return self
        origin_matrix = copy.deepcopy(self)
        for el in range(1, power):
            origin_matrix *= self
        return origin_matrix


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
mid = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
m1 = Matrix([[3, 2], [-10, 0], [14, 5]])
m2 = Matrix([[5, 2, 10], [-0.5, -0.25, 18], [-22, -2.5, -0.125]])
print(f"\nРезультат 5 * m2:\n{5 * m2}")
print(f"\nРезультат m2 * (120 * mid * m1):\n{m2 * (120 * mid * m1)}")

# E - check 1
m = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
print(f"\nРешение уравнения (check 1): {m.solve([1, 1, 1])}")

# E - check 2
m = Matrix([[1, 1, 1], [0, 2, 0], [0, 0, 4]])
print(f"\nРешение уравнения (check 2): {m.solve([1, 1, 1])}")

# E - check 3
m = Matrix([[1, 1, 1], [0, 1, 2], [0.5, 1, 1.5]])
try:
    s = m.solve([1, 1, 1])
    print('WA No solution')
except Exception as e:
    print('\nРешение уравнения (check 3): No answer')

# F - check 1
m = SquareMatrix([[1, 0], [0, 1]])
print(f"\nF - check 1: {isinstance(m, Matrix)}")

# F - check 2
m = SquareMatrix([[1, 0], [0, 1]])
print(f"\nF - check 2:\n{m ** 0}")

# F - check 3
m = SquareMatrix([[1, 1, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0],
                  [0, 0, 1, 1, 0, 0],
                  [0, 0, 0, 1, 1, 0],
                  [0, 0, 0, 0, 1, 1],
                  [0, 0, 0, 0, 0, 1]]
                )
print(f"\n{m}")
print('----------')
print(f'Степень 1\n{m ** 1}')
print('----------')
print(f'Степень 2\n{m ** 2}')
print('----------')
print(f'Степень 3\n{m ** 3}')
print('----------')
print(f'Степень 4\n{m ** 4}')
print('----------')
print(f'Степень 5\n{m ** 5}')

