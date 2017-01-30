from pyplasm import*
import csv
import os.path
import src.house as h
from src import workshop_10 as w10
"""
N.B. I file house.py, roof.py e stairs.py sono rispettivamente il workshop_08.py, 
il workshop_09.py, e il workshop_03.py che ho rinominato per comodita'
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


def create_fence(width,axis):
	pil1 = CUBOID([.5,.2,2])
	pillars = STRUCT([pil1, T(1)(1.5),pil1])
	
	horizontal_pil = R([1,3])(-PI/2.)(pil1)
	horizontal_pil = STRUCT([T(3)(1.5),horizontal_pil])

	base_fence = STRUCT([pillars, horizontal_pil])

	fence = []
	for i in range(0,width):
		fence.append(base_fence)
		fence.append(T(1)(1.5))

	if(axis=='x'):
		return STRUCT(fence)
	if(axis=='y'):
		return R([1,2])(PI/2.)(STRUCT(fence))




def main():
		
	#----house1---------------------
	house1 = w10.create_first_model()
	house1 = S([1,2,3])([7,7,7])(house1)
	house1 = STRUCT([T([1,2,3])([80,20,13]),house1])

	f1 = create_fence(12,'x')
	f1 = S([1,2,3])([7,7,7])(f1)
	f1 = STRUCT([T([1,2,3])([60,25,13]),f1])

	f2 = create_fence(10,'y')
	f2 = S([1,2,3])([7,7,7])(f2)
	f2 = STRUCT([T([1,2,3])([60,25,13]),f2])

	f3 = create_fence(10,'y')
	f3 = S([1,2,3])([7,7,7])(f3)
	f3 = STRUCT([T([1,2,3])([190,25,13]),f3])

	fence1 = STRUCT([f1,f2,f3])
	house1 = STRUCT([house1, fence1])


	#----house2---------------------
	house2 = w10.create_second_model()
	house2 = S([1,2,3])([2,2,2])(house2)
	house2 = STRUCT([T([1,2,3])([220,70,13]),house2])

	fence2 = fence1
	fence2 = STRUCT([T(1)(130),fence2])

	house2 = STRUCT([house2, fence2])

	#----house3---------------------
	house3 = w10.create_first_model()
	house3 = S([1,2,3])([7,7,7])(house3)
	house3 = STRUCT([T([1,2,3])([340,20,13]),house3])

	fence3 = fence2
	fence3 = STRUCT([T(1)(130),fence3])

	house3 = STRUCT([house3, fence3])

	#----house4---------------------
	house4 = w10.create_first_model()
	house4 = S([1,2,3])([7,7,7])(house4)
	house4 = STRUCT([R([1,2])(PI/2.),house4])
	house4 = STRUCT([T([1,2,3])([520,170,13]),house4])


	f4 = create_fence(8,'x')
	f4 = S([1,2,3])([7,7,7])(f4)
	f4 = STRUCT([T([1,2,3])([100,135,13]),f4])

	f5 = create_fence(8,'x')
	f5 = S([1,2,3])([7,7,7])(f5)
	f5 = STRUCT([T([1,2,3])([100,25,13]),f5])

	fence4 = STRUCT([f5,f3, f4])
	fence4 = STRUCT([T([1,2])([340,130]),fence4])

	house4 = STRUCT([house4, fence4])


	#----house5---------------------
	house5 = w10.create_second_model()
	house5 = S([1,2,3])([2,2,2])(house5)
	house5 = STRUCT([R([1,2])(PI),house5])
	house5 = STRUCT([T([1,2,3])([210,230,13]),house5])

	fence5 = STRUCT([f5,f3, f4])
	fence5 = R([1,2])(PI/2.)(fence5)
	fence5 = STRUCT([T([1,2])([260,60]),fence5])

	house5 = STRUCT([house5, fence5])


	#----house6---------------------
	house6 = w10.create_first_model()
	house6 = S([1,2,3])([7,7,7])(house6)
	house6 = STRUCT([R([1,2])(PI),house6])
	house6 = STRUCT([T([1,2,3])([330,280,13]),house6])

	fence6 = fence5
	fence6 = STRUCT([T(1)(110),fence6])
	house6 = STRUCT([house6, fence6])


	#----house7---------------------
	house7 = w10.create_first_model()
	house7 = S([1,2,3])([7,7,7])(house7)
	house7 = STRUCT([T([1,2,3])([120,250,13]),house7])

	fence7 = fence1
	fence7 = STRUCT([T([1,2])([40,230]),fence7])

	house7 = STRUCT([house7, fence7])


	#----house8---------------------
	house8 = w10.create_second_model()
	house8 = S([1,2,3])([2,2,2])(house8)
	house8 = STRUCT([T([1,2,3])([250,320,13]),house8])

	fence8 = fence7
	fence8 = STRUCT([T(1)(130),fence8])

	house8 = STRUCT([house8, fence8])


	#----house9---------------------
	house9 = w10.create_second_model()
	house9 = S([1,2,3])([2,2,2])(house9)
	house9 = STRUCT([R([1,2])(PI/4.),house9])
	house9 = STRUCT([T([1,2,3])([480,270,13]),house9])

	fence9 = f2
	fence9 = STRUCT([T([1,2])([470,250]),fence9])

	house9 = STRUCT([house9, fence9])


	#----ground---------------------
	ground = create_ground("lines/street.lines","lines/straight_street.lines","lines/box.lines","images/grass.jpg")



	VIEW(STRUCT([ground, house1, house2, house3, house4, house5, house6, house7, house8, house9]))




if __name__ == '__main__':
	main()



