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


# Define the Sierpinski 3D Generator Operator
class Sierpinski3DGeneratorOperator(bpy.types.Operator):
    bl_idname = "mesh.sierpinski_3d_generator"
    bl_label = "Generate Sierpinski 3D"
    bl_options = {'REGISTER', 'UNDO'}

    sierpinski_depth: bpy.props.IntProperty(
        name="Depth",
        description="Specify the depth of the Sierpinski 3D Generator",
        min=0,
        max=5,  # Adjust the maximum depth as needed
        default=3
    )

    scale: bpy.props.FloatProperty(
        name="Scale",
        description="Specify the scale factor for the generated shape",
        min=0.1,
        max=10,
        default=1.0
    )

    def execute(self, context):
        # Define the vertices of an initial tetrahedron
        v0 = (0, 0, 1 * self.scale)
        v1 = (1 * self.scale, 0, -1 * self.scale)
        v2 = (-0.5 * self.scale, math.sqrt(3) * 0.5 * self.scale, -1 * self.scale)
        v3 = (-0.5 * self.scale, -math.sqrt(3) * 0.5 * self.scale, -1 * self.scale)

        # Create the Sierpinski 3D shape using the specified parameters
        create_tetrahedron(v0, v1, v2, v3, self.sierpinski_depth, self.scale)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "sierpinski_depth")
        layout.prop(self, "scale")


# Register and add to the "add mesh" menu.
def register():
    bpy.utils.register_class(Sierpinski3DGeneratorOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(Sierpinski3DGeneratorOperator)


def menu_func(self, context):
    layout = self.layout
    layout.operator(Sierpinski3DGeneratorOperator.bl_idname)


if __name__ == "__main__":
    register()
