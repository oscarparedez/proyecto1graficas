from gl import *
from lib import color, writebmp
from model import Texture

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
  if tcolor == []:
    return color(0,0,0)
  else:
    r = int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0
    g = int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0
    b = int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    #print(tcolor[2], tcolor[1], tcolor[0])
    if r > 255:
      r = 255
    if g > 255:
      g = 255
    if b > 255:
      b = 255
    return color(r,g,b)

def sky_shader(render, **kwargs):
  # barycentric
  w, v, u = kwargs['bar']
  # texture
  tcolor = (137,209,254)
  # normals
  nA, nB, nC = kwargs['varying_normals']
  # light intensity
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC
  if tcolor == []:
    return color(0,0,0)
  else:
    return color(0,224 ,240)

r = Renderer()
r.glInit()
r.glCreateWindow(1500, 1500)
r.glViewPort(0, 0, 1500, 1500)
r.light = norm(V3(1, -2, 1.5))
r.active_shader = gourad
r.lookAt(V3(2, 0, 2), V3(0, 0, 0), V3(0, 1, 0))

#Soldier's gun
t3 = Texture('./models/mp5/mp5.bmp')
r.active_texture = t3
r.load('./models/mp5/mp5.obj', translate=(-0.89, -0.47, 0.55), scale=(0.0025, 0.0025, 0.0025), rotate=(0.5, -0.4, 0))
r.draw_arrays('TRIANGLES')

#Soldier
t1 = Texture('./models/soldier/soldier.bmp')
r.active_texture = t1
r.load('./models/soldier/soldier.obj', translate=(-0.6, -0.9, 0.25), scale=(0.12, 0.12, 0.12), rotate=(0, 0.7, 0))
r.draw_arrays('TRIANGLES')

#The good one from the movie
t2 = Texture('./models/deadpool/deadpool.bmp')
r.active_texture = t2
r.load('./models/deadpool/deadpool.obj', translate=(0, -0.9, 0.1), scale=(0.005, 0.005, 0.005), rotate=(0, 0.9, 0))
r.draw_arrays('TRIANGLES')

#Soldier #2
t4 = Texture('./models/soldier2/soldier2.bmp')
r.active_texture = t4
r.load('./models/soldier2/soldier2.obj', translate=(0.5, -0.8, 0.1), scale=(0.15, 0.15, 0.15), rotate=(0, 0, 0))
r.draw_arrays('TRIANGLES')

#Floor
t5 = Texture('./models/escenario/rock.bmp')
r.active_texture = t5
r.load('./models/escenario/escenario.obj', translate=(-0.6, -0.8, 0.1), scale=(1.6, 0.4, 0.1), rotate=(0, 0.5, 0))
r.draw_arrays('TRIANGLES')

#Sky
r.active_shader = sky_shader
r.load('./models/escenario/escenario.obj', translate=(-0.4, 0.4, -0.4), scale=(1.5, 1, 0.1), rotate=(0, 0.5, 0))
r.draw_arrays('TRIANGLES')

writebmp('a.bmp', 1500, 1500, r.framebuffer)