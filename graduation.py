import bpy
import mathutils
import math
D, OBJ, CUR = bpy.data, bpy. data. objects, bpy.data.curves

def grad():
    mat = bpy.data.materials.new('nombre')
    coll = bpy.data.collections.new('Graduation')
    D.scenes["Scene"].collection.children.link(coll)
    extrem = D.objects.new('unit', None)
    extrem.location = (1,0,0)
    coll.objects.link(extrem)
    
    for i in range(-50,51):
        grad = CUR.new(type='FONT', name = 'nombre')
        obj = OBJ.new('Nombre',grad)
        coll.objects.link(obj)
        obj.rotation_euler.x = math.radians(90.0)
        obj.data.extrude = .05
        obj.data.align_x = 'CENTER'
        obj.data.body = str(i)
        obj.location.x = i
        obj.location.z = .05
        obj.data.materials.append(mat)
        for j in range(3):
            obj.scale[j] = .5  
        drv = obj.driver_add('location',0)
        var = drv.driver.variables.new() 
        var.name='MaVar'  
        var.type='TRANSFORMS'
        target = var.targets[0] 
        target.id = extrem
        target.transform_type = 'LOC_X'
        target.transform_space = 'WORLD_SPACE'
        drv.driver.expression = var.name +'*'+ str(i)
        obj.parent = extrem  
grad()
