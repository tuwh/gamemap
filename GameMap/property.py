# property.py

import bpy


def ensure_material(name, color):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
    return mat


def assign_material_to_chunk(obj, terrain_type):
    mat_map = {
        "grass": (0.2, 0.6, 0.2, 1),
        "rock": (0.4, 0.4, 0.4, 1),
        "sand": (0.8, 0.7, 0.3, 1),
        "water": (0.2, 0.4, 0.8, 1),
    }
    color = mat_map.get(terrain_type.lower(), (1, 1, 1, 1))
    mat = ensure_material(terrain_type, color)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def update_terrain_material(self, context):
    assign_material_to_chunk(self, self.terrain_type.lower())

def update_walkable(self, context):
    obj = self
    if obj and obj.name.startswith("chunk_"):
        obj["walkable"] = obj.walkable

class ChunkPropertyGroup(bpy.types.PropertyGroup):
    chunk_size: bpy.props.IntProperty(name="Chunk Size", default=2, min=1)
    count_x: bpy.props.IntProperty(name="Count X", default=4, min=1)
    count_y: bpy.props.IntProperty(name="Count Y", default=4, min=1)


classes = [ChunkPropertyGroup]


def register_props():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.chunk_props = bpy.props.PointerProperty(type=ChunkPropertyGroup)
    bpy.types.Object.terrain_type = bpy.props.EnumProperty(
        name="Terrain Type",
        description="Type of terrain for this chunk",
        items=[
            ("GRASS", "Grass", "Grassy terrain"),
            ("ROCK", "Rock", "Rocky terrain"),
            ("SAND", "Sand", "Sandy terrain"),
            ("WATER", "Water", "Watery area"),
        ],
        default="GRASS",
        update=update_terrain_material,
    )

    bpy.types.Object.walkable = bpy.props.BoolProperty(
        name="Walkable",
        description="Can walk through this terrain",
        default=True,
        update= update_walkable,
    )


def unregister_props():
    del bpy.types.Scene.chunk_props
    del bpy.types.Object.terrain_type
    del bpy.types.Object.walkable

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
