import bpy, sys ,os
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    for l in sys.path:
        print(l)
        
        
import courbe

print(courbe.fonc)
#courbe.nettoi()
