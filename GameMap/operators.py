import bpy
import random
from bpy.types import Operator
from bpy.props import IntProperty, StringProperty
from mathutils import Vector, Euler

from bpy.props import StringProperty, FloatProperty
from .heightmap import apply_heightmap_to_chunks, load_heightmap_image


class OBJECT_OT_apply_heightmap(Operator):
    bl_idname = "object.apply_heightmap"
    bl_label = "Apply Heightmap to Chunks"
    bl_description = "Apply a heightmap to selected chunks and create continuous terrain"

    filepath: StringProperty(subtype="FILE_PATH")
    height_scale: FloatProperty(name="Height Scale", default=1.0)

    def execute(self, context):
        selected_chunks = [
            obj for obj in context.selected_objects
            if obj.type == 'MESH' and obj.name.startswith("chunk_")
        ]

        if not selected_chunks:
            self.report({'WARNING'}, "Please select at least one chunk.")
            return {'CANCELLED'}

        height_data, img_size = load_heightmap_image(self.filepath)
        apply_heightmap_to_chunks(selected_chunks, height_data, img_size, self.height_scale)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OBJECT_OT_generate_chunks(Operator):
    bl_idname = "object.generate_chunks"
    bl_label = "Generate Chunk Grid"

    def execute(self, context):
        props = context.scene.chunk_props
        size = props.chunk_size
        count_x = props.count_x
        count_y = props.count_y

        if "chunks" not in bpy.data.collections:
            chunk_collection = bpy.data.collections.new("chunks")
            context.scene.collection.children.link(chunk_collection)
        else:
            chunk_collection = bpy.data.collections["chunks"]

        for obj in bpy.context.selected_objects:
            obj.select_set(False)

        for x in range(count_x):
            for y in range(count_y):
                bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False)
                plane = context.active_object
                plane.name = f"chunk_{x}_{y}"
                plane.location = (
                    (x - count_x / 2 + 0.5) * size,
                    (y - count_y / 2 + 0.5) * size,
                    0
                )
                chunk_collection.objects.link(plane)
                # context.scene.collection.objects.unlink(plane)

                plane["chunk_x"] = x
                plane["chunk_y"] = y
                plane["walkable"] = True
                plane.terrain_type = "GRASS"

        return {'FINISHED'}


class OBJECT_OT_scatter_props(Operator):
    bl_idname = "object.scatter_props"
    bl_label = "Scatter Props on Chunk"
    bl_description = "Randomly scatter props like trees, rocks, etc. onto the selected chunks"

    density: IntProperty(name="Density", default=30, min=1, max=500)
    asset_collection: StringProperty(name="Asset Collection", default="map_reference")

    def execute(self, context):
        asset_coll = bpy.data.collections.get(self.asset_collection)
        if not asset_coll:
            self.report({'ERROR'}, f"Collection '{self.asset_collection}' not found.")
            return {'CANCELLED'}

        selected_chunks = [
            obj for obj in context.selected_objects
            if obj.type == 'MESH' and obj.name.startswith("chunk_")
        ]
        if not selected_chunks:
            self.report({'WARNING'}, "No valid chunks selected.")
            return {'CANCELLED'}

        for chunk in selected_chunks:
            self.scatter_on_chunk(chunk, asset_coll)

        return {'FINISHED'}

    def scatter_on_chunk(self, chunk, asset_coll):
        bounds = chunk.bound_box
        min_x = min([v[0] for v in bounds]) + chunk.location.x
        max_x = max([v[0] for v in bounds]) + chunk.location.x
        min_y = min([v[1] for v in bounds]) + chunk.location.y
        max_y = max([v[1] for v in bounds]) + chunk.location.y

        for _ in range(self.density):
            source_obj = random.choice(asset_coll.objects)
            new_obj = source_obj.copy()
            new_obj.data = source_obj.data.copy()
            new_obj.animation_data_clear()
            bpy.context.collection.objects.link(new_obj)

            pos_x = random.uniform(min_x, max_x)
            pos_y = random.uniform(min_y, max_y)
            pos_z = chunk.location.z

            new_obj.location = Vector((pos_x, pos_y, pos_z))
            new_obj.rotation_euler = Euler((0, 0, random.uniform(0, 3.14)), 'XYZ')
            scale = random.uniform(0.8, 1.5)
            new_obj.scale = Vector((scale, scale, scale))
            new_obj.parent = chunk


classes = [
    OBJECT_OT_generate_chunks,
    OBJECT_OT_scatter_props,
    OBJECT_OT_apply_heightmap
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
