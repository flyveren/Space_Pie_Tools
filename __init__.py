import bpy

bl_info = {
    "name": "Space Pie Tools",
    "author": "Flyveren",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "Spacebar",
    "description": "Pie Menu for Tools",
    "warning": "",
    "doc_url": "",
    "category": "Tools",
}


def _is_43_plus():
    return bpy.app.version >= (4, 3, 0)


class SPACEPIETOOLS_OT_activate_brush(bpy.types.Operator):
    """Activate a brush from the essentials asset library"""
    bl_idname = "spacepietools.activate_brush"
    bl_label = "Activate Brush"

    asset_path: bpy.props.StringProperty()

    def execute(self, context):
        print("[Space Pie Tools] Activating brush:", self.asset_path)
        try:
            bpy.ops.brush.asset_activate(
                asset_library_type='ESSENTIALS',
                asset_library_identifier="",
                relative_asset_identifier=self.asset_path,
            )
        except Exception as e:
            self.report({'WARNING'}, "Could not activate brush: " + str(e))
            print("[Space Pie Tools] ERROR:", e)
            return {'CANCELLED'}
        return {'FINISHED'}


def _brush_asset(pie, brush_name, blend_file, fallback_icon="NONE"):
    """Add a brush asset activation entry to the pie menu (Blender 4.3+)."""
    icon_value = 0
    brush = bpy.data.brushes.get(brush_name)
    if brush and brush.preview:
        icon_value = brush.preview.icon_id
    if icon_value:
        op = pie.operator("spacepietools.activate_brush", text=brush_name, icon_value=icon_value)
    else:
        try:
            op = pie.operator("spacepietools.activate_brush", text=brush_name, icon=fallback_icon)
        except TypeError:
            op = pie.operator("spacepietools.activate_brush", text=brush_name)
    op.asset_path = "brushes/" + blend_file + "/Brush/" + brush_name


class PAINT_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if context.mode == "PAINT_TEXTURE":
            return True

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _f = "essentials_brushes-mesh_texture.blend"
            _brush_asset(pie, "Paint Soft", _f)
            _brush_asset(pie, "Blend Soft", _f)
            pie.separator()
            pie.separator()
            _brush_asset(pie, "Paint Hard", _f)
            _brush_asset(pie, "Airbrush", _f)
            _brush_asset(pie, "Sharpen", _f)
            _brush_asset(pie, "Erase Soft", _f)
        else:
            pie.operator("wm.tool_set_by_id", text="Draw").name = "builtin_brush.Draw"
            pie.operator("wm.tool_set_by_id", text="Soften").name = "builtin_brush.Soften"
            pie.separator()
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Clone").name = "builtin_brush.Clone"
            pie.operator("wm.tool_set_by_id", text="Smear").name = "builtin_brush.Smear"
            pie.operator("wm.tool_set_by_id", text="Fill").name = "builtin_brush.Fill"
            pie.operator("wm.tool_set_by_id", text="Mask").name = "builtin_brush.Mask"



class VERTEX_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if context.mode == "PAINT_VERTEX":
            return True

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _f = "essentials_brushes-mesh_vertex.blend"
            _brush_asset(pie, "Paint Soft", _f)
            _brush_asset(pie, "Blend Soft", _f)
            _brush_asset(pie, "Paint Hard", _f)
            _brush_asset(pie, "Airbrush", _f)
        else:
            pie.operator("wm.tool_set_by_id", text="Draw").name = "builtin_brush.Draw"
            pie.operator("wm.tool_set_by_id", text="Blur").name = "builtin_brush.Blur"
            pie.operator("wm.tool_set_by_id", text="Average").name = "builtin_brush.Average"
            pie.operator("wm.tool_set_by_id", text="Smear").name = "builtin_brush.Smear"




class GREASEPENCIL_VERTEX_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if _is_43_plus():
            return context.mode == "VERTEX_GREASE_PENCIL"
        return context.mode == "VERTEX_GPENCIL"

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _f = "essentials_brushes-gp_vertex.blend"
            _brush_asset(pie, "Draw", _f)
            _brush_asset(pie, "Blur", _f)
            _brush_asset(pie, "Replace", _f)
            _brush_asset(pie, "Smear", _f)
        else:
            pie.operator("wm.tool_set_by_id", text="Draw").name = "builtin_brush.Draw"
            pie.operator("wm.tool_set_by_id", text="Blur").name = "builtin_brush.Blur"
            pie.operator("wm.tool_set_by_id", text="Replace").name = "builtin_brush.Replace"
            pie.operator("wm.tool_set_by_id", text="Smear").name = "builtin_brush.Smear"




