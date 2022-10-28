import numpy as np
import bmesh
from .utils import get_face_parameters, compare_parameters, avg_parameters
import bpy
from pathlib import Path
from bpy.utils import resource_path

class Mesh_checker():

    def __init__(self, context):
        self.last_selection = []
        self.context = context
        self.bm = bmesh.from_edit_mesh(context.active_object.data)
        self.mat = context.active_object.matrix_world
        try:
            self.geonodes_group = bpy.data.node_groups['Autocomplete Utils']
        except:
            self.append_geo_nodes()
            self.geonodes_group = bpy.data.node_groups['Autocomplete Utils']


    def check_for_changes(self):
        # checks if bmesh has changed
        # comparing vertex coordiantes and selection to last_selection
        self.bm.verts.ensure_lookup_table()

        new = str([(v.co, v.select) for v in self.bm.verts])
        if new != self.last_selection:
            self.last_selection = new
            return True
        return False

    def update_mesh_data(self):
        # update mesh data in layer
        print("update_mesh_data")
        
        self.bm.faces.ensure_lookup_table()
        self.bm.verts.ensure_lookup_table()

        layer = self.bm.faces.layers.int.get("AutocompleteSelect")
        if layer == None:
            layer = self.bm.faces.layers.int.new("AutocompleteSelect")
        self.bm.faces.ensure_lookup_table()

        parameters_faces = {
            "normal": [],
            "area": []
        }

        # get parameters of selected faces
        for face in self.bm.faces:
            if face.select:
                get_face_parameters(face, parameters_faces)

        # convert to numpy array
        for key in parameters_faces:
            parameters_faces[key] = np.array(parameters_faces[key])
        
        # calculate average of parameters
        avg, diff = avg_parameters(parameters_faces, np.ones(2), np.zeros(2))

        edges = []
        # compare average parameters with all faces and set layer
        for face in self.bm.faces:
            if not face.select and compare_parameters(face, avg, diff):
                face[layer] = 1
                # get edges of face for drawing
                for edge in face.edges:
                    edges.append(self.mat @ edge.verts[0].co)
                    edges.append(self.mat @ edge.verts[1].co)
                
            else:
                face[layer] = 0

        self.bm.faces.ensure_lookup_table()
        return edges

    def get_tris(self):
        # get triangles from bmesh
        layer = self.bm.faces.layers.int.get("AutocompleteSelect")
        tris = self.bm.calc_loop_triangles()
        tris_coords = []

        for triangle in tris:
            if triangle[0].face[layer] == 1:
                tris_coords.append(self.mat @ triangle[0].vert.co)
                tris_coords.append(self.mat @ triangle[1].vert.co)
                tris_coords.append(self.mat @ triangle[2].vert.co)

        return tris_coords

    
    def append_geo_nodes(self):
        # append geometry nodes group AutocompleteUtils
        print("Appending Autocomplete Utils")
        USER = Path(resource_path('USER'))
        src = USER / "scripts/addons"

        file_path = src / "AutocompleteUtils.blend"
        inner_path = "NodeTree"
        object_name = "Autocomplete Utils"

        bpy.ops.wm.append(
            filepath=str(file_path / inner_path / object_name),
            directory=str(file_path / inner_path),
            filename=object_name
        )