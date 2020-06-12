import bpy
import numpy as np
import math

fonc = [math.sin, math.cos]
bname = 'courbe'
fname = [str(f).split()[2][:-1] for f in fonc]
#print(fonc,fname)
#MasterColl = s.objects

s = bpy.data.scenes['Scene'].view_layers['View Layer'].layer_collection.collection
#fps = bpy.data.scenes['Scene'].render.fps

def nettoi():
    bpy.app.handlers.frame_change_pre.clear()
    for cur in bpy.data.curves:
        if bname in cur.name:
            bpy.data.curves.remove(cur)    
    for o in bpy.data.objects:
        if bname in o.name:
            bpy.data.objects.remove(o)
    for c in bpy.data.collections:           
        if 'MaCollection' in c.name:
            bpy.data.collections.remove(c)
                    
    
def cree():
    for name in fname:
        MaColl = bpy.data.collections.new('MaCollection'+name)
        s.children.link(MaColl)
        curveData = bpy.data.curves.new(bname+name, type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 2
        curveData.bevel_depth = 0.01
        curveOB = bpy.data.objects.new(bname+name, curveData)
        MaColl.objects.link(curveOB)

def updateline(nom, f, t, zoom = 1):
    bpy.data.curves[nom].splines.clear() 
    n = 100
    xVals = np.linspace(0,10,n)
    yVals = [(zoom*x,0.0,zoom*f(x+t),1) for x in xVals]
    bpy.data.curves[nom].splines.new('POLY')
    p = bpy.data.curves[nom].splines[0].points
    p.add(len(yVals)-1)
    for i, coord in enumerate(yVals):
        p[i].co = coord
    




def update(scene):
    t = scene.frame_current//4
    for i,f in enumerate(fonc):    
        nom = bname+fname[i]
        updateline(nom,f, t)




nettoi()
cree()
bpy.app.handlers.frame_change_pre.append(update)