class GREASEPENCIL_EDIT_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if _is_43_plus():
            return context.mode == "EDIT_GREASE_PENCIL"
        return context.mode == "EDIT_GPENCIL"

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("wm.tool_set_by_id", text="Select Box", icon="SELECT_SET").name = "builtin.select_box"
        pie.operator("wm.tool_set_by_id", text="Move", icon="EMPTY_ARROWS").name = "builtin.move"
        pie.operator("wm.tool_set_by_id", text="Rotate", icon="ORIENTATION_GIMBAL").name = "builtin.rotate"
        pie.operator("wm.tool_set_by_id", text="Scale", icon="CON_SIZELIKE").name = "builtin.scale"

        pie.operator("wm.tool_set_by_id", text="Radius").name = "builtin.radius"

        pie.operator("wm.tool_set_by_id", text="Interpolate").name = "builtin.interpolate"

        pie.operator("wm.tool_set_by_id", text="Extrude").name = "builtin.extrude"

        pie.operator("wm.tool_set_by_id", text="Transform Fill").name = "builtin.transform_fill"




class GREASEPENCIL_WEIGHT_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if _is_43_plus():
            return context.mode == "WEIGHT_GREASE_PENCIL"
        return context.mode == "WEIGHT_GPENCIL"

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _brush_asset(pie, "Weight", "essentials_brushes-gp_weight.blend")
        else:
            pie.operator("wm.tool_set_by_id", text="Weight").name = "builtin_brush.Weight"

class GREASEPENCIL_DRAW_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if _is_43_plus():
            return context.mode == "PAINT_GREASE_PENCIL"
        return context.mode == "PAINT_GPENCIL"

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _f = "essentials_brushes-gp_draw.blend"
            _brush_asset(pie, "Pencil", _f)
            pie.operator("wm.tool_set_by_id", text="Erase").name = "builtin.erase"
            pie.separator()
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Fill").name = "builtin.fill"
            pie.operator("wm.tool_set_by_id", text="Eyedropper").name = "builtin.eyedropper"
            _brush_asset(pie, "Tint", _f)
            pie.operator("wm.tool_set_by_id", text="Cutter").name = "builtin.cutter"
        else:
            pie.operator("wm.tool_set_by_id", text="Draw").name = "builtin_brush.Draw"
            pie.operator("wm.tool_set_by_id", text="Erase").name = "builtin_brush.Erase"
            pie.separator()
            #pie.prop(context.scene.tool_settings, "use_keyframe_insert_auto", text="Auto Key", icon="RADIOBUT_ON")
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Fill").name = "builtin_brush.Fill"
            pie.operator("wm.tool_set_by_id", text="Eyedropper").name = "builtin.eyedropper"
            pie.operator("wm.tool_set_by_id", text="Tint").name = "builtin_brush.Tint"
            pie.operator("wm.tool_set_by_id", text="Cutter").name = "builtin.cutter"

class GREASEPENCIL_SCULPT_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if _is_43_plus():
            return context.mode == "SCULPT_GREASE_PENCIL"
        return context.mode == "SCULPT_GPENCIL"

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _f = "essentials_brushes-gp_sculpt.blend"
            _brush_asset(pie, "Grab", _f)
            _brush_asset(pie, "Thickness", _f)
            _brush_asset(pie, "Randomize", _f)
            _brush_asset(pie, "Twist", _f)
            _brush_asset(pie, "Pull", _f)
            _brush_asset(pie, "Smooth", _f)
            _brush_asset(pie, "Pinch", _f)
            _brush_asset(pie, "Strength", _f)
        else:
            pie.operator("wm.tool_set_by_id", text="Grab").name = "builtin_brush.Grab"
            pie.operator("wm.tool_set_by_id", text="Thickness").name = "builtin_brush.Thickness"
            pie.operator("wm.tool_set_by_id", text="Randomize").name = "builtin_brush.Randomize"
            pie.operator("wm.tool_set_by_id", text="Twist").name = "builtin_brush.Twist"
            pie.operator("wm.tool_set_by_id", text="Push").name = "builtin_brush.Push"
            pie.operator("wm.tool_set_by_id", text="Smooth").name = "builtin_brush.Smooth"
            pie.operator("wm.tool_set_by_id", text="Pinch").name = "builtin.Pinch"
#           pie.operator("wm.tool_set_by_id", text="Clone").name = "builtin_brush.Clone"
            pie.operator("wm.tool_set_by_id", text="Strength").name = "builtin_brush.Strength"



class WEIGHT_MT_Tool_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if context.mode == "PAINT_WEIGHT":
            return True

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            _f = "essentials_brushes-mesh_weight.blend"
            _brush_asset(pie, "Draw", _f)
            _brush_asset(pie, "Blur", _f)
            pie.separator()
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Sample").name = "builtin.sample_weight"
            _brush_asset(pie, "Smear", _f)
            pie.operator("wm.tool_set_by_id", text="Gradient").name = "builtin.gradient"
            _brush_asset(pie, "Average", _f)
        else:
            pie.operator("wm.tool_set_by_id", text="Draw").name = "builtin_brush.Draw"
            pie.operator("wm.tool_set_by_id", text="Blur").name = "builtin_brush.Blur"
            pie.separator()
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Sample").name = "builtin.sample_weight"
            pie.operator("wm.tool_set_by_id", text="Smear").name = "builtin_brush.Smear"
            pie.operator("wm.tool_set_by_id", text="Gradient").name = "builtin.gradient"
            pie.operator("wm.tool_set_by_id", text="Average").name = "builtin_brush.Average"

class SCULPT_MT_Brush_Pie(bpy.types.Menu):

    bl_label = "Select Brush"

    @classmethod
    def poll(cls, context):
        if context.mode == "SCULPT":
            return True

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        if _is_43_plus():
            # Blender 4.3+ uses brush assets instead of builtin_brush tool IDs
            _f = "essentials_brushes-mesh_sculpt.blend"
            _brush_asset(pie, "Clay Strips", _f, "MOD_SOLIDIFY")
            _brush_asset(pie, "Crease Polish", _f, "SMOOTHCURVE")
            _brush_asset(pie, "Scrape/Fill", _f, "MESH_PLANE")
            _brush_asset(pie, "Grab", _f, "EMPTY_ARROWS")
            _brush_asset(pie, "Inflate/Deflate", _f, "MESH_UVSPHERE")
            _brush_asset(pie, "Draw Sharp", _f, "SHARPCURVE")
            _brush_asset(pie, "Flatten/Contrast", _f, "MESH_PLANE")
            _brush_asset(pie, "Pinch/Magnify", _f, "PINNED")
        else:
            # Blender 2.80 - 4.2 uses builtin_brush tool IDs
            pie.operator("wm.tool_set_by_id", text="Clay Strips", icon="BRUSH_CLAY_STRIPS").name = "builtin_brush.Clay Strips"
            pie.operator("wm.tool_set_by_id", text="Crease", icon="BRUSH_CREASE").name = "builtin_brush.Crease"
            pie.operator("wm.tool_set_by_id", text="Scrape", icon="BRUSH_SCRAPE").name = "builtin_brush.Scrape"
            pie.operator("wm.tool_set_by_id", text="Grab", icon="BRUSH_GRAB").name = "builtin_brush.Grab"
            pie.operator("wm.tool_set_by_id", text="Inflate", icon="BRUSH_INFLATE").name = "builtin_brush.Inflate"
            pie.operator("wm.tool_set_by_id", text="Draw Sharp", icon="BRUSH_SCULPT_DRAW").name = "builtin_brush.Draw Sharp"
            pie.operator("wm.tool_set_by_id", text="Blob", icon="BRUSH_BLOB").name = "builtin_brush.Blob"
            pie.operator("wm.tool_set_by_id", text="Pinch", icon="BRUSH_PINCH").name = "builtin_brush.Pinch"


class EDITMESH_MT_Tool_Pie(bpy.types.Menu):

    bl_label = "Select Tool"

    @classmethod
    def poll(cls, context):
        if context.mode == "EDIT_MESH":
            return True

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("wm.tool_set_by_id", text="Select Box", icon="SELECT_SET").name = "builtin.select_box"
        pie.operator("wm.tool_set_by_id", text="Extrude", icon="MOD_SOLIDIFY").name = "builtin.extrude_region"
        pie.operator("wm.tool_set_by_id", text="Rotate", icon="ORIENTATION_GIMBAL").name = "builtin.rotate"
        pie.operator("wm.tool_set_by_id", text="Scale", icon="CON_SIZELIKE").name = "builtin.scale"

        pie.operator("wm.tool_set_by_id", text="Move", icon="EMPTY_ARROWS").name = "builtin.move"
        pie.operator("wm.tool_set_by_id", text="Inset", icon="MOD_MESHDEFORM").name = "builtin.inset_faces"
        pie.operator("wm.tool_set_by_id", text="Loop Cut", icon="MOD_EDGESPLIT").name = "builtin.loop_cut"
        pie.operator("wm.tool_set_by_id", text="Bevel", icon="MOD_BEVEL").name = "builtin.bevel"


