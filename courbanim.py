import bpy
import math
import mathutils
import numpy as np


fonc = [math.sin, math.cos]
bname = 'courbe'
fname = [str(f).split()[2][:-1] for f in fonc]


def updateline(nom, f, dec):
    bpy.data.curves[nom].splines.clear() 
    n = 100
    xVals = np.linspace(0,10,n)
    yVals = [(x,0.0,f(x+dec) + 2.0,1) for x in xVals]
    bpy.data.curves[nom].splines.new('POLY')
    p = bpy.data.curves[nom].splines[0].points
    p.add(len(yVals)-1)
    for i, coord in enumerate(yVals):
        p[i].co = coord
    

def updatevec(dec):
    n = 100
    for obj in bpy.data.objects:
        if 'flech' in obj.name:
            obj.location[2] = math.sin(obj.parent.location[0]+dec) + 2.0


def update(scene):
    dec = scene.frame_current / 4
    
    updatevec(dec)
    for i,f in enumerate(fonc):    
        nom = bname+fname[i]
        updateline(nom,f, dec)

bpy.app.handlers.frame_change_pre.append(update)
