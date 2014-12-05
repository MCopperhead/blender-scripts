bl_info = {
    "name": "Align Vertices",
    "author": "Wayfaerer",
    "version": (1, 0),
    "blender": (2, 62, 0),
    "warning": "",
    "category": "Mesh",
    #TODO: translate description to English and add details to the README file.
    "description": "В 3D View выравнивает выделенный ряд вершин по крайним вершинам." }

import bpy
from mathutils import Euler


class AlignVertices(bpy.types.Operator):
    bl_idname = "object.align_vertices"
    bl_label = "Align Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    constraint_axis = bpy.props.BoolVectorProperty(name="Constraint Axis",
                                                   subtype="XYZ")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print(bpy.context.space_data.region_3d.view_rotation.to_euler())
        view_top = Euler((0, 0, 0))
        view_front = Euler((1.5707963705062866, 0, 0))
        view_right = Euler((1.570796251296997, 0, 1.570796251296997))
        view_bottom = Euler((3.1415927410125732, 0, 0))
        view_left = Euler((1.570796251296997, 0, -1.570796251296997))
        view_back = Euler((1.5708, 0, 3.1415927410125732))

        viewport_direction = bpy.context.space_data.region_3d.view_rotation.to_euler()

        bpy.ops.object.mode_set(mode='OBJECT')
        me = bpy.context.active_object.data

        selected_verts = [v for v in me.vertices if v.select]
        edges = [e for e in me.edges if e.select]

        utmost_vertices = []

        for e in edges:
            for i in e.vertices:
                if me.vertices[i] in utmost_vertices:
                    utmost_vertices.remove(me.vertices[i])
                else:
                    utmost_vertices.append(me.vertices[i])

        for vert in selected_verts:
            if vert not in utmost_vertices:
                if self.constraint_axis[0]:
                    if viewport_direction in (view_top, view_bottom):
                        h1 = utmost_vertices[0].co.y
                        h2 = utmost_vertices[1].co.y
                        h = vert.co.y
                    else:
                        h1 = utmost_vertices[0].co.z
                        h2 = utmost_vertices[1].co.z
                        h = vert.co.z
                    v1 = utmost_vertices[0].co.x
                    v2 = utmost_vertices[1].co.x
                    vert.co.x = ((h - h1) * (v2 - v1)) / (h2 - h1) + v1
                if self.constraint_axis[1]:
                    if viewport_direction in (view_top, view_bottom):
                        h1 = utmost_vertices[0].co.x
                        h2 = utmost_vertices[1].co.x
                        h = vert.co.x
                    else:
                        h1 = utmost_vertices[0].co.z
                        h2 = utmost_vertices[1].co.z
                        h = vert.co.z
                    v1 = utmost_vertices[0].co.y
                    v2 = utmost_vertices[1].co.y
                    vert.co.y = ((h - h1) * (v2 - v1)) / (h2 - h1) + v1
                if self.constraint_axis[2]:
                    if viewport_direction in (view_front, view_back):
                        h1 = utmost_vertices[0].co.x
                        h2 = utmost_vertices[1].co.x
                        h = vert.co.x
                    else:
                        h1 = utmost_vertices[0].co.y
                        h2 = utmost_vertices[1].co.y
                        h = vert.co.y
                    v1 = utmost_vertices[0].co.z
                    v2 = utmost_vertices[1].co.z
                    vert.co.z = ((h - h1) * (v2 - v1)) / (h2 - h1) + v1

        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

addon_keymaps = []


class AlignTools(bpy.types.Panel):
    bl_idname = "OBJECT_PT_align_tools"
    bl_label = "Align Tools"
    bl_description = "Align Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        self.layout.operator("object.align_vertices")


def register():
    bpy.utils.register_class(AlignVertices)
    bpy.utils.register_class(AlignTools)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.default.keymaps["Window"]

    kmi = km.keymap_items.new(AlignVertices.bl_idname, 'A', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(AlignVertices)
    bpy.utils.unregister_class(AlignTools)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear() 