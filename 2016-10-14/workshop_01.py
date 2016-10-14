from pyplasm import*
	
def plane_frame(distanceList, interstoryHeight, widthPill, widthBeam):
	"""
	@param distanceList: list of distance between the pillars. 
	@param interstoryHeight: list of distance between the floor.
	@param widthPill: is the width of a pillar. All pillars have same width.
	@param widthBeam: width of the beam.
	In this function we consider that widthPill = widthBeam, because of the stability of the frame.
	
	"""
	
	numBeam = len(interstoryHeight)
	pillarsList = [widthPill]

	for item in distanceList:
		pillarsList.append(item)
		pillarsList.append(widthPill)

	beamList = []

	for item in interstoryHeight:
		beamList.append(item)
		beamList.append(widthBeam)

	numPill = len(distanceList)+1

	print(beamList)
	

	hPillList = [(-i) for i in beamList]
	print(hPillList)

	xPillar = QUOTE(pillarsList)
	yPillar = QUOTE([widthPill, -4])
	xyPillar = PROD([yPillar, xPillar])
	pillar = PROD([xyPillar, QUOTE(hPillList)])

	
	sumdistancepill = sum([abs(i) for i in distanceList])

	
	xBeam = QUOTE([(widthPill*numPill)+sumdistancepill]) #lunghezza della trave
	yBeam = QUOTE([widthBeam]) #spessore della trave
	xyBeam = PROD([yBeam, xBeam])
	beam = PROD([xyBeam, QUOTE(beamList)]) #altezza della trave

	VIEW(STRUCT([pillar, beam]))


distanceList=[-2,-1]
interstoryHeight = [-2, -5,-1]
widthPill = 0.5
widthBeam = widthPill

plane_frame(distanceList, interstoryHeight, widthPill, widthBeam)


