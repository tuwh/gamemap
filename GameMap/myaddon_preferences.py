import os

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences

from .constant import *


class MyAddonPreferences(AddonPreferences):
    # this must match the add-on name (the folder name of the unzipped file)
    bl_idname = PLUGIN_NAME

    grid_size: bpy.props.IntProperty(
        name="Grid Size",
        description="Size of each grid cell",
        default=2,
        min=1
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text = "单个网格大小")
        layout.prop(self, "grid_size")

