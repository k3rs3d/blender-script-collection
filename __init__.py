bl_info = {
    "name": "Kersed Scripts",
    "blender": (3, 0, 0),
    "category": "Object",
    "author": "Kersed",
    "description": "A collection of scripts by Kersed.",
    "location": "Add > Mesh > Kersed",
    "version": (0, 1, 0),
    "support": "COMMUNITY",
}

import bpy, os, sys

# Add the addon directory to the Python path
addon_directory = os.path.dirname(os.path.realpath(__file__))
addon_parent_directory = os.path.dirname(addon_directory)
if addon_parent_directory not in sys.path:
    sys.path.append(addon_parent_directory)

# Add the 'lib' directory to the Python path
lib_directory = os.path.join(addon_directory, "lib")
if lib_directory not in sys.path:
    sys.path.append(lib_directory)
    
    
class KersedSubMenu(bpy.types.Menu):
    bl_label = "Kersed"
    bl_idname = "VIEW3D_MT_mesh_add_kersed"

    def draw(self, context):
        layout = self.layout
        # Populate the menu based on enabled generators
        prefs = bpy.context.preferences.addons[__name__].preferences
        if prefs.enable_sierpinski:
            layout.operator("mesh.sierpinski_generator")
        # other generators later
        
def add_kersed_menu(self, context):
    layout = self.layout
    layout.menu("VIEW3D_MT_mesh_add_kersed")


from . import gen_sierpinski

class KersedGeneratorsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    enable_sierpinski: bpy.props.BoolProperty(
        name="Enable Sierpinski Gen",
        default=True,
    )

    # other preferences for other generators (later)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "enable_sierpinski")
        # other generators later


def register():
    # Register the common menu
    bpy.utils.register_class(KersedSubMenu)
    bpy.types.VIEW3D_MT_mesh_add.append(add_kersed_menu)

    # Check preferences and only register enabled generators
    bpy.utils.register_class(KersedGeneratorsPreferences)
    prefs = bpy.context.preferences.addons[__name__].preferences

    if prefs.enable_sierpinski:
        gen_sierpinski.register()

def unregister():
    gen_sierpinski.unregister()
    
    bpy.types.VIEW3D_MT_mesh_add.remove(add_kersed_menu)
    bpy.utils.unregister_class(KersedSubMenu)
    bpy.utils.unregister_class(KersedGeneratorsPreferences)
    
if __name__ == "__main__":
    register()