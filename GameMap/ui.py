import bpy
from bpy.types import Panel


class VIEW3D_PT_chunk_tools(Panel):
    bl_label = "Chunk Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Chunk Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene.chunk_props, "chunk_size")
        layout.prop(scene.chunk_props, "count_x")
        layout.prop(scene.chunk_props, "count_y")
        layout.operator("object.generate_chunks", icon="MESH_GRID")
        layout.operator("object.scatter_props", icon="PARTICLES")
        layout.operator("object.apply_heightmap", icon="IMAGE")

        obj = context.object
        if obj and obj.name.startswith("chunk_"):
            layout.label(text="Selected Chunk:")
            layout.prop(obj, "terrain_type")
            layout.prop(obj, 'walkable', text="Walkable")


def register():
    bpy.utils.register_class(VIEW3D_PT_chunk_tools)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_chunk_tools)