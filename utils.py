import numpy as np




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




