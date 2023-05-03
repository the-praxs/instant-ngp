import sys
import tinyobjloader

filename = "../models/cornell_box.obj"


reader = tinyobjloader.ObjReader()

# Load .obj(and .mtl) using default configuration
ret = reader.ParseFromFile(filename)

# Optionally you can set custom `config`
# config = tinyobj.ObjReaderConfig()
# config.triangulate = False
# ret = reader.ParseFromFile(filename, config)

if ret == False:
    print("Failed to load : ", filename)
    print("Warn:", reader.Warning())
    print("Err:", reader.Error())
    sys.exit(-1)

if reader.Warning():
    print("Warn:", reader.Warning())

attrib = reader.GetAttrib()
print("attrib.vertices = ", len(attrib.vertices))
print("attrib.normals = ", len(attrib.normals))
print("attrib.texcoords = ", len(attrib.texcoords))

# vertex data must be `xyzxyzxyz...`
assert len(attrib.vertices) % 3 == 0

# normal data must be `xyzxyzxyz...`
assert len(attrib.normals) % 3 == 0

# texcoords data must be `uvuvuv...`
assert len(attrib.texcoords) % 2 == 0

for (i, v) in enumerate(attrib.vertices):
    print(f"v[{i}] = {v}")

for (i, v) in enumerate(attrib.normals):
    print(f"vn[{i}] = {v}")

for (i, v) in enumerate(attrib.texcoords):
    print(f"vt[{i}] = {t}")

print(f"numpy_vertices = {attrib.numpy_vertices()}")

materials = reader.GetMaterials()
print("Num materials: ", len(materials))
for m in materials:
    print(m.name)
    print(m.diffuse)
    print(m.diffuse_texname)
    # Partial update(array indexing) does not work
    # m.diffuse[1] = 1.0

    # Update with full object assignment works
    m.diffuse = [1, 2, 3]
    print(m.diffuse)

    # print(m.shininess)
    # print(m.illum)

shapes = reader.GetShapes()
print("Num shapes: ", len(shapes))
for shape in shapes:
    print(shape.name)
    print(f"len(num_indices) = {len(shape.mesh.indices)}")
    for (i, idx) in enumerate(shape.mesh.indices):
        print(f"[{i}] v_idx {idx.vertex_index}")
        print(f"[{i}] vn_idx {idx.normal_index}")
        print(f"[{i}] vt_idx {idx.texcoord_index}")
    print(f"numpy_indices = {shape.mesh.numpy_indices()}")
    print(f"numpy_num_face_vertices = {shape.mesh.numpy_num_face_vertices()}")
    print(f"numpy_material_ids = {shape.mesh.numpy_material_ids()}")
