import struct

def frombuffer(array, dtype):
    newarray = []
    for element in array:
        newarray.append(element)
    return newarray

def isMatrix(object):
    return isinstance(object, list)

def minor(mat, i, j):
    return [row[:j] + row[j+1:] for row in (mat[:i]+mat[i+1:])]

def det(mat):
    if len(mat) == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

    determinant = 0
    
    for c in range(len(mat)):
        determinant += ((-1)**c) * mat[0][c] * det(minor(mat, 0, c))
    return determinant

def grid(intervalX, intervalY):
    li1 = []
    li2 = []
    for i in intervalX:

        li3 = []
        for j in intervalY:            
            li3.append(i)
        li2.append(li3)
    li1.append(li2)
    li2 = []

    for i in intervalX:
        li3 = []

        for j in intervalY:            
            li3.append(j)
        li2.append(li3)
    lista.append(li2)
    return li1

def reshape(mat):
  matLength = len(mat)
  matRowLength = len(mat[0])
  matColumnLength = len(mat[0][0])
  x = matLength * matRowLength * matColumnLength/2
  x = int(x)
  li1 = []
  for i in mat:
    for j in i:
      for k in j:
        li1.append(k)

  li2 = []
  for i in range(0, 2):
    li3 = []
    for j in range(0, x):
      li3.append(li1[i * x + j])
    li2.append(li3)
  return li2

def vstack(mat):
    matColumnLength = len(mat[0])
    li1 = mat
    li2 = []
    for i in range(0, matColumnLength):
        li2.append(1.0)
    li1.append(li2)
    return li1

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

def transpose(mat):
    rows = len(mat)
    columns = len(mat[0])
    trans = []
    for j in range(columns):
        row = []
        for i in range(rows):
           row.append(mat[i][j])
        trans.append(row)
    return trans
    