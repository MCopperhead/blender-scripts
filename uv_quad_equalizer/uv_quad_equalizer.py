bl_info = {
    "name": "UV Quad Equalizer",
    "author": "Wayfaerer",
    "version": (1, 1),
    "blender": (2, 62, 0),
    "warning": "", 
    "category": "Mesh",
    #TODO: translate description to English and add details to the README file.
    "description": "Выравнивает по вертикали и горизонтали выделенный в UV развёртке фейс,"
                   " и потом выполняет Follow Active Quads"}

import bpy
from bpy.props import *


def main():
    bpy.ops.object.mode_set(mode='OBJECT') # Can't access coordinate data in edit mode currently 
    me = bpy.context.active_object.data
    polys = dict()
    selected_verts = []

    for f in me.polygons:
        polys[f] = []
        for i in f.loop_indices:  # <-- python Range object with the proper indices already set
            l = me.loops[i]  # The loop entry this polygon point refers to
            ul = me.uv_layers.active
            cur_vertex = ul.data[l.index]
            if cur_vertex.select:
                polys[f].append(cur_vertex)
                selected_verts.append(cur_vertex)

    for poly in polys.values():
        prev_vertex = None
        if len(poly) == 4:    
            poly.append(poly[0])
            for vertex in poly:
                if prev_vertex is not None:                
                    diff_x = abs(prev_vertex.uv.x - vertex.uv.x)
                    diff_y = abs(prev_vertex.uv.y - vertex.uv.y)
                    if diff_x < diff_y:
                        for selected_vert in selected_verts:
                            if selected_vert.uv == vertex.uv and selected_vert is not vertex:
                                selected_vert.uv.x = prev_vertex.uv.x
                        vertex.uv.x = prev_vertex.uv.x
                    elif diff_x > diff_y:
                        for selected_vert in selected_verts:
                            if selected_vert.uv == vertex.uv and selected_vert is not vertex:
                                selected_vert.uv.y = prev_vertex.uv.y
                        vertex.uv.y = prev_vertex.uv.y
                prev_vertex = vertex                         

    bpy.ops.object.mode_set(mode='EDIT')
    try:
        bpy.ops.uv.follow_active_quads()
    except:
        bpy.ops.error.message('INVOKE_DEFAULT', message = "Do you have active face?")


class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    message = StringProperty()
 
    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=200)
 
    def draw(self, context):
        self.layout.label("Error")
        row = self.layout
        row.prop(self, "message")
        row.operator("error.ok")
 
 
class OkOperator(bpy.types.Operator):
    bl_idname = "error.ok"
    bl_label = "OK"

    def execute(self, context):
        return {'FINISHED'}


class QuadEqualizer(bpy.types.Operator):
    bl_idname = "uv.uv_quad_equalizer"
    bl_label = "UV Quad Equalizer"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(QuadEqualizer.bl_idname)


addon_keymaps = []


def register():
    bpy.utils.register_class(OkOperator)
    bpy.utils.register_class(MessageOperator)
    bpy.utils.register_class(QuadEqualizer)
    bpy.types.IMAGE_MT_uvs.append(menu_func)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.default.keymaps["Window"]

    kmi = km.keymap_items.new(QuadEqualizer.bl_idname, 'E', 'PRESS', ctrl=True, shift=True)

    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(QuadEqualizer)
    bpy.utils.unregister_class(OkOperator)
    bpy.utils.unregister_class(MessageOperator)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
