import numpy as np
import bmesh
from .utils import get_face_parameters, compare_parameters, avg_parameters

class Mesh_checker():

    def __init__(self, context):
        self.last_selection = []
        self.context = context
        self.bm = bmesh.from_edit_mesh(context.active_object.data)


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
                    edges.append(edge.verts[0].co)
                    edges.append(edge.verts[1].co)
                
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
                tris_coords.append(triangle[0].vert.co)
                tris_coords.append(triangle[1].vert.co)
                tris_coords.append(triangle[2].vert.co)

        return tris_coords