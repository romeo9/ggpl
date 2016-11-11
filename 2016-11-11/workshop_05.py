from pyplasm import*
from larlib import*


def create_desk(dx,dy,dz):

	r = dy/20. #cylinder radius

	desk = STRUCT([T(3)(dz),CUBOID([dx,dy,.1])])
	leg = STRUCT([T([1,2])([r*2,r*2]),CYLINDER([r,dz])(30)])
	xlegs = STRUCT([leg, T(1)(dx-(r*4)),leg])
	ylegs = STRUCT([xlegs, T(2)(dy-(r*4)), xlegs])

	desk = STRUCT([ylegs,desk])
	box = SKEL_1(BOX([1,2,3])(desk))

	return desk


def create_chair(dx,dy,dz):
	r = .05
	thickness = r/2.

	s = SPHERE(r)([100,100])

	seat = STRUCT([T([1,2,3])([r,r,(dz/2.)-r]),CUBOID([dx-(r*2),dy-(r*2),thickness])])
	back = STRUCT([T([1,2,3])([r,r*3,((dz/2.)+(dz/4.))]), CUBOID([dx-(r*2),thickness,(dz/4.)]) ])

	seat = (COLOR(Color4f([220/255., 165/255., 116/255.,1])))(seat)
	back = (COLOR(Color4f([220/255., 165/255., 116/255.,1])))(back)

	leg1 = STRUCT([CYLINDER([r,dz/2.])(30),T(3)(dz/2.),s])
	leg2 = CYLINDER([r,(dz/2.)-r])(30)

	legBack = STRUCT([T([1,2])([r*2,r*2]),leg2, T(3)((dz/2.)-thickness),leg1])
	legFront = STRUCT([T([1,2])([r*2,r*2]),leg2])
	
	legBack = (COLOR(Color4f([96/255., 96/255., 96/255.,1])))(legBack)
	legFront = (COLOR(Color4f([96/255., 96/255., 96/255.,1])))(legFront)
	
	xlegs = STRUCT([legBack, T(1)(dx-(r*4)),legBack])	
	ylegs = STRUCT([T(2)(dy-(r*4)),legFront, T(1)(dx-(r*4)), legFront])

	chair = STRUCT([xlegs,ylegs,seat, back])
	box = SKEL_1(BOX([1,2,3])(chair))

	return chair
	



def create_blackboard(dx,dy,dz):
	thickness = 0.1

	c = CUBOID([dx,dy,dz])
	board = STRUCT([T([1,2])([thickness/2.,thickness/2.]),CUBOID([dx-thickness,dy-thickness,dz])])
	board = (COLOR(Color4f([0/255., 0/255., 0/255.,1])))(board)
	frame = DIFFERENCE([c,board])

	
	text = PROD([S([1,2])([thickness,thickness])(OFFSET([thickness,thickness])(TEXT("pyplasm"))), Q(thickness/2.)])
	text = STRUCT([T([1,2])([0.2,1]),text])
	blackboard = STRUCT([board,frame,text])
	
	return blackboard


def create_closet(dx,dy,dz):
	thickness = 0.05
	c = CUBOID([dx,dy,dz])
	door1 = STRUCT([T([1,2,3])([thickness,dy,thickness]),CUBOID([(dx/2.)-(thickness*2),thickness,dz-(thickness*2)])])
	door2 = STRUCT([T([1,2,3])([(dx/2.)+(thickness),dy,thickness]),CUBOID([(dx/2.)-(thickness*2),thickness,dz-(thickness*2)])])

	c = (COLOR(Color4f([153/255., 76/255., 0/255.,1])))(c)
	door1 = (COLOR(Color4f([80/255., 25/255., 0/255.,1])))(door1)
	door2 = (COLOR(Color4f([80/255., 25/255., 0/255.,1])))(door2)

	knob = SPHERE(thickness)([50,50])
	knobs = STRUCT([T([1,2,3])([(dx/2.)-(thickness*2),dy+thickness,dz/2.]),knob,T(1)(thickness*4),knob])

	knobs = (COLOR(Color4f([80/255., 25/255., 0/255.,1])))(knobs)

	closet = STRUCT([c, door1,door2,knobs])

	VIEW(closet)

create_closet(1,1,3.5)







