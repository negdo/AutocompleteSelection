import bpy

class Autocomplete(bpy.types.Operator):
    bl_idname = "object.autocomplete"
    bl_label = "Autocomplete"
    bl_description = "Autocomplete selection of faces, edges and vertices"

    def execute(self, context):
        pass

        return {"FINISHED"}
