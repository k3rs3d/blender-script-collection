import bpy
import math

# Get a reference to the active objects in the scene
objs = bpy.context.selected_objects

# Make sure at least one object is selected
if len(objs) == 0:
    raise Exception("No objects are selected!")

# Set the start and end frames for the animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120

# Set the current frame to the start of the animation
bpy.context.scene.frame_current = 1

# Set the initial scale of the objects to 1
for obj in objs:
    obj.scale = (1, 1, 1)

# Animate the objects over the course of the animation
for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
    bpy.context.scene.frame_current = frame

    # Calculate the scale factor based on the current frame
    scale_factor = math.sin(frame / 30)

    # Scale the objects along the Y axis by the calculated factor
    for obj in objs:
        obj.scale[1] = scale_factor

        # Add a new animation keyframe at the current frame
        obj.keyframe_insert(data_path="scale")
