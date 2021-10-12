import struct

def frombuffer(array, dtype):
    newarray = []
    for element in array:
        newarray.append(element)
    return newarray

def dot(mat1, mat2):
    if not isinstance(mat1[0], list):
        mat1 = [[i] for i in mat1]
    if not isinstance(mat2[0], list):
        mat2 = [[i] for i in mat2]
  
    result = []
    for i in range(0, len(mat1)):
        app = []
        for j in range(0, len(mat2[0])):
            subS = 0
            for k in range(0, len(mat1[0])):
                subS += mat1[i][k] * mat2[k][j]
            app.append(subS)
        result.append(app)
    return result