# ------------Se utilizo como referencia para algunas operaciones https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
import struct

def frombuffer(array, dtype):
    newarray = []
    for element in array:
        newarray.append(element)
    return newarray

def det2(mat):
    return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

def det(mat):
    det = 0
    for i in range(len(mat)):
        determinant += ((-1)**i)*mat[0][i]*det(identity(mat))
    return determinant

def inverse2(mat):
    det = det2(mat)
    return [[m[1][1]/det, -1*m[0][1]/det], [-1*m[1][0]/det, m[0][0]/det]]  

def dot(mat1, mat2):
    if not isinstance(mat1[0], list):
        mat1 = [[i] for i in mat1]
    if not isinstance(mat2[0], list):
        mat2 = [[i] for i in mat2]

    product = []
    for i in range(len(mat1)):
        vec = []
        for j in range(len(mat2[0])):
            operation = 0
            for k in range(len(mat1[0])):
                operation += mat1[i][k] * mat2[k][j]
            vec.append(operation)
        product.append(vec)
    return product


#def dot(mat1, mat2):
#    return sum(x*y for x, y in zip(mat1, mat2))


def trasponse(mat):
    for i in range(len(mat[0])):
        for j in range(i+1, len(mat[0])):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    return mat

# def trasponse(mat):
#     return map(list,zip(*mat))
