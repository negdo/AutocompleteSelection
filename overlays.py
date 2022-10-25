# manages overlays showing suggested autocomplete

import bpy
import bmesh
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from struct import pack
from .mesh_checker import Mesh_checker

class OverlayAutocomplete():
    def __init__(self, bm, layer, context):
        bgl.glEnable(bgl.GL_DEPTH_TEST)
        self.shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
        self.bm = bm
        self.layer = layer
        self.handler = None
        self.faces_to_draw = []
        self.context = context
        self.mesh_checker = Mesh_checker(context)

    def start(self):
        self.handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (), 'WINDOW', 'POST_VIEW')

    def stop(self):
        try:
            bpy.types.SpaceView3D.draw_handler_remove(self.handler, 'WINDOW')
        except:
            print("Canno't remove handler")

    def draw_callback(self):
        # check for changes and apply them to mesh
        # TODO
        #print("draw_callback")
        if self.mesh_checker.check_for_changes():
            self.mesh_checker.update_mesh_data()
            self.faces_to_draw = self.mesh_checker.get_tris()

        batch = batch_for_shader(self.shader, 'TRIS', {"pos": self.faces_to_draw})
        self.shader.bind()
        color = self.shader.uniform_from_name("color")
        self.shader.uniform_vector_float(color, pack("4f", 0.6, 0.6, 0.1, 1.0), 4)
        batch.draw(self.shader)