# manages overlays showing suggested autocomplete

import bpy
import bmesh
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from struct import pack

class OverlayAutocomplete():
    def __init__(self, bm, layer):
        bgl.glEnable(bgl.GL_DEPTH_TEST)
        self.shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
        self.bm = bm
        self.layer = layer
        self.st = bpy.types.SpaceView3D
        self.handler = None

    def start(self):
        self.handler = self.st.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')

    def stop(self):
        self.st.draw_handler_remove(self.handler, 'WINDOW')

    def draw(self):
        # check for changes and apply them to mesh
        # TODO
        faces_to_draw = []

        batch = batch_for_shader(self.shader, 'TRIS', {"pos": faces_to_draw})
        self.shader.bind()
        color = self.shader.uniform_from_name("color")
        self.shader.uniform_vector_float(color, pack("4f", 0.6, 0.6, 0.1, 1.0), 4)
        batch.draw(self.shader)