import numpy as np

def check_for_changes(bm, last_selection):
    # checks if bmesh has changed
    # comparing vertex coordiantes and selection to last_selection
    new = str([(v.co, v.select) for v in bm.verts])
    if new != last_selection:
        last_selection = new
        return True
    return False


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
    
    differences[0] = vectorLength(face.normal - avg_parameters[0])
    differences[1] = abs(face.calc_area() - avg_parameters[1])

    differences -= diff_parameters

    if differences.size == (differences >= 0).sum():
        return True
    else:
        return False


def avg_parameters(parameters_faces, factor, delta):
    # calculates average and highest difference of given parameters
    # parameters_faces: dict of np.arrays
    # factor: np array
    # delta: np array

    avg = np.zeros(2)
    diff = np.zeros(2)

    # average all parameters
    avg[0] = np.average(parameters_faces["normal"])
    avg[1] = np.average(parameters_faces["area"])

    # converting normal to length for easier comparison
    vecLenVectorized = np.vectorize(vectorLength)
    np.subtract(parameters_faces["normal"], avg[0])
    vecLenVectorized(parameters_faces["normal"])

    # highest difference between average and parameter
    max1 = vectorLength(avg[0] - np.amax(parameters_faces["normal"]))
    max2 = vectorLength(avg[0] - np.amin(parameters_faces["normal"]))
    diff[0] = max(max1, max2)*factor[0] + delta[0]
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




