import bpy
from math import *
import fvect
from bpy.types import(Panel, Operator, PropertyGroup)
import mathutils
D = bpy.data

class MonPano(Panel):
    bl_label = "Calculer"
    bl_idname = "OBJECT_PT_monpano"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Math addon"

    def draw(self, context):
        layout = self.layout
        scene = context.scene.mes_props
        col = layout.column()
        col.operator('mon.op')
        col.prop(scene, "vecteur")   

class MonOp(Operator):
    bl_idname = "mon.op"
    bl_label = "X"
    bl_description = ""
    
    def execute(self, context):
        scene = context.scene.mes_props
        vecteur = scene.vecteur
        print(fvect.vect(mathutils.Vector(vecteur)))
        vecteur[0] += 1.0
        return {'FINISHED'}

class MesProps(bpy.types.PropertyGroup):
    vecteur: bpy.props.FloatVectorProperty(name='Vecteur', description='', default=(0.0, 0.0, 0.0))

classes = (MonPano,MonOp,MesProps)
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.mes_props = bpy.props.PointerProperty(type=MesProps)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mes_props
    
if __name__ == "__main__":
    register()
