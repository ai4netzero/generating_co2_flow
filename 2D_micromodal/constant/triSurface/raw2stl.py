#script to raw image and create an stl mesh for DNS
import matplotlib.pyplot as plt
import numpy as np
import skimage
from skimage import data
from skimage.measure import marching_cubes
from stl import mesh
import argparse
from scipy import ndimage
import os

parser = argparse.ArgumentParser()
parser.add_argument('--x_min', required=True, type=int, help='minimum crop x')
parser.add_argument('--x_max', required=True, type=int, help='maximum crop x')
parser.add_argument('--y_min', required=True, type=int, help='minimum crop y')
parser.add_argument('--y_max', required=True, type=int, help='maximum crop y')
parser.add_argument('--z_min', required=True, type=int, help='minimum crop z')
parser.add_argument('--z_max', required=True, type=int, help='maximum crop z')
parser.add_argument('--pores_value', required=True, type=int, help='value of porespace in image')
parser.add_argument('--solid_value', required=True, type=int, help='value of solid in image')
parser.add_argument('--image_name', required=True, type=str, help='file name of your image')
parser.add_argument('--x_dim', required=True, type=int, help='size of image in x dir')
parser.add_argument('--y_dim', required=True, type=int, help='size of image in y dir')
parser.add_argument('--z_dim', required=True, type=int, help='size of image in z dir')


opt = parser.parse_args()

# User Input

target_direc = ""
image_name = opt.image_name
output_direc = ""

x_dim=opt.x_dim
y_dim=opt.y_dim
z_dim=opt.z_dim


x_min = opt.x_min
x_max = opt.x_max
y_min = opt.y_min
y_max = opt.y_max
z_min = opt.z_min
z_max = opt.z_max
pores_value = opt.pores_value
solid_value = opt.solid_value

print('stl: ',image_name)


# make sure that image name contains only the name without the path or extensions
image_name = os.path.splitext(os.path.basename(image_name))[0]

# END User Input

print('Value of the pores is:'+str(pores_value))

img = np.fromfile(target_direc+image_name+'.raw', dtype='uint8', sep="")
img = np.reshape(img, (z_dim, y_dim, x_dim))
print('shape of image: ', img.shape)

img_crop = img[z_min:z_max,y_min:y_max,x_min:x_max]
img_padded = np.pad(img_crop, pad_width=1,mode='constant', constant_values=pores_value)

print('Unique values in the padded image are:'+str(np.unique(img_padded)))


img_padded=np.swapaxes(img_padded,0,2)

pores = (img_padded==pores_value)*1
distance_map = ndimage.distance_transform_edt(pores)
search_size=int(min((x_max-x_min)/4,(y_max-y_min)/4,(z_max-z_min)/4))
search_window = distance_map[search_size:(x_max-x_min-search_size),(search_size):(y_max-y_min-search_size),(search_size):(z_max-z_min-search_size)]
ind = np.unravel_index(np.argmax(search_window, axis=None), search_window.shape)

ind_x = ind[0]+search_size
ind_y = ind[1]+search_size
ind_z = ind[2]+search_size

with open("./pore_indx", "w") as f:
	f.write(str(ind_x+1))

with open("./pore_indy", "w") as f:
	f.write(str(ind_y+1))

with open("./pore_indz", "w") as f:
	f.write(str(ind_z+1))

verts, faces, normals, values = skimage.measure.marching_cubes(img_padded, (pores_value+solid_value)/2, step_size=1, allow_degenerate=1)

# Create the mesh
imagemesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        imagemesh.vectors[i][j] = verts[f[j],:]

# Write the mesh to file "cube.stl"
imagemesh.save(output_direc+'Image_meshed.stl')
imagemesh.save(output_direc+'Image_meshed_python.stl')

