bl_info = {
    "name": "Kersed Scripts",
    "blender": (3, 0, 0),
    "category": "Object",
    "author": "Kersed",
    "description": "A collection of scripts.",
    "location": "F3 Menu > Kersed Scripts",
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

from . import gen_sierpinski_2d, gen_sierpinski_3d

def register():
    gen_sierpinski_2d.register()
    gen_sierpinski_3d.register()

def unregister():
    gen_sierpinski_2d.unregister()
    gen_sierpinski_3d.register()
    
if __name__ == "__main__":
    register()