import bpy
import math
import mathutils
import numpy as np


fonc = [math.sin, math.cos]
bname = 'courbe'
fname = [str(f).split()[2][:-1] for f in fonc]
#print(fonc,fname)

A = bpy.app
D = bpy.data
C = bpy.context
Ops = bpy.ops
T = bpy.types
P = bpy.path
Pr = bpy.props
U = bpy.utils
MC = C.view_layer.active_layer_collection.collection.objects
SC = C.scene.collection.children
mat = bpy.data.materials['vecteur']
s = bpy.data.scenes['Scene'].view_layers['View Layer'].layer_collection.collection
vecint = None
v= bpy.data.scenes['Scene'].render.fps

def creempty(vec):
    coll = bpy.data.collections.new('Vecteur')
    SC.link(coll)
    orig = D.objects.new('orig', None)
    orig.location = vec[:]
    flech = bpy.data.objects['fvect'].copy()
    norme = bpy.data.objects['nvect'].copy()
    flech.parent = orig
    norme.parent = orig
    flech.constraints["Suivi de"].target = orig
    norme.constraints["Suivi de"].target = flech
    drv = norme.animation_data.drivers[0]
    var = drv.driver.variables[0]
    var.targets[0].id = orig  
    var.targets[1].id = flech
    #drv.driver.expression = var.name + '- 0.2'
    coll.objects.link(orig)
    coll.objects.link(flech)
    coll.objects.link(norme)
    return orig, coll


def vec():
    Koll = bpy.data.collections.new('vector')
    SC.link(Koll)
    veco = mathutils.Vector((0.0, 0.0, 0.0))
    veco_n = veco.normalized()
    retour = creempty(veco)
    collectreturn = retour[1]
    Koll.children.link(collectreturn)
    SC.unlink(collectreturn)





def chvec(n):
    Koll = bpy.data.collections.new('ChampVecteur')
    SC.link(Koll)
    for i in range(n):
    
        if i == 0:
            veco = mathutils.Vector((i, 0.0, 0.0))
            veco_n = veco.normalized()
            retour = creempty(veco)
            vecint = retour[0]
            collectreturn = retour[1]
            Koll.children.link(collectreturn)
            SC.unlink(collectreturn)
    
        else:
            veco = mathutils.Vector((i, 0.0, 0.0))
            veco_n = veco.normalized()
            retour = creempty(veco)
            retour[0].parent = vecint
            collectreturn = retour[1]
            Koll.children.link(collectreturn)
            SC.unlink(collectreturn)
    



def nettoi():
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
        MasterColl = s.objects
        MaColl = bpy.data.collections.new('MaCollection'+name)
        s.children.link(MaColl)
        curveData = bpy.data.curves.new(bname+name, type='CURVE')
        curveData.dimensions = '3D'
        curveData.resolution_u = 2
        curveData.bevel_depth = 0.01
        curveOB = bpy.data.objects.new(bname+name, curveData)
        MaColl.objects.link(curveOB)

def updateline(nom, f, dec):
    bpy.data.curves[nom].splines.clear() 
    n = 100
    xVals = np.linspace(0,10,n)
    yVals = [(x,0.0,f(x+dec),1) for x in xVals]
    bpy.data.curves[nom].splines.new('POLY')
    p = bpy.data.curves[nom].splines[0].points
    p.add(len(yVals)-1)
    for i, coord in enumerate(yVals):
        p[i].co = coord
        
    
    
    

def updatevec(dec):
    for i, obj in enumerate(bpy.data.objects):
        if 'fvect.' in obj.name:
            print(obj.name)
            obj.location[2] = math.cos(obj.parent.location[0]+dec)


def update(scene):
    dec = scene.frame_current
    updatevec(dec)
    for i,f in enumerate(fonc):    
        nom = bname+fname[i]
        updateline(nom,f, dec)


#nettoi()
#cree()
bpy.app.handlers.frame_change_pre.append(update)

#cree()

#chvec(4)
