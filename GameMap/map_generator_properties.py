from bpy.props import IntProperty, FloatProperty
from bpy.types import  PropertyGroup

class MapGeneratorProperties(PropertyGroup):
    grid_size: FloatProperty(
        name="Grid Size",
        default=2.0,
        min=0.1,
        description="Size of one tile"
    )

    tiles_x: IntProperty(
        name="Tiles X",
        default=10,
        min=1,
        description="Number of tiles in X"
    )

    tiles_y: IntProperty(
        name="Tiles Y",
        default=10,
        min=1,
        description="Number of tiles in Y"
    )
