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






class Vecteur:
    def __init__(self,comp):
        
        self.comp = comp
        #self.vecteur = comp
        self.vec(self.comp)
        
    
    
    def creempty(self, vect):
        coll = bpy.data.collections.new('Vecteur')
        SC.link(coll)
        orig = bpy.data.objects['vecteur'].copy()
        norme = bpy.data.objects['nvect'].copy()
        norme.parent = orig
        flech = bpy.data.objects['fvect'].copy()
        flech.parent = orig
        flech.constraints["Suivi de"].target = orig
        flech.location = vect[:]
        norme.constraints["Suivi de"].target = flech
        flech1 = bpy.data.objects['fvectu'].copy()
        flech1.parent = flech
        flech1.constraints["Suivi de"].target = orig
        flech1.location = vect.normalized()[:]
        matrix_world = np.identity(4, dtype=float)
        flech1.matrix_world = matrix_world
        drv = flech1.animation_data.drivers[0]
        var = drv.driver.variables[0]
        var.targets[0].id = orig  
        var.targets[1].id = flech
        drv = norme.animation_data.drivers[0]
        var = drv.driver.variables[0]
        var.targets[0].id = orig  
        var.targets[1].id = flech
        #drv.driver.expression = var.name + '- 0.2'
        coll.objects.link(orig)
        coll.objects.link(flech)
        coll.objects.link(flech1)
        coll.objects.link(norme)
        return orig, coll


    def vec(self, comp):
        vect = mathutils.Vector(comp)
        Koll = bpy.data.collections.new('vector')
        SC.link(Koll)
        retour = self.creempty(vect)
        collectreturn = retour[1]
        Koll.children.link(collectreturn)
        SC.unlink(collectreturn)

v = Vecteur((1.0, 1.0, 1.0))
