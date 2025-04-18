# my_plugin/operators.py
import bpy

class GenerateGridOperator(bpy.types.Operator):
    bl_idname = "object.generate_map"
    bl_label = "Generate Map"
    bl_description = "Generate a tiled map centered at the origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.map_generator_props
        size = props.grid_size
        tiles_x = props.tiles_x
        tiles_y = props.tiles_y

        offset_x = (tiles_x * size) / 2
        offset_y = (tiles_y * size) / 2

        map_collection_name = "chunks"
        if map_collection_name in bpy.data.collections:
            map_collection = bpy.data.collections[map_collection_name]
        else:
            map_collection = bpy.data.collections.new(map_collection_name)
            bpy.context.scene.collection.children.link(map_collection)
        chunk_id = 1
        for x in range(tiles_x):
            for y in range(tiles_y):
                bpy.ops.mesh.primitive_plane_add(
                    size=size,
                    location=(
                        x * size - offset_x + size / 2,
                        y * size - offset_y + size / 2,
                        0
                    )
                )
                plane = context.active_object
                plane.name = f"chunk_{chunk_id}"
                plane["chunk_x"] = x
                plane["chunk_y"] = y
                plane["terrain_type"] = "grass"
                plane["walkable"] = True
                chunk_id += 1
        return {'FINISHED'}



