import struct
import customNumpy

def color(r, g, b):
  return bytes([b, g, r])

class V3(object):
  def __init__(self, x, y = None, z = None):
    if (customNumpy.isMatrix(x)):
      self.x, self.y, self.z = x
    else:
      self.x = x
      self.y = y
      self.z = z

  def __repr__(self):
    return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

class V2(object):
  def __init__(self, x, y = None):
    if (customNumpy.isMatrix(x)):
      self.x, self.y = x
    else:
      self.x = x
      self.y = y

  def __repr__(self):
    return "V2(%s, %s)" % (self.x, self.y)

def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

def bbox(*vertices):
  xs = [ vertex.x for vertex in vertices ]
  ys = [ vertex.y for vertex in vertices ]
  xs.sort()
  ys.sort()

  return V2(int(xs[0]), int(ys[0])), V2(int(xs[-1]), int(ys[-1]))


def barycentric(A, B, C, P):
  bary = cross(
    V3(C.x - A.x, B.x - A.x, A.x - P.x),
    V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if abs(bary.z) < 1:
    return -1, -1, -1

  return (
    1 - (bary.x + bary.y) / bary.z,
    bary.y / bary.z,
    bary.x / bary.z
  )

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def writebmp(filename, width, height, pixels):
  f = open(filename, 'bw')

  # File header (14 bytes)
  f.write(char('B'))
  f.write(char('M'))
  f.write(dword(14 + 40 + width * height * 3))
  f.write(dword(0))
  f.write(dword(14 + 40))

  # Image header (40 bytes)
  f.write(dword(40))
  f.write(dword(width))
  f.write(dword(height))
  f.write(word(1))
  f.write(word(24))
  f.write(dword(0))
  f.write(dword(width * height * 3))
  f.write(dword(0))
  f.write(dword(0))
  f.write(dword(0))
  f.write(dword(0))

  # Pixel data (width x height x 3 pixels)
  for x in range(height):
    for y in range(width):
      f.write(pixels[x][y])
  f.close()