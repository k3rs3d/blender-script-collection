import bpy
import math
import mathutils


def create_tetrahedron(v0, v1, v2, v3, depth, scale):
    if depth == 0:
        vertices = [v0, v1, v2, v3]
        edges = []
        faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
        mesh = bpy.data.meshes.new(name="Tetrahedron")
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()
        obj = bpy.data.objects.new("Tetrahedron", mesh)
        bpy.context.collection.objects.link(obj)
        return

    # Convert to Vector for arithmetic operations
    v0, v1, v2, v3 = mathutils.Vector(v0), mathutils.Vector(v1), mathutils.Vector(v2), mathutils.Vector(v3)

    # Calculate the midpoints of the edges
    mid01 = (v0 + v1) / 2
    mid02 = (v0 + v2) / 2
    mid03 = (v0 + v3) / 2
    mid12 = (v1 + v2) / 2
    mid13 = (v1 + v3) / 2
    mid23 = (v2 + v3) / 2

    # Create four smaller tetrahedrons at each corner
    create_tetrahedron(v0, mid01, mid02, mid03, depth - 1, scale)
    create_tetrahedron(mid01, v1, mid12, mid13, depth - 1, scale)
    create_tetrahedron(mid02, mid12, v2, mid23, depth - 1, scale)
    create_tetrahedron(mid03, mid13, mid23, v3, depth - 1, scale)
    
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


# Define the Sierpinski 3D Generator Operator
class SierpinskiGeneratorOperator(bpy.types.Operator):
    bl_idname = "mesh.sierpinski_generator"
    bl_label = "Generate Sierpinski"
    bl_options = {'REGISTER', 'UNDO'}

    sierpinski_depth: bpy.props.IntProperty(
        name="Depth",
        description="Specify the depth of the Sierpinski Generator",
        min=0,
        max=10,
        default=3
    )

    scale: bpy.props.FloatProperty(
        name="Scale",
        description="Specify the scale factor for the generated shape",
        min=0.1,
        max=10,
        default=1.0
    )

    mode: bpy.props.EnumProperty(
        name="Mode",
        description="Select 2D or 3D mode",
        items=[
            ('2D', '2D', '2D Sierpinski'),
            ('3D', '3D', '3D Sierpinski')
        ],
        default='3D'
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

    def execute(self, context):
        if self.mode == '3D':
            v0 = (0, 0, 1 * self.scale)
            v1 = (1 * self.scale, 0, -1 * self.scale)
            v2 = (-0.5 * self.scale, math.sqrt(3) * 0.5 * self.scale, -1 * self.scale)
            v3 = (-0.5 * self.scale, -math.sqrt(3) * 0.5 * self.scale, -1 * self.scale)
            create_tetrahedron(v0, v1, v2, v3, self.sierpinski_depth, self.scale)
        else:
            scale = self.scale
            if self.orientation == 'XY':
                create_triangle((-1 * scale, 0, 0), (1 * scale, 0, 0), (0, math.sqrt(3) * scale, 0), self.sierpinski_depth, scale)
            elif self.orientation == 'XZ':
                create_triangle((-1 * scale, 0, 0), (1 * scale, 0, 0), (0, 0, math.sqrt(3) * scale), self.sierpinski_depth, scale)
            elif self.orientation == 'YZ':
                create_triangle((0, -1 * scale, 0), (0, 1 * scale, 0), (0, 0, math.sqrt(3) * scale), self.sierpinski_depth, scale)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mode")
        layout.prop(self, "sierpinski_depth")
        layout.prop(self, "scale")
        if self.mode == '2D':
            layout.prop(self, "orientation")


# Register and add to the "add mesh" menu.
def register():
    bpy.utils.register_class(SierpinskiGeneratorOperator)


def unregister():
    bpy.utils.unregister_class(SierpinskiGeneratorOperator)

if __name__ == "__main__":
    register()
