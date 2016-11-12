from pyplasm import*
from larlib import*


def create_desk(dx,dy,dz):
	"""
	Function that create a desk for a classroom
	@param dx: dimension x of the desk
	@param dy: dimension y of the desk
	@param dz: dimension z of the desk

	"""
	r = dy/20. #cylinder radius

	desk = STRUCT([T(3)(dz),CUBOID([dx,dy,.1])])
	leg = STRUCT([T([1,2])([r*2,r*2]),CYLINDER([r,dz])(30)])
	xlegs = STRUCT([leg, T(1)(dx-(r*4)),leg])
	legs = STRUCT([xlegs, T(2)(dy-(r*4)), xlegs])

	supportDesk = STRUCT([T([1,2,3])([r*1.5,r*1.5,dz-(r*2)]),CUBOID([dx-(r*3),dy-(r*3),r*2])])
	diffSupport = STRUCT([T([1,2,3])([r*2.5,r*2.5,dz-(r*2)]),CUBOID([dx-(r*5),dy-(r*5),r*2])])
	supportDesk = DIFFERENCE([supportDesk,diffSupport])

	
	box = SKEL_1(BOX([1,2,3])(desk))

	desk = (COLOR(Color4f([220/255., 165/255., 116/255.,1])))(desk)
	legs = (COLOR(Color4f([0/255., 0/255., 0/255.,1])))(legs)
	supportDesk = (COLOR(Color4f([0/255., 0/255., 0/255.,1])))(supportDesk)
	desk = STRUCT([legs,desk,supportDesk])
	return desk



def create_chair(dx,dy,dz):
	"""
	Function that create a chair for a classroom
	@param dx: dimension x of the chair
	@param dy: dimension y of the chair
	@param dz: dimension z of the chair

	"""
	r = .05
	thickness = r/2.

	s = SPHERE(r)([30,30])
	s = JOIN(SKEL_1(s))

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
	


def create_closet(dx,dy,dz):
	"""
	Function that create a closet for a classroom
	@param dx: dimension x of the closet
	@param dy: dimension y of the closet
	@param dz: dimension z of the closet

	"""
	thickness = 0.05
	c = CUBOID([dx,dy,dz])
	door1 = STRUCT([T([1,2,3])([thickness,dy,thickness]),CUBOID([(dx/2.)-(thickness*2),thickness,dz-(thickness*2)])])
	door2 = STRUCT([T([1,2,3])([(dx/2.)+(thickness),dy,thickness]),CUBOID([(dx/2.)-(thickness*2),thickness,dz-(thickness*2)])])

	c = (COLOR(Color4f([153/255., 76/255., 0/255.,1])))(c)
	door1 = (COLOR(Color4f([80/255., 25/255., 0/255.,1])))(door1)
	door2 = (COLOR(Color4f([80/255., 25/255., 0/255.,1])))(door2)

	knob = SPHERE(thickness)([30,30])
	knob = JOIN(SKEL_1(knob))
	knobs = STRUCT([T([1,2,3])([(dx/2.)-(thickness*2),dy+thickness,dz/2.]),knob,T(1)(thickness*4),knob])

	knobs = (COLOR(Color4f([80/255., 25/255., 0/255.,1])))(knobs)

	closet = STRUCT([c, door1,door2,knobs])

	box = SKEL_1(BOX([1,2,3])(closet))

	return closet


def create_prof_desk(dx,dy,dz):
	"""
	Function that create a desk for the professor for a classroom
	@param dx: dimension x of the desk
	@param dy: dimension y of the desk
	@param dz: dimension z of the desk

	"""
	r = dy/25.
	desk = STRUCT([T(3)(dz),CUBOID([dx,dy,.1])])
	leg = STRUCT([T([1,2])([r*2,r*2]),CYLINDER([r,dz])(30)])
	xlegs = STRUCT([leg, T(1)(dx-(r*4)),leg])
	legs = STRUCT([xlegs, T(2)(dy-(r*4)), xlegs])

	supportDesk = STRUCT([T([1,2,3])([r*1.5,r*1.5,dz-(r*2)]),CUBOID([dx-(r*3),dy-(r*3),r*2])])
	diffSupport = STRUCT([T([1,2,3])([r*2.5,r*2.5,dz-(r*2)]),CUBOID([dx-(r*5),dy-(r*5),r*2])])
	supportDesk = DIFFERENCE([supportDesk,diffSupport])

	drawer = STRUCT([T([1,2,3])([r*4,r*2,dz-(dz/4.)]),CUBOID([dx/3.,dy/2.,dz/4.])])
	knob = STRUCT([T([1,2,3])([dx/4.,r,dz-(dz/6.)]),SPHERE(r)([30,30])])
	knob = JOIN(SKEL_1(knob))

	border1 = STRUCT([T([2,3])([dy-r,dz/3.]),CUBOID([dx,r,dz/2.])])
	border2 = STRUCT([T(3)(dz/3.),CUBOID([r,dy,dz/2.])])
	border3 = STRUCT([T([1,3])([dx-r,dz/3.]),CUBOID([r,dy,dz/2.])])

	border1 = (COLOR(Color4f([225/255., 161/255., 106/255.,1])))(border1)
	border2 = (COLOR(Color4f([225/255., 161/255., 106/255.,1])))(border2)
	border3 = (COLOR(Color4f([225/255., 161/255., 106/255.,1])))(border3)



	borders = STRUCT([border1,border2,border3])

	supportDesk = (COLOR(Color4f([0/255., 0/255., 0/255.,1])))(supportDesk)
	legs = (COLOR(Color4f([0/255., 0/255., 0/255.,1])))(legs)
	knob = (COLOR(Color4f([0/255., 0/255., 0/255.,1])))(knob)
	desk = (COLOR(Color4f([51/255., 255/255., 153/255.,1])))(desk)
	drawer = (COLOR(Color4f([225/255., 161/255., 106/255.,1])))(drawer)

	desk = STRUCT([legs,desk,supportDesk,drawer,knob,borders])

	return desk



def ggpl_main():
	"""
	Function that takes each forniture and create a classroom
	"""

	deskChair = STRUCT([T([2])([3]),create_desk(2,1,1),T([1,2])([1.3,1.4]),R([1,2])(PI)(create_chair(1,1,1.7))])

	desk = STRUCT([deskChair, T(1)(3), deskChair])
	desks = STRUCT([desk, T([2])([2]),desk, T([2])([2]),desk])
	profDesk = STRUCT([T([1,2])([1.1,0.9]),create_prof_desk(2,1,1.5)])
	chair1 = STRUCT([T(1)(2),create_chair(1,1,1.7)])
	closet = STRUCT([T([1,2])([7,4]),R([1,2])(PI/2)(create_closet(2,1,3))])

	room = SKEL_1(CUBOID([7,10,3]))

	classroom = STRUCT([profDesk,chair1,desks,closet,room])

	return classroom

VIEW(ggpl_main())

#VIEW(create_prof_desk(2,1,1.5)) #profdesk01
#VIEW(create_prof_desk(3,1,2)) #profdesk02

#VIEW(create_closet(2,1,3)) #closet01
#VIEW(create_closet(1,1,2)) #closet02

#VIEW(create_chair(1.2,1.2,2)) #chair01
#VIEW(create_chair(2,1,1)) #chair02

#VIEW(create_desk(2,1,1)) #desk01
#VIEW(create_desk(1,1,1)) #desk02

