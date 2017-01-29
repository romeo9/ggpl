from pyplasm import*
import csv
import os.path
import src.house as h
from src import workshop_10 as w10
"""
N.B. I file house.py, roof.py e stairs.py sono rispettivamente il workshop_08.py, 
il workshop_09.py, e il workshop_03.py che ho rinominato per comodità 
"""

def readFile(filename):
	"""
	Function that read a file between filename.
	@param filename: name of file
	"""

	file = open(filename, 'rb')
	reader = csv.reader(file, delimiter=",")
	return list(reader)

def create_box(filename):
	reader = readFile(filename)
	lines = []
	for i in reader:
		s = POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]])
		lines.append(s)

	box = STRUCT(lines)
	
	return box


def create_ground(filename_curvestreet, filename_straightstreet, filename_box, texture_grass):
	"""
	function that create the basement for the model
	@param filename_curvestreet: link of the file .lines where there are the curve streets
	@param filename_straightstreet: file .lines with the straight street
	@param filename_box: file .lines with the shape of the basement
	@param texture_grass: file .jpg of the grass texture
	"""

	readCurve = readFile(filename_curvestreet)
	readStraight = readFile(filename_straightstreet)

	curve = []
	lines = []


	for i in readCurve:
		c = MAP(BEZIER(S1)([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]]))(INTERVALS(1)(5))	
		curve.append(c)

	for i in readStraight:
		s = POLYLINE([[float(i[0]),float(i[1])],[float(i[2]),float(i[3])]])
		lines.append(s)

	curve_street = STRUCT(curve)
	straight_street = STRUCT(lines)
	streets = STRUCT([curve_street, straight_street])

	marciapiede = streets
	marciapiede = OFFSET([30,30])(marciapiede)
	
	streets = OFFSET([20,20])(streets)
	streets = PROD([streets, Q(5)])
	streets = COLOR(Color4f([40/255., 40/255., 40/255.,1]))(streets)
	
	marciapiede = PROD([marciapiede, Q(3)])
	marciapiede = STRUCT([T([1,2])([-3,-3]),marciapiede])

	box = create_box(filename_box)
	box = SOLIDIFY(box)
	
	box = PROD([box, Q(3)])
	box = TEXTURE(texture_grass)(box)
	box = MATERIAL([0,.44,.031,.2,  0,0,0,1,  0,0,0,1, 0,0,0,1, 1])(box)

	allS = STRUCT([streets,box,marciapiede])

	case = SOLIDIFY(create_box(filename_box))
	case = PROD([case, Q(10)])
	case = COLOR(Color4f([51/255., 25/255., 0/255.,1]))(case)

	return STRUCT([case, T(3)(10),allS])




house1 = w10.create_first_model()
house1 = S([1,2,3])([7,7,7])(house1)
house1 = STRUCT([T([1,2,3])([80,20,13]),house1])

house2 = w10.create_second_model()
house2 = S([1,2,3])([2,2,2])(house2)
house2 = STRUCT([T([1,2,3])([180,70,13]),house2])

house3 = w10.create_first_model()
house3 = S([1,2,3])([7,7,7])(house3)
house3 = STRUCT([T([1,2,3])([280,20,13]),house3])

house4 = w10.create_second_model()
house4 = S([1,2,3])([2,2,2])(house4)
house4 = STRUCT([R([1,2])(PI/4.),house4])
house4 = STRUCT([T([1,2,3])([430,70,13]),house4])

house5 = w10.create_first_model()
house5 = S([1,2,3])([7,7,7])(house5)
house5 = STRUCT([R([1,2])(PI/2.),house5])
house5 = STRUCT([T([1,2,3])([520,170,13]),house5])

house6 = w10.create_second_model()
house6 = S([1,2,3])([2,2,2])(house6)
house6 = STRUCT([R([1,2])(PI),house6])
house6 = STRUCT([T([1,2,3])([200,230,13]),house6])

house7 = w10.create_first_model()
house7 = S([1,2,3])([7,7,7])(house7)
house7 = STRUCT([R([1,2])(PI),house7])
house7 = STRUCT([T([1,2,3])([330,280,13]),house7])

house8 = w10.create_first_model()
house8 = S([1,2,3])([7,7,7])(house8)
house8 = STRUCT([T([1,2,3])([120,250,13]),house8])

house9 = w10.create_second_model()
house9 = S([1,2,3])([2,2,2])(house9)
house9 = STRUCT([T([1,2,3])([250,320,13]),house9])

house10 = w10.create_second_model()
house10 = S([1,2,3])([2,2,2])(house10)
house10 = STRUCT([R([1,2])(PI/4.),house10])
house10 = STRUCT([T([1,2,3])([480,270,13]),house10])


ground = create_ground("lines/street.lines","lines/straight_street.lines","lines/box.lines","images/grass.jpg")

VIEW(STRUCT([ground, house1,house2,house3,house4, house5, house6, house7,house8, house9,house10]))
