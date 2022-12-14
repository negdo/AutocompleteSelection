import numpy as np
from pathlib import Path
from bpy.utils import resource_path
import bpy



def get_autocomplete_face_coords(bm):
    # returns coords of faces that should be autocompleted
    # if layer is 1, vertices of the face get into coords
    bm.faces.ensure_lookup_table()
    coords = []
    try: 
        layer = bm.faces.layers.int.get("AutocompleteSelect")
        tris = bm.calc_loop_triangles()
        coords = np.zeros((len(tris)*3, 3))
        c = 0
        for i in range(len(tris)):
            if tris[i][0].face[layer] == 1:
                for v in tris[i]:
                    coords[c] = v.vert.co
                    c += 1
        coords = coords[:c]

    except: pass
    return coords


def compare_parameters(face, avg_parameters, diff_parameters):
    # compares parameters of face to average of selected faces
    # returns True if face is within range of diff_parameters
    # face: bmesh face
    # avg_parameters: np.array([normal, area])
    # diff_parameters: np.array([normal, area])
    # 0 - normal
    # 1 - area

    differences = np.zeros(2)
    
    differences[0] = vectorLength(np.array(face.normal) - avg_parameters[0])
    differences[1] = abs(face.calc_area() - avg_parameters[1])

    differences -= diff_parameters

    if differences.size == (differences <= 0.001).sum():
        return True
    else:
        return False


def avg_parameters(parameters_faces, factor, delta):
    # calculates average and highest difference of given parameters
    # parameters_faces: dict of np.arrays
    # factor: np array
    # delta: np array

    avg = [0, 0]
    diff = np.zeros(2)

    # average all parameters
    avg[0] = np.average(parameters_faces["normal"], axis=0)
    avg[1] = np.average(parameters_faces["area"])

    # converting normal to length for easier comparison
    parameters_faces["normal"] = np.subtract(parameters_faces["normal"], avg[0])

    normals = np.zeros(len(parameters_faces["normal"]))
    for i in range(len(parameters_faces["normal"])):
        normals[i] = vectorLength(parameters_faces["normal"][i])


    # highest difference between average and parameter

    diff[0] = np.amax(normals)*factor[0] + delta[0]
    max1 = abs(avg[1] - np.amax(parameters_faces["area"]))
    max2 = abs(avg[1] - np.amin(parameters_faces["area"]))
    diff[1] = max(max1, max2)*factor[1] + delta[0]

    return avg, diff


def get_face_parameters(face, parameters):
    # appends parameters of face to parameters dict
    parameters["normal"].append(face.normal)
    parameters["area"].append(face.calc_area())


def vectorLength(vector):
    # returns length of vector
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5


def get_bounding_box(bm):
    # returns rotated bounding box of selected faces


    # get selected faces
    bm.faces.ensure_lookup_table()
    faces = []
    for face in bm.faces:
        if face.select:
            faces.append(face.verts[0].co)

    faces = np.array(faces)

    
    # get average coordinates of selected faces
    avg = np.average(faces, axis=0)

    # find a point that is furthest away from average
    # this point will be the center of the bounding box

    from_center = np.subtract(faces, avg)

    distances = np.zeros(len(from_center))
    for i in range(len(from_center)):
        distances[i] = vectorLength(from_center[i])
    
    # get index of point that is furthest away from average

    vector1 = from_center[np.argmax(distances)]

    # get a point that is furthest away from vector1

    distances = np.zeros(len(from_center))


def append_geo_nodes():
    # append geometry nodes group AutocompleteUtils
    print("Appending Autocomplete Utils")
    USER = Path(resource_path('USER'))
    src = USER / "scripts/addons/AutocompleteSelection"

    file_path = src / "AutocompleteUtils.blend"
    inner_path = "NodeTree"
    object_name = "Autocomplete Utils"

    bpy.ops.wm.append(
        filepath=str(file_path / inner_path / object_name),
        directory=str(file_path / inner_path),
        filename=object_name
    )


