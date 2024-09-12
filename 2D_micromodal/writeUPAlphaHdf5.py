import os
import h5py
import numpy as np
import argparse

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


parser = argparse.ArgumentParser()
parser.add_argument('--x_min', required=True, type=int, help='minimum crop x')
parser.add_argument('--x_max', required=True, type=int, help='maximum crop x')
parser.add_argument('--y_min', required=True, type=int, help='minimum crop y')
parser.add_argument('--y_max', required=True, type=int, help='maximum crop y')
#parser.add_argument('--z_min', required=True, type=int, help='minimum crop z')
#parser.add_argument('--z_max', required=True, type=int, help='maximum crop z')
parser.add_argument('--res', required=True, type=float, help='maximum resolution')
#parser.add_argument('--n_x', required=True, type=int, help='number of cells in x direction')
#parser.add_argument('--n_y', required=True, type=int, help='number of cells in y direction')
#parser.add_argument('--n_z', required=True, type=int, help='number of cells in z direciton')
#parser.add_argument('--n_level', required=True, type=int, help='level of refinement')
parser.add_argument('--output_filename', type=str, help='',default="voxelisedResults.hdf5")


opt = parser.parse_args()

x_min = opt.x_min
x_max = opt.x_max
y_min = opt.y_min
y_max = opt.y_max
#z_min = opt.z_min
#z_max = opt.z_max

dimX = x_max - x_min  
dimY = y_max - y_min
#dimZ = z_max - z_min

res=opt.res

#n_x = opt.n_x
#n_y = opt.n_y


#Ux = np.zeros((n_x, n_y))
#Uy = np.zeros((n_x, n_y))
#Uz = np.zeros((n_x, n_y, n_z))
img = np.zeros((dimX, dimY))


x = np.zeros(dimX*dimY)
y = np.zeros(dimX*dimY)
#z = np.zeros(dimX*dimY*dimZ)

all_files = os.listdir(os.getcwd())
all_files_numbers = [dir for dir in all_files if is_number(dir) ]
all_files_numbers.sort()

#file = open("constant/polyMesh/cellCenters","r")
#file = open("1/cellCenters","r")
file = open(all_files_numbers[0]+'/cellCenters',"r")

Lines = file.readlines()
count =0
wbool=0


for line in Lines:
    ls = line.strip()
    if (ls==")"):
        break
    if (wbool==1):
        x[count]=float(ls.split("(")[1].split(")")[0].split()[0])
        y[count]=float(ls.split("(")[1].split(")")[0].split()[1])
        #z[count]=float(ls.split("(")[1].split(")")[0].split()[2])
        count +=1
    if (ls=="("):
        wbool=1


resX = res
resY = res
#resZ = res*dimZ/n_z


print("count dir")
ndir = 0

for dir in os.listdir(os.getcwd()):
    if is_number(dir):
        ndir +=1

time = np.zeros(ndir)

eps = np.zeros((dimX,dimY, ndir))
Ux = np.zeros((dimX,dimY,ndir))
Uy = np.zeros((dimX,dimY,ndir))
pc = np.zeros((dimX, dimY, ndir))
p = np.zeros((dimX, dimY, ndir))
alpha_water = np.zeros((dimX,dimY,ndir))

tcount =0
#for dir in os.listdir(os.getcwd()):
for dir in all_files_numbers:
#  if is_number(dir):
    print(dir)
    time[tcount]=float(dir)

    file = open(dir+"/U","r")
    Lines = file.readlines()
    count = 0
    wbool = 0
    for line in Lines:
        ls = line.strip()
        if (ls == ")"):
            break
        if (wbool == 1):
            a = np.floor((x[count]) / resX)
            b = np.floor((y[count]) / resY)
            # c = np.floor((z[count])/resZ)
            img[a.astype(int), b.astype(int)] = 1.0
            Ux[a.astype(int), b.astype(int),tcount] = float(ls.split("(")[1].split(")")[0].split()[0])
            Uy[a.astype(int), b.astype(int),tcount] = float(ls.split("(")[1].split(")")[0].split()[1])
            # Uz[a.astype(int), b.astype(int),c.astype(int)] = float(ls.split("(")[1].split(")")[0].split()[2])
            count += 1
        if (ls == "("):
            wbool = 1

    file = open(dir + "/pc", "r")
    Lines = file.readlines()
    count = 0
    wbool = 0
    for line in Lines:
        ls = line.strip()
        if (ls == ")"):
            break
        if (wbool == 1):
            a = np.floor((x[count]) / resX)
            b = np.floor((y[count]) / resY)
            # c = np.floor((z[count])/resZ)
            pc[a.astype(int), b.astype(int), tcount] = float(ls)
            # Uz[a.astype(int), b.astype(int),c.astype(int)] = float(ls.split("(")[1].split(")")[0].split()[2])
            count += 1
        if (ls == "("):
            wbool = 1
    file = open(dir + "/alpha.water", "r")
    Lines = file.readlines()
    count = 0
    wbool = 0
    for line in Lines:
        ls = line.strip()
        if (ls == ")"):
            break
        if (wbool == 1):
            a = np.floor((x[count]) / resX)
            b = np.floor((y[count]) / resY)
            # c = np.floor((z[count])/resZ)
            alpha_water[a.astype(int), b.astype(int), tcount] = float(ls)
            # Uz[a.astype(int), b.astype(int),c.astype(int)] = float(ls.split("(")[1].split(")")[0].split()[2])
            count += 1
        if (ls == "("):
            wbool = 1
    file = open(dir + "/p", "r")
    Lines = file.readlines()
    count = 0
    wbool = 0
    for line in Lines:
        ls = line.strip()
        if (ls == ")"):
            break
        if (wbool == 1):
            a = np.floor((x[count]) / resX)
            b = np.floor((y[count]) / resY)
            # c = np.floor((z[count])/resZ)
            p[a.astype(int), b.astype(int), tcount] = float(ls)
            # Uz[a.astype(int), b.astype(int),c.astype(int)] = float(ls.split("(")[1].split(")")[0].split()[2])
            count += 1
        if (ls == "("):
            wbool = 1
    tcount += 1


f = h5py.File(opt.output_filename,"w")

img=np.swapaxes(img,0,1)
Ux=np.swapaxes(Ux,0,2)
Uy=np.swapaxes(Uy,0,2)
pc=np.swapaxes(pc,0,2)
p=np.swapaxes(p,0,2)
alpha_water=np.swapaxes(alpha_water,0,2)


f.create_dataset('img', data=img, dtype="float", compression="gzip")
f.create_dataset('Ux', data=Ux, dtype="float", compression="gzip")
f.create_dataset('Uy', data=Uy, dtype="float", compression="gzip")
f.create_dataset('pc', data=pc, dtype="float", compression="gzip")
f.create_dataset('alpha_water', data=alpha_water, dtype="float", compression="gzip")
f.create_dataset('p', data=p, dtype="float", compression="gzip")




f.close()
