import bpy
from .myaddon_preferences import *
from .grid_gen_operator import *
from .map_generator_properties import *
from .pannel import *
from .chunk_properties import *
bl_info = {
    "name": 'GameMap',
    "author": "[tuwh]",
    "blender": (4, 0, 0),
    "version": (0, 0, 1),
    "description": "这是一个地图编辑器",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "3D View"
}

dictionary = {
    "zh_CN": {
        ("*", "Example Addon Side Bar Panel"): "示例插件面板",
        ("*", "Example Functions"): "示例功能",
        ("*", "MapAddon"): "地图编辑",
        ("*", "Resource Folder"): "资源文件夹",
        ("*", "Int Config"): "整数参数",
        ("*", "Boolean Config"): "布尔参数",
        # This is not a standard way to define a translation, but it is still supported with preprocess_dictionary.
        # "Boolean Config": "布尔参数",
        # "Second Panel": "第二面板",
        # "GameMap": "地图",
        ("*", "Add-on Preferences View"): "插件设置面板",
        ("Operator", "ExampleOperator"): "示例操作",
    }
}

dictionary["zh_HANS"] = dictionary["zh_CN"]

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


def register():
    bpy.utils.register_class(MapPanel)
    bpy.utils.register_class(MyAddonPreferences)
    bpy.utils.register_class(GenerateGridOperator)
    bpy.utils.register_class(MapGeneratorProperties)
    bpy.utils.register_class(ChunkPropertiesPanel)
    bpy.types.Scene.map_generator_props = bpy.props.PointerProperty(type=MapGeneratorProperties)
    bpy.app.translations.register(bl_info["name"], dictionary)
    print("地图绘制插件已加载")

def unregister():
    bpy.app.translations.unregister(bl_info["name"])
    bpy.utils.unregister_class(MapPanel)
    bpy.utils.unregister_class(MyAddonPreferences)
    bpy.utils.unregister_class(GenerateGridOperator)
    bpy.utils.unregister_class(MapGeneratorProperties)
    bpy.utils.unregister_class(ChunkPropertiesPanel)
    print("地图绘制插件已卸载")

