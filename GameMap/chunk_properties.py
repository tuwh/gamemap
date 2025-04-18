from bpy.props import EnumProperty, BoolProperty, StringProperty
import bpy

# 地形类型选项
TERRAIN_TYPES = [
    ("grass", "Grass", ""),
    ("water", "Water", ""),
    ("rock", "Rock", ""),
    ("sand", "Sand", "")
]

class ChunkPropertiesPanel(bpy.types.Panel):
    bl_label = "Chunk Properties"
    bl_idname = "VIEW3D_PT_chunk_properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Chunk Props"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.name.startswith("chunk_")

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if not obj:
            layout.label(text="No object selected.")
            return

        if not obj.name.startswith("chunk_"):
            layout.label(text="Selected object is not a chunk.")
            return

        layout.label(text=f"Name: {obj.name}")
        layout.label(text=f"Chunk X: {obj.get('chunk_x', 'N/A')}")
        layout.label(text=f"Chunk Y: {obj.get('chunk_y', 'N/A')}")

        # terrain_type dropdown
        terrain_type = obj.get("terrain_type", "grass")
        layout.prop(obj, '["terrain_type"]', text="Terrain Type", expand=True)

        # walkable checkbox
        walkable = obj.get("walkable", True)
        layout.prop(obj, '["walkable"]', text="Walkable")
