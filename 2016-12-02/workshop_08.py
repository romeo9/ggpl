from pyplasm import*
import csv

def readFile(filename):

	file = open(filename, 'rb')
	reader = csv.reader(file, delimiter=",")
	return list(reader)


def create_external_enclosure(filename):
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	extWall = STRUCT(points)	
	extWall = S([1,2,3])([.02,.02,.02])(extWall)
	extWall = OFFSET([.2,.2,3])(extWall)
	extWall = TEXTURE("images/exterior.jpg")(extWall)

	return extWall
	

def create_internal_partitions(filename):
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))

	intWall = STRUCT(points)
	intWall = S([1,2,3])([.02,.02,.02])(intWall)
	intWall = OFFSET([.2,.2,3])(intWall)
	intWall = TEXTURE("images/interior.jpg")(intWall)

	return intWall

def create_floor(filename):
	pointsRead = readFile(filename)
	points = []
	indexs = []
	temp = 0

	for i in pointsRead:
		points.append(POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))
	

	floor = SOLIDIFY(STRUCT(points))	
	floor = S([1,2,3])([.02,.02,.02])(floor)
	floor = TEXTURE("images/parquet.jpg")(floor)
	

	return floor

def ggpl_create_house():

	ext = create_external_enclosure("lines/external_enclosure.lines")
	intP = create_internal_partitions("lines/internal_partitions.lines")

	floor = create_floor("lines/external_enclosure.lines")
	
	VIEW(STRUCT([floor, ext, T([1,2])([.42,1.85]),intP]))


ggpl_create_house()
