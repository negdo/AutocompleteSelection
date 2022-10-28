'''
Copyright (C) 2022 Miha Marinko
miha.marinko20@gmail.com

Created by Miha Marinko

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Autocomplete Selection",
    "description": "Autocomplete selection of faces, edges and vertices",
    "author": "Miha Marinko",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    "bl_options": {"REGISTER", "UNDO"} }

import bpy
from .autocomplete import Autocomplete





addon_keymaps = []
def register():
    bpy.utils.register_class(Autocomplete)

    # Add the hotkey
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(Autocomplete.bl_idname, type='SPACE', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(Autocomplete)