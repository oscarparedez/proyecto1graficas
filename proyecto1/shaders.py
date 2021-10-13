from gl import *
from lib import color, writebmp
from obj import Texture

width = 1500
height = 1500

def gourad(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_texture.get_color(tx, ty)
  # normals
  nA, nB, nC = kwargs['varying_normals']
  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC

  r = int(tcolor[2] * intensity)
  g = int(tcolor[1] * intensity)
  b = int(tcolor[0] * intensity)

  if r < 0:
    r = 0
  elif r > 255:
    r = 255
  if g < 0:
    g = 0
  elif g > 255:
    g = 255
  if b < 0:
    b = 0
  elif b > 255:
    b = 255
  return color(r, g, b)

def sky(render, **kwargs):
  return color(0, 224, 240)

rend = Renderer()
rend.glInit()
rend.glCreateWindow(width, height)
rend.glViewPort(0, 0, width, height)

rend.lookAt(V3(2, 0, 2), V3(0, 0, 0), V3(0, 1, 0))
rend.light = norm(V3(1, 2, 1.5))

rend.active_shader = gourad

#Soldier's gun
t3 = Texture('./models/mp5/mp5.bmp')
rend.active_texture = t3
rend.load('./models/mp5/mp5.obj', translate=(-0.86, -0.47, 0.55), scale=(0.0028, 0.0028, 0.0028), rotate=(0.5, -0.4, 0))
rend.draw_arrays('TRIANGLES')

#Soldier
t1 = Texture('./models/soldier/soldier.bmp')
rend.active_texture = t1
rend.load('./models/soldier/soldier.obj', translate=(-0.6, -0.9, 0.25), scale=(0.12, 0.12, 0.12), rotate=(0, 0.7, 0))
rend.draw_arrays('TRIANGLES')

#The good one from the movie
t2 = Texture('./models/deadpool/deadpool.bmp')
rend.active_texture = t2
rend.load('./models/deadpool/deadpool.obj', translate=(0, -0.9, 0.1), scale=(0.005, 0.005, 0.005), rotate=(0, 0.9, 0))
rend.draw_arrays('TRIANGLES')

#Soldier #2
t4 = Texture('./models/soldier2/soldier2.bmp')
rend.active_texture = t4
rend.load('./models/soldier2/soldier2.obj', translate=(0.5, -0.8, 0.1), scale=(0.15, 0.15, 0.15), rotate=(0, 0, 0))
rend.draw_arrays('TRIANGLES')

#Floor
t5 = Texture('./models/escenario/asphalt.bmp')
rend.active_texture = t5
rend.load('./models/escenario/escenario.obj', translate=(-0.6, -0.8, 0.1), scale=(1.6, 0.4, 0.1), rotate=(0, 0.5, 0))
rend.draw_arrays('TRIANGLES')

# #Renetti
t6 = Texture('./models/renetti/renetti.bmp')
rend.active_texture = t6
rend.load('./models/renetti/renetti.obj', translate=(0.97, -0.37, 0.4), scale=(0.0018, 0.0018, 0.0018), rotate=(0.8, 0.9, 0.8))
rend.draw_arrays('TRIANGLES')

# 1911 Handgun
t6 = Texture('./models/1911/1911.bmp')
rend.active_texture = t6
rend.load('./models/1911/1911.obj', translate=(0, -0.6, 0.4), scale=(0.0028, 0.0028, 0.0028), rotate=(0.9, 0.2, 0))
rend.draw_arrays('TRIANGLES')

#Sky
rend.active_shader = sky
rend.load('./models/escenario/escenario.obj', translate=(-0.4, 0.4, -0.4), scale=(1.5, 1, 0.1), rotate=(0, 0.5, 0))
rend.draw_arrays('TRIANGLES')

writebmp('a.bmp', width, height, rend.framebuffer)