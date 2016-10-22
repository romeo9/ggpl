from pyplasm import*
	

#start function ------------------------------------------------------------
def plane_frame(distanceList, interstoryHeight, widthPill, widthBeam):
	"""
	@param distanceList: list of distance between the pillars. 
	@param interstoryHeight: list of distance between the floor.
	@param widthPill: is the width of a pillar. All pillars have same width.
	@param widthBeam: width of the beam.
	In this function we consider that widthPill = widthBeam, because of the stability of the frame.
	
	"""
	
	numBeam = len(interstoryHeight) #number of beam
	pillarsList = [widthPill] #create a new list of pillars and distance between them. First element is the first pillar.

	#creation of pillars' list
	for item in distanceList:
		pillarsList.append(item)
		pillarsList.append(widthPill)


	beamList = [] #create an empty beams' list

	#inserting element inside beams' list
	for item in interstoryHeight:
		beamList.append(item)
		beamList.append(widthBeam)

	#number of pillars it's like number of distance - 1
	numPill = len(distanceList)+1
	
	#create a list with the pillars' heights that are negative instead of interstory height
	hPillList = [(-i) for i in beamList]

	#x axis of pillars
	xPillar = QUOTE(pillarsList)
	#y axis of pillars
	yPillar = QUOTE([widthPill, -4])
	#2D pillars
	xyPillar = PROD([yPillar, xPillar])
	#3D pillars
	pillar = PROD([xyPillar, QUOTE(hPillList)])

	#need sum of distance between pillars to calculate lenght of beam
	sumdistancepill = sum([abs(i) for i in distanceList])

	#x axis of beam
	xBeam = QUOTE([(widthPill*numPill)+sumdistancepill])
	#y axis of beam
	yBeam = QUOTE([widthBeam])
	#2D beam
	xyBeam = PROD([yBeam, xBeam])
	#3D beam
	beam = PROD([xyBeam, QUOTE(beamList)]) 

	#view method
	VIEW(STRUCT([pillar, beam]))


#end function---------------------------------------------------------------------


#TEST
distanceList=[-1,-1,-1, -7]
interstoryHeight = [-2,-2,-2]

#here, pillar's width has to be the same of bean's, but this can be changed
widthPill = .1
widthBeam = .1

#call function
plane_frame(distanceList, interstoryHeight, widthPill, widthBeam)