class OBJECT_MT_Tool_Pie(bpy.types.Menu):

    bl_label = "Select Tool"

    @classmethod
    def poll(cls, context):
        if context.mode in ["OBJECT", "POSE", "EDIT_CURVE", "EDIT_ARMATURE", "EDIT_LATTICE"]:
            return True

    def draw(self, context):

        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("wm.tool_set_by_id", text="Select Box", icon="SELECT_SET").name = "builtin.select_box"
        pie.operator("wm.tool_set_by_id", text="Move", icon="EMPTY_ARROWS").name = "builtin.move"

        if context.mode == "OBJECT":
            pie.operator("wm.tool_set_by_id", text="Measure", icon="DRIVER_DISTANCE").name = "builtin.measure"
        else:
            pie.operator("wm.tool_set_by_id", text="Rotate", icon="ORIENTATION_GIMBAL").name = "builtin.rotate"

        if context.mode == "OBJECT":
            pie.operator("wm.tool_set_by_id", text="Cursor", icon="PIVOT_CURSOR").name = "builtin.cursor"
        else:
            pie.operator("wm.tool_set_by_id", text="Scale", icon="CON_SIZELIKE").name = "builtin.scale"

        if context.mode == "OBJECT":
            pie.operator("wm.tool_set_by_id", text="Tweak", icon="RESTRICT_SELECT_OFF").name = "builtin.select"
            pie.operator("wm.tool_set_by_id", text="Scale", icon="CON_SIZELIKE").name = "builtin.scale"
            pie.operator("wm.tool_set_by_id", text="Select Circle", icon="MESH_CIRCLE").name = "builtin.select_circle"
            pie.operator("wm.tool_set_by_id", text="Rotate", icon="ORIENTATION_GIMBAL").name = "builtin.rotate"

        if context.mode == "EDIT_ARMATURE":
            pie.operator("wm.tool_set_by_id", text="Bone Size").name = "builtin.bone_size"
            pie.operator("wm.tool_set_by_id", text="Extrude").name = "builtin.extrude"
            pie.operator("wm.tool_set_by_id", text="Bone Roll").name = "builtin.roll"
            pie.operator("wm.tool_set_by_id", text="Shear").name = "builtin.shear"

        if context.mode == "POSE":
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Breakdowner").name = "builtin.breakdowner"

        if context.mode == "EDIT_LATTICE":
            pie.separator()
            pie.separator()
            pie.separator()
            pie.operator("wm.tool_set_by_id", text="Shear").name = "builtin.shear"


        if context.mode == "EDIT_CURVE":
            pie.operator("wm.tool_set_by_id", text="Radius").name = "builtin.radius"
            pie.operator("wm.tool_set_by_id", text="Draw").name = "builtin.draw"
            pie.operator("wm.tool_set_by_id", text="Tilt").name = "builtin.tilt"
            pie.operator("wm.tool_set_by_id", text="Extrude").name = "builtin.extrude"

classes = [SPACEPIETOOLS_OT_activate_brush, VERTEX_MT_Brush_Pie, PAINT_MT_Brush_Pie, WEIGHT_MT_Tool_Pie, GREASEPENCIL_VERTEX_MT_Brush_Pie, GREASEPENCIL_EDIT_MT_Brush_Pie, GREASEPENCIL_WEIGHT_MT_Brush_Pie, GREASEPENCIL_SCULPT_MT_Brush_Pie, GREASEPENCIL_DRAW_MT_Brush_Pie, SCULPT_MT_Brush_Pie, EDITMESH_MT_Tool_Pie, OBJECT_MT_Tool_Pie]

addon_keymaps = []

def register():

    for cls in classes:
        bpy.utils.register_class(cls)



    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "SCULPT_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])

        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "EDITMESH_MT_Tool_Pie"
        addon_keymaps.append([km, kmi])

        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "OBJECT_MT_Tool_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "WEIGHT_MT_Tool_Pie"
        addon_keymaps.append([km, kmi])

        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "GREASEPENCIL_DRAW_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "GREASEPENCIL_SCULPT_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "GREASEPENCIL_WEIGHT_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "GREASEPENCIL_EDIT_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "GREASEPENCIL_VERTEX_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "PAINT_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])


        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu_pie", type="SPACE", value="PRESS")
        kmi.properties.name = "VERTEX_MT_Brush_Pie"
        addon_keymaps.append([km, kmi])

def unregister():


    for cls in classes:
        bpy.utils.unregister_class(cls)


    addon_keymaps.clear()

if __name__ == "__main__":
    register()
