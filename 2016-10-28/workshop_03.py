from pyplasm import*
import math


#---------start function--------------------------------------------------
def create_straight_stairs(width, tread, riser, nStep):
	"""
	function that creates a stairs according to given parameters.
	@param width: horizontal length of single step
	@param tread: distance between single step
	@param riser: distance of height of single step
	"""
	
	xStep = MKPOL([[[tread, 0],[tread, riser*2], [tread*2, riser*2], [tread*2, riser]], [[1,2,3,4]], None])

	step = PROD([QUOTE([width]), xStep])

	firstStep = CUBOID([width,tread,riser])

	stairsList=[]
	stairsList.append(firstStep)

	tempy = 0
	tempz = 0
	for i in range(nStep-1):
		trasl = STRUCT([T(2)(tempy),T(3)(tempz), step]) #every step there is a traslation
		stairsList.append(trasl)
		tempy = tread+tempy
		tempz = riser+tempz

	return STRUCT(stairsList)
#---------end function--------------------------------------------------


#---------start function--------------------------------------------------
def ggpl_straight_stairs(dx, dy, dz):
	"""
	function that take in input three dimensions of an example box. According to these params
	this function build a structure with a skeleton of the box and inside
	"""
	dy=dy*2
	dz=dz/2

	yStep = 1	#dimension of single step
	xStep = dx 	#dimension of single step, if you want to make this param editable, you can make xStep=dx
	
	box = SKEL_1(CUBOID([dx,dy,dz]))

	nStep = int(dy/yStep)
	zStep = (float(dz)/float(nStep))


	stairs = create_straight_stairs(xStep, yStep, zStep, nStep)
	

	VIEW(STRUCT([stairs, box]))

#---------end function--------------------------------------------------


ggpl_straight_stairs(2,3,5)

