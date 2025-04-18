bl_info = {
    "name": "Chunk Terrain Editor",
    "author": "You",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Chunk Tools",
    "description": "Generate grid-based chunks with terrain types and vegetation",
    "category": "Object",
}
# 调试配置
import sys
PYDEVD_PATH = r"C:/Users/tuwh/AppData/Local/Programs/Python/Python312/Lib/site-packages"
if PYDEVD_PATH not in sys.path:
    sys.path.append(PYDEVD_PATH)
import pydevd_pycharm
pydevd_pycharm.settrace(
    host='127.0.0.1',
    port=5678,
    stdoutToServer=True,
    stderrToServer=True,
    suspend=False
)

import bpy
from . import operators, ui, property


def register():
    property.register_props()
    operators.register()
    ui.register()


def unregister():
    operators.unregister()
    ui.unregister()
    property.unregister_props()


if __name__ == "__main__":
    register()
