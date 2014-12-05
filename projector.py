bl_info = {
    "name": "Projector",
    "author": "Wayfaerer",
    "version": (1, 0),
    "blender": (2, 62, 0),
    "warning": "",
    "category": "Mesh"}

import bpy


def main(individuals):
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_target = 'CLOSEST'
    bpy.context.scene.tool_settings.snap_element = 'FACE'
    bpy.context.scene.tool_settings.use_snap_self = False
    if individuals:
        bpy.context.scene.tool_settings.use_snap_project = True
    else:
        bpy.context.scene.tool_settings.use_snap_project = False
    bpy.ops.object.modal_operator('INVOKE_DEFAULT')
    bpy.ops.transform.translate('INVOKE_DEFAULT',
                                constraint_axis=(False, False, True),
                                constraint_orientation='VIEW')


class ModalOperator(bpy.types.Operator):
    bl_idname = 'object.modal_operator'
    bl_label = 'Process Input'

    def modal(self, context, event):
        if event.type in ("RET", "LEFTMOUSE"):
            bpy.context.scene.tool_settings.use_snap = False
            bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
            bpy.context.scene.tool_settings.snap_element = 'VERTEX'
            bpy.context.scene.tool_settings.use_snap_self = True
            bpy.context.scene.tool_settings.use_snap_project = False
            return {'FINISHED'}
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class Individuals(bpy.types.Operator):
    bl_idname = "object.individuals"
    bl_label = "Individuals"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(individuals=True)
        return {'FINISHED'}


class Whole(bpy.types.Operator):
    bl_idname = "object.whole"
    bl_label = "Whole"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(individuals=False)
        return {'FINISHED'}


class Menu(bpy.types.Menu):
    bl_label = 'Projector'
    bl_idname = 'view3d.mymenu'

    def draw(self, context):
        self.layout.operator("object.individuals")
        self.layout.operator("object.whole")


def menu_func(self, context):
    self.layout.operator(Projector.bl_idname)

addon_keymaps = []


def register():
    bpy.utils.register_class(Individuals)
    bpy.utils.register_class(Whole)
    bpy.utils.register_class(ModalOperator)
    bpy.utils.register_class(Menu)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.default.keymaps["Window"]

    kmi = km.keymap_items.new("wm.call_menu", 'J', 'PRESS', ctrl=True)
    kmi.properties.name = "view3d.mymenu"
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(Projector)
    bpy.utils.unregister_class(ModalOperator)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()      
