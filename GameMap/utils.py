import bpy

def ensure_materials():
    colors = {
        "grass": (0.0, 0.8, 0.0, 1),
        "water": (0.2, 0.4, 1.0, 1),
        "rock": (0.5, 0.5, 0.5, 1),
        "sand": (0.9, 0.8, 0.3, 1),
    }

    materials = {}
    for name, color in colors.items():
        mat_name = f"Mat_{name}"
        if mat_name in bpy.data.materials:
            mat = bpy.data.materials[mat_name]
        else:
            mat = bpy.data.materials.new(mat_name)
            mat.diffuse_color = color
            mat.use_nodes = False
        materials[name] = mat
    return materials

def apply_material(obj, terrain_type, materials):
    mat = materials.get(terrain_type)
    if mat:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
