from mimetypes import init
import bpy
import bmesh
from .overlays import OverlayAutocomplete


class Autocomplete(bpy.types.Operator):
    bl_idname = "object.autocomplete"
    bl_label = "Autocomplete"
    bl_description = "Autocomplete selection of faces, edges and vertices"


    def execute(self, context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        layer = bm.faces.layers.int.get("AutocompleteSelect")
        overlay = OverlayAutocomplete(bm, layer, context)
        overlay.start()


        return {"FINISHED"}
