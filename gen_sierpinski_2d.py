import bpy
import math
import mathutils

def create_triangle(v0, v1, v2, depth, scale):
    if depth == 0:
        vertices = [v0, v1, v2]
        edges = []
        faces = [(0, 1, 2)]
        mesh = bpy.data.meshes.new(name="Triangle")
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()
        obj = bpy.data.objects.new("Triangle", mesh)
        bpy.context.collection.objects.link(obj)
        return

    # Convert to Vector for arithmetic operations
    v0, v1, v2 = mathutils.Vector(v0), mathutils.Vector(v1), mathutils.Vector(v2)

    # Calculate the midpoints of the triangle
    mid01 = (v0 + v1) / 2
    mid12 = (v1 + v2) / 2
    mid20 = (v2 + v0) / 2

    # Create three smaller triangles at each corner
    create_triangle(v0, mid01, mid20, depth - 1, scale)
    create_triangle(mid01, v1, mid12, depth - 1, scale)
    create_triangle(mid20, mid12, v2, depth - 1, scale)

# Define the Sierpinski 2D Generator Operator
class Sierpinski2DOperator(bpy.types.Operator):
    bl_idname = "mesh.sierpinski_2d_generator"
    bl_label = "Generate Sierpinski 2D"
    bl_options = {'REGISTER', 'UNDO'}

    sierpinski_depth: bpy.props.IntProperty(
        name="Depth",
        description="Specify the depth of the Sierpinski 2D Generator",
        min=0,
        max=10,
        default=3
    )

    orientation: bpy.props.EnumProperty(
        name="Orientation",
        description="Select the orientation/plane to generate on",
        items=[
            ('XY', 'XY Plane', 'Generate on XY Plane'),
            ('XZ', 'XZ Plane', 'Generate on XZ Plane'),
            ('YZ', 'YZ Plane', 'Generate on YZ Plane')
        ],
        default='XY'
    )

    scale: bpy.props.FloatProperty(
        name="Scale",
        description="Specify the scale factor for the generated shape",
        min=0.1,
        max=10,
        default=1.0
    )

    def execute(self, context):
        # Create the Sierpinski 2D shape using the specified parameters
        scale = self.scale
        if self.orientation == 'XY':
            create_triangle((-1 * scale, 0, 0), (1 * scale, 0, 0), (0, math.sqrt(3) * scale, 0), self.sierpinski_depth, scale)
        elif self.orientation == 'XZ':
            create_triangle((-1 * scale, 0, 0), (1 * scale, 0, 0), (0, 0, math.sqrt(3) * scale), self.sierpinski_depth, scale)
        elif self.orientation == 'YZ':
            create_triangle((0, -1 * scale, 0), (0, 1 * scale, 0), (0, 0, math.sqrt(3) * scale), self.sierpinski_depth, scale)

        return {'FINISHED'}

# Register and add to the "add mesh" menu.
def register():
    bpy.utils.register_class(Sierpinski2DOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Sierpinski2DOperator)

def menu_func(self, context):
    layout = self.layout
    layout.operator(Sierpinski2DOperator.bl_idname)

if __name__ == "__main__":
    register()
