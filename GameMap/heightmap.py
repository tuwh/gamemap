import bpy
import bmesh
import numpy as np
from mathutils import Vector

def load_heightmap_image(path):
    img = bpy.data.images.load(path)
    pixels = np.array(img.pixels[:])
    pixels = pixels[::4]  # 只取 R 分量
    pixels = np.reshape(pixels, (img.size[1], img.size[0]))  # 高度图是 height x width
    return pixels, img.size

def apply_heightmap_to_chunk(obj, height_data, img_size, height_scale=1.0):
    if obj.type != 'MESH':
        return

    # 细分平面
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=50)
    bpy.ops.object.mode_set(mode='OBJECT')

    # 获取 bounding box 尺寸
    bounds = obj.bound_box
    min_x = min(v[0] for v in bounds)
    max_x = max(v[0] for v in bounds)
    min_y = min(v[1] for v in bounds)
    max_y = max(v[1] for v in bounds)

    width = max_x - min_x
    height = max_y - min_y

    for v in obj.data.vertices:
        vx = (v.co.x - min_x) / width
        vy = (v.co.y - min_y) / height
        px = int(vx * (img_size[0] - 1))
        py = int(vy * (img_size[1] - 1))
        value = height_data[py][px]
        v.co.z = value * height_scale


def apply_heightmap_to_chunks(objs, height_data, img_size, height_scale=1.0):
    # Step 1: 计算整个区域的边界
    all_coords = [Vector((obj.location.x, obj.location.y)) for obj in objs]
    min_x = min(v.x for v in all_coords)
    max_x = max(v.x for v in all_coords)
    min_y = min(v.y for v in all_coords)
    max_y = max(v.y for v in all_coords)
    total_width = max_x - min_x
    total_height = max_y - min_y

    for obj in objs:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=50)
        bpy.ops.object.mode_set(mode='OBJECT')

        # 每个 chunk 局部顶点根据全局位置去取图像采样
        bounds = obj.bound_box
        obj_min_x = min(v[0] for v in bounds) + obj.location.x
        obj_max_x = max(v[0] for v in bounds) + obj.location.x
        obj_min_y = min(v[1] for v in bounds) + obj.location.y
        obj_max_y = max(v[1] for v in bounds) + obj.location.y
        obj_width = obj_max_x - obj_min_x
        obj_height = obj_max_y - obj_min_y

        for v in obj.data.vertices:
            world_x = obj.matrix_world @ v.co
            tx = (world_x.x - min_x) / total_width
            ty = (world_x.y - min_y) / total_height
            px = int(tx * (img_size[0] - 1))
            py = int(ty * (img_size[1] - 1))
            if 0 <= px < img_size[0] and 0 <= py < img_size[1]:
                value = height_data[py][px]
                v.co.z = value * height_scale