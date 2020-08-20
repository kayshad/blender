import bpy
import math



A = bpy.app
D = bpy.data
C = bpy.context
O = bpy.ops
T = bpy.types
P = bpy.path
Pr = bpy.props
U = bpy.utils

point0 = (3,3,3)
point1 = (1,0,0)
point2 = (1,1,0)
point2inv = (-1,-1,0)






def vecteur(point0,point1):
    print(bpy.data.scenes.keys())
    coll = bpy.data.collections.new('Vecteur')
    bpy.context.scene.collection.children.link(coll)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.02, depth=1.0, end_fill_type='TRIFAN', calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.5, 0.0, 0.0), rotation=(0.0, math.radians(90.0), 0.0))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    obj = D.objects['Cylindre']
    obj.name = 'norme'
    coll.objects.link(obj)
    C.view_layer.active_layer_collection.collection.objects.unlink(obj)    
    newvec = bpy.context.active_object
    orig = D.objects.new('originevect', None)
    orig.location[0] = point0[0]
    orig.location[1] = point0[1]
    orig.location[2] = point0[2]
    extrem = D.objects.new('extremvect', None)
    extrem.constraints.new(type='TRACK_TO')
    extrem.empty_display_type = 'CONE'
    extrem.empty_display_size = 0.1
    extrem.location[0] = point1[0]
    extrem.location[1] = point1[1]
    extrem.location[2] = point1[2]
    extrem.parent = orig
    extrem.constraints[0].target = orig
    extrem.constraints[0].track_axis = 'TRACK_NEGATIVE_Y'
    extrem.constraints[0].up_axis = 'UP_Z'
    newvec.parent = orig
    newvec.constraints.new(type='TRACK_TO')
    newvec.constraints[0].target = extrem
    newvec.constraints[0].track_axis = 'TRACK_X'
    newvec.constraints[0].up_axis = 'UP_Z'
    drv = newvec.driver_add('scale',0)
    var = drv.driver.variables.new() 
    var.name='MaVar' 
    var.type='LOC_DIFF'
    targeto = var.targets[0] 
    targete = var.targets[1]
    targeto.id = orig
    targete.id = extrem
    drv.driver.expression = var.name + '- 0.40'
    coll.objects.link(orig)
    coll.objects.link(extrem)
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.1, radius2=0.0, depth=0.5, end_fill_type='TRIFAN', calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, -0.25, 0.0), rotation=(-math.radians(90.0), 0.0, 0.0))
    obj = D.objects['Cône']
    obj.name = 'cone'
    coll.objects.link(obj)
    C.view_layer.active_layer_collection.collection.objects.unlink(obj)
    bpy.data.objects['cone'].parent = extrem
    
    
    return orig,extrem

    
def sumVector(point0, point1,point2):
    
    
    pointSomme= [0,0,0]
    for i in range(3):
        pointSomme[i] = point0[i] + point1[i] +point2[i]    
    retour0 = vecteur(point0,point1)
    retour1 = vecteur(point1,point2)
    retour2 = vecteur(point0,pointSomme)
    drv = retour0[1].driver_add('location')
    tuploc = ('LOC_X', 'LOC_Y', 'LOC_Z')
    for i in range(3):
        var = drv[i].driver.variables.new()
        var.name='MaVar'
        var.type='TRANSFORMS' 
        target = var.targets[0] 
        target.id = bpy.data.objects[retour1[0].name]
        target.transform_type = tuploc[i]
        target.transform_space = 'WORLD_SPACE'
        drv[i].driver.expression = var.name
         
        
         
    drv = retour2[1].driver_add('location')
    for j in range(3):
        var = drv[j].driver.variables.new()
        var.name='MaVar'
        var.type='TRANSFORMS' 
        target = var.targets[0] 
        target.id = bpy.data.objects[retour1[1].name]
        target.transform_type = tuploc[j]
        target.transform_space = 'WORLD_SPACE'
        drv[j].driver.expression = var.name
        
        

vecteur(point0,point1)
#sumVector(point0,point1,point2)
#sumVector(point0,point1,point2inv)
