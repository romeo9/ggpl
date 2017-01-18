from pyplasm import*
from src import workshop_07 as w7
from src import workshop_09 as w9
import house as h
import csv

"""
- scale interne/esterne
- struttura spaziale
- tetto
- porte/finestre
"""

scale = .05
hwall = 2.
hdoor = hwall-(hwall/4.)
hwindow = hwall-(hwall/4.)


verts = [[0,0,0],[6,0,0],[6,6,0],[3,6,0],[3,3,0],[0,3,0],[0,0,0]]
cells = [[1,2,5,6],[2,3,4,5]]

directions = [[[0,0,0],1],[[6,0,0],2],[[6,6,0],3],[[3,6,0],4],[[3,3,0],4],[[0,3,0],4]]

alfa = PI/4

#w9.create_roof(verts, cells, alfa, directions)



#------create house------

house = h.ggpl_create_house()

#VIEW(house)





#----windows/doors--------

def hpc_door(dx,dy,dz):



	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([dx-(dx/4.),dy/4.,dz-(dz/4.)])
	c1 = STRUCT([T([1,3])([(dx/4.)/2.,(dz/4.)/2.]),c1])
	c2 = STRUCT([T([2])([dy-(dy/4.)]),c1])
	door = DIFFERENCE([c,STRUCT([c1,c2])])
	return door


def create_doors(filename):

	reader = h.readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	doors = []

	for i in reader:
		if(i[1]==i[3]):
			door = hpc_door(i[2]-i[0],4,hdoor/scale)
			door = STRUCT([T([1,2])([i[0],i[1]]),door])	
			doors.append(door)
		else:
			door = hpc_door(4,i[3]-i[1],hdoor/scale)
			door = STRUCT([T([1,2])([i[0],i[1]]),door])	
			doors.append(door)

	doors = STRUCT(doors)
	doors = S([1,2,3])([scale,scale,scale])(doors)

	return doors


def hpc_window(dx,dy,dz):
	dimborder = .2

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([(dx-(3*dimborder))/2.,dy,(dz-(3*dimborder))/2.])
	c2 = STRUCT([T([1,3])([dimborder,dimborder]),c1,T([1])([((dx-(3*dimborder))/2.)+dimborder]),c1])
	c3 = STRUCT([c2, T(3)([((dz-(3*dimborder))/2.)+dimborder]),c2])


	borders = STRUCT([DIFFERENCE([c,c3])])
	glasses = STRUCT([T(2)(3*(dy/8.)),CUBOID([dx,dy/4.,dz])])

	borders = TEXTURE("images/parquet.jpg")(borders)


	window = STRUCT([borders,glasses])
	return window




def create_windows(filename):

	reader = h.readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	windows = []

	for i in reader:
		if(i[1]==i[3]):
			window = hpc_window(i[2]-i[0],4,hwindow/scale)
			window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
			windows.append(window)
		else:
			window = hpc_door(4,i[3]-i[1],hwindow/scale)
			window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
			windows.append(window)

	windows = STRUCT(windows)
	windows = S([1,2,3])([scale,scale,scale])(windows)

	return windows





windows = create_windows("lines/windows.lines")
#VIEW(STRUCT([house,windows]))
doors = create_doors("lines/doors.lines")

floor = STRUCT([house, doors, windows])

VIEW(STRUCT([floor, T(3)(hwall)]*3))




