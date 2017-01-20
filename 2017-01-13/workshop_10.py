from pyplasm import*
import roof as r
import house as h
import csv,numpy
from src import workshop_07 as w7

"""
- scale interne/esterne
- struttura spaziale
- tetto
- porte/finestre
"""

scale = .05
hwall = 3.
hdoor = hwall-(hwall/4.)
hwindow = hwall-(hwall/4.)
dimborder = .2

alfa = PI/4.

#w9.create_roof(verts, cells, alfa, directions)



#------create house------

house = h.ggpl_create_house("lines/ext_walls.lines","lines/int_walls.lines")

#VIEW(house)


#start function ---------------------------------------------------------
def readFile(filename):
	"""
	Function that read a file between filename.
	@param filename: name of file
	"""

	file = open(filename, 'rb')
	reader = csv.reader(file, delimiter=",")
	return list(reader)
#end function -----------------------------------------------------------


#----windows/doors--------

def hpc_door(dx,dy,dz):

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([dx-(dx/4.),dy/4.,dz-(dz/4.)])
	c1 = STRUCT([T([1,3])([(dx/4.)/2.,(dz/4.)/2.]),c1])
	c2 = STRUCT([T([2])([dy-(dy/4.)]),c1])

	

	door = DIFFERENCE([c,STRUCT([c1,c2])])

	door = TEXTURE("images/parquet.jpg")(door)
	return door


def create_doors(filename):

	reader = readFile(filename)
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
	dimborder = .4

	c = CUBOID([dx,dy,dz])
	c1 = CUBOID([(dx-(3*dimborder))/2.,dy,(dz-(3*dimborder))/2.])
	c2 = STRUCT([T([1,3])([dimborder,dimborder]),c1,T([1])([((dx-(3*dimborder))/2.)+dimborder]),c1])
	c3 = STRUCT([c2, T(3)([((dz-(3*dimborder))/2.)+dimborder]),c2])


	borders = STRUCT([DIFFERENCE([c,c3])])
	glasses = STRUCT([T(2)(3*(dy/8.)),CUBOID([dx,dy/4.,dz])])

	borders = TEXTURE("images/parquet.jpg")(borders)
	glasses = TEXTURE("images/glass.jpg")(glasses)


	window = STRUCT([borders,glasses])
	return window




def create_windows(filename):

	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]

	windows = []


	for i in reader:
		print i
		if(i[1]==i[3]):
			if(i[2]>i[0]):
				window = hpc_window(i[2]-i[0],4,hwindow/scale)
				window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
			else:
				window = hpc_window(i[0]-i[2],4,hwindow/scale)
				window = STRUCT([T([1,2,3])([i[2],i[1],((hwall/8.)/scale)]),window]) 		
			
		else:
			window = hpc_door(4,i[3]-i[1],hwindow/scale)
			window = STRUCT([T([1,2,3])([i[0],i[1],((hwall/8.)/scale)]),window])	
		windows.append(window)

	windows = STRUCT(windows)
	windows = S([1,2,3])([scale,scale,scale])(windows)

	return windows


def create_ground_floor(path_ext_walls,path_int_walls):
	ext = h.create_external_enclosure(path_ext_walls)
	intP = h.create_internal_partitions(path_int_walls)
	parquet = h.create_floor(path_ext_walls)

	dimDoor = [2.,dimborder,(hwall)-(hwall/8.)]
	door = hpc_door(dimDoor[0],dimDoor[1],dimDoor[2])
	c = CUBOID([dimDoor[0],dimDoor[1],dimDoor[2]])

	reader = readFile(path_ext_walls)
	reader = [[float(float(j)) for j in i] for i in reader]


	print reader
	door = STRUCT([T([1,2])([reader[0][1]*scale,reader[0][1]*scale]),door])
	c = STRUCT([T([1,2])([reader[0][1]*scale,reader[0][1]*scale]),c])
	
	floor = DIFFERENCE([ext,c])
	floor = TEXTURE("images/interior.jpg")(floor)
	return STRUCT([floor,door,intP, parquet])




def create_roof(filename):
	reader = readFile(filename)
	reader = [[float(float(j)) for j in i] for i in reader]
	#print reader
	points = []
	for i in reader:
		points.append([i[0],i[1],0])
	points.append([reader[0][0],reader[0][1]])
	#print "----------------------------------",points
	
	directions = []
	directions.append([points[0],1])
	directions.append([points[1],2])
	directions.append([points[2],2])
	directions.append([points[3],2])
	directions.append([points[4],3])
	directions.append([points[5],3])
	directions.append([points[6],3])
	directions.append([points[7],4])
	directions.append([points[8],4])
	directions.append([points[9],4])
	directions.append([points[10],4])
	directions.append([points[11],4])

	print points
	cells = [[1,2,3],[3,4,5,6,3],[6,7,8,9,3],[9,10,11,3],[3,11,12,1]]
	#VIEW(r.create_roof(points,cells,alfa,directions))

	#VIEW(POLYLINE(points))
	#VIEW(r.create_roof(points, cells, alfa, directions))
	pol = MKPOL([points,cells,1])

	listapunti = UKPOL(pol)
	#cells = listapunti[1]
	#print cells
	roof = r.create_roof(points,cells,alfa,directions)
	roof = S([1,2,3])([scale+.001,scale+.001,scale+.001])(roof)
	return roof



windows = create_windows("lines/windows.lines")
doors = create_doors("lines/doors.lines")
floor = STRUCT([house, doors, windows])
gf = create_ground_floor("lines/ext_walls.lines","lines/int_walls.lines")
gf = STRUCT([gf,doors,windows])



roof = create_roof("lines/ext_walls.lines")
VIEW(STRUCT([gf, T(3)(hwall),floor,T(3)(hwall),roof]))



