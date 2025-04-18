import bpy
from .constant import *
from .grid_gen_operator import GenerateGridOperator
class BasePanel(object):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MapAddon"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

class MapPanel(BasePanel, bpy.types.Panel):
    bl_label = "Map Generator"
    bl_idname = "VIEW3D_PT_map_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MapGen"

    def draw(self, context):
        layout = self.layout
        props = context.scene.map_generator_props

        layout.prop(props, "grid_size")
        row = layout.row()
        row.prop(props, "tiles_x")
        row.prop(props, "tiles_y")
        row.operator("object.generate_map", icon='MESH_PLANE')

