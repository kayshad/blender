import bpy
import math
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
coll = bpy.data.collections.new('Vecteur')
SC.link(coll)
mat = bpy.data.materials['chrome.000']

def emptyinit(so,se,po,pe):
    orig = D.objects.new(so, None)
    orig.location = po
    ext = D.objects.new(se, None)
    ext.location = pe
    ext.empty_display_type = 'CONE'
    ext.empty_display_size = 0.1
    ext.parent = orig
    ext.constraints.new(type='TRACK_TO')
    cons = ext.constraints[0]
    cons.target = orig
    cons.track_axis = 'TRACK_NEGATIVE_Y'
    cons.up_axis = 'UP_Z'
    coll.objects.link(orig)
    coll.objects.link(ext)
    
    return orig, ext


def norminit(so,se,po,pe):
    
    e = emptyinit(so,se,po,pe)
    
    Ops.mesh.primitive_cylinder_add(vertices=16, radius=.02, depth=1.0, end_fill_type='TRIFAN', calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.5, 0.0, 0.0), rotation=(0.0, math.radians(90.0), 0.0))
    Ops.object.transform_apply(location=False, rotation=True, scale=False)
    Ops.object.origin_set(type='ORIGIN_CURSOR')
    obj = D.objects['Cylindre']
    obj.name = 'norme'
    obj.data.materials.append(mat)
    obj.parent = e[0]
    obj.constraints.new(type='TRACK_TO')
    cons = obj.constraints[0]
    cons.target = e[1]
    cons.track_axis = 'TRACK_X'
    cons.up_axis = 'UP_Z'
    drv = obj.driver_add('scale',0)
    var = drv.driver.variables.new() 
    var.name='MaVar' 
    var.type='LOC_DIFF'
    targeto = var.targets[0] 
    targete = var.targets[1]
    targeto.id = e[0]
    targete.id = e[1]
    drv.driver.expression = var.name + '- 0.40'
    coll.objects.link(obj)
    MC.unlink(obj)
    
    Ops.mesh.primitive_cone_add(vertices=32, radius1=0.1, radius2=0.0, depth=0.5, end_fill_type='TRIFAN', calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, -0.25, 0.0), rotation=(-math.radians(90.0), 0.0, 0.0))
    obj = D.objects['Cône']
    obj.name = 'cone'
    obj.data.materials.append(mat)
    coll.objects.link(obj)
    MC.unlink(obj)
    bpy.data.objects['cone'].parent = e[1]
    return e

def relat(v1,v2,v3):
    v2[0].parent = v1[1]
    v2[0].matrix_parent_inverse = v1[1].matrix_world.inverted()
    v3[0].parent = v1[0]
    v3[0].matrix_parent_inverse = v1[0].matrix_world.inverted()
    v3[1].parent = v2[1]
    v3[1].matrix_parent_inverse = v2[1].matrix_world.inverted()


def som(p0,p1,p3):
    tuple_add = lambda a, b: tuple(i+j for i, j in zip(a, b))
    v1 = norminit('orig','ext', p0, p1)
    v2 = norminit('orig','ext', v1[1].location, p3)
    v3 = norminit('orig','ext', v1[0].location, tuple_add(v1[1].location,v2[1].location))
    relat(v1,v2,v3)


def somo(p1,p3):
    tuple_add = lambda a, b: tuple(i+j for i, j in zip(a, b))
    v1 = norminit('orig','ext', (0,0,0), p1)
    v2 = norminit('orig','ext', v1[0].location, p3)
    v3 = norminit('orig','ext', v1[0].location, tuple_add(v1[1].location,v2[1].location))
    relat(v1,v2,v3)


def sub(p0,p1,p3):
    tuple_add = lambda a, b: tuple(i+j for i, j in zip(a, b))
    tuple_inv = lambda a: tuple(-1*i for i in a)
    v1 = norminit('orig','ext', p0, p1)
    v2 = norminit('orig','ext', v1[1].location, p3)
    v3 = norminit('orig','ext', v1[0].location, tuple_add(v1[1].location,tuple_inv(v2[1].location)))
    relat(v1,v2,v3)


def subo(p1,p3):
    tuple_add = lambda a, b: tuple(i+j for i, j in zip(a, b))
    tuple_inv = lambda a: tuple(-1*i for i in a)
    v1 = norminit('orig','ext', (0,0,0), p1)
    v2 = norminit('orig','ext', v1[0].location, p3)
    v3 = norminit('orig','ext', v1[0].location, tuple_add(v1[1].location,tuple_inv(v2[1].location)))
    relat(v1,v2,v3)    

#som((0,0,0),(1,1,1),(2,3,2))
#sub((0,0,0),(1,1,1),(2,3,2))
subo((1,1,1),(2,3,2))
#somo((1,1,1),(2,3,2))
