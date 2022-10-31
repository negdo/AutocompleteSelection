from mimetypes import init
import bpy
import bmesh
from .overlays import OverlayAutocomplete
from .utils import *


class Autocomplete(bpy.types.Operator):
    bl_idname = "object.autocomplete"
    bl_label = "Autocomplete"
    bl_description = "Autocomplete selection of faces, edges and vertices"


    def execute(self, context):
        if context.mode != 'EDIT_MESH':
            return {'CANCELLED'}
        if not 'Autocomplete Utils' in bpy.data.node_groups.keys():
            bpy.ops.object.editmode_toggle()
            append_geo_nodes()
            bpy.ops.object.editmode_toggle()

        bm = bmesh.from_edit_mesh(context.active_object.data)
        layer = bm.faces.layers.int.get("AutocompleteSelect")
        overlay = OverlayAutocomplete(bm, layer, context)
        overlay.start()


        return {"FINISHED"}
