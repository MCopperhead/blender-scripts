bl_info = {
    "name": "UV Horizontal Island",
    "author": "Wayfaerer",
    "version": (1, 1),
    "blender": (2, 62, 0),
    "warning": "", 
    "category": "Mesh"}

import bpy
from bpy.props import *
from math import atan


def main():
    bpy.ops.object.mode_set(mode='OBJECT')
    me = bpy.context.active_object.data
    
    v1_coords = None
    v2_coords = None
    for f in me.polygons:
        for i in f.loop_indices:
            l = me.loops[i]
            ul = me.uv_layers.active
            cur_vertex = ul.data[l.index]
            if cur_vertex.select:
                if v1_coords:
                    if cur_vertex.uv == v1_coords:
                        cur_vertex.select = False
                    else:
                        v2_coords = cur_vertex.uv
                else:
                    v1_coords = cur_vertex.uv
                    cur_vertex.select = False
                                  
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.snap_cursor(target='SELECTED')
    bpy.context.space_data.pivot_point = "CURSOR"
    bpy.ops.uv.select_linked()
 
    diff_y = v1_coords.y - v2_coords.y
    diff_x = v1_coords.x - v2_coords.x
    angle = atan(diff_y/diff_x)
    bpy.ops.transform.rotate(value=angle)


class HorizontalIsland(bpy.types.Operator):
    bl_idname = "uv.uv_horizontal_island"
    bl_label = "UV Horizontal Island"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(HorizontalIsland.bl_idname)

addon_keymaps = []


def register():
    bpy.utils.register_class(HorizontalIsland)
    bpy.types.IMAGE_MT_uvs.append(menu_func)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.default.keymaps["Window"]

    kmi = km.keymap_items.new(HorizontalIsland.bl_idname, 'H', 'PRESS', ctrl=True, shift=True)

    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(HorizontalIsland)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
