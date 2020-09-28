import numpy, sys
from math import pi, sin, cos, asin, atan2, fabs
from numpy import sqrt, dot, cross
from numpy.linalg import norm

def LLH_to_PCPF(pRad,pLat,pLon,pAlt):
	pRad = float(pRad)
	pLat = float(pLat)
	pLon = float(pLon)
	pAlt = float(pAlt)
	dtr = float(pi / 180.0)
	csLat = cos(dtr * pLat)
	snLat = sin(dtr * pLat)
	csLon = cos(dtr * pLon)
	snLon = sin(dtr * pLon)
	pX = (pRad + pAlt) * csLat * csLon;
	pY = (pRad + pAlt) * csLat * snLon;
	pZ = (pRad + pAlt) * snLat;
	return pX,pY,pZ

def PCPF_to_LLH(pRad,pX,pY,pZ):
	pRad = float(pRad)
	pX = float(pX)
	pY = float(pY)
	pZ = float(pZ)
	dtr = float(pi / 180.0)
	rp = sqrt(pX*pX + pY*pY + pZ*pZ)
	pLat = asin(pZ / rp) / dtr
	csLat = cos(dtr * pLat)
	snLat = sin(dtr * pLat)
	pLon = atan2(pY, pX) / dtr
	p = sqrt(pX*pX + pY*pY)
	rnow = sqrt((pRad * csLat) * (pRad * csLat) + (pRad * snLat) * (pRad * snLat))
	pAlt = rp - rnow
	return pLat,pLon,pAlt

def trilateratePCPFs(pCoords1,pCoords2,pCoords3,pRange1,pRange2,pRange3):
    rCoords1 = pCoords2 - pCoords1
    rX = rCoords1 / norm(rCoords1)
    rCoords2 = pCoords3 - pCoords1
    rP = dot(rX, rCoords2)
    rCoords3 = rCoords2 - rP * rX
    rY = rCoords3 / norm(rCoords3)
    rZ = cross(rX,rY)
    rD = norm(pCoords2 - pCoords1)
    rJ = dot(rY,rCoords2)
    pX = (pRange1 * pRange1 - pRange2 * pRange2 + rD * rD) / (2 * rD)
    pY = (pRange1 * pRange1 - pRange3 * pRange3 - 2 * rP * pX + rP * rP + rJ * rJ) / (2 * rJ)
    rCoords4 = pRange1 * pRange1 - pX * pX - pY * pY
    if rCoords4 < 0:
        print("Warning! Intersection point is unstable!")
        print("Found coordinates maybe be incorrect!")
    pZ = sqrt(fabs(rCoords4))
    pCoordsLower = pCoords1 + pX * rX + pY * rY + pZ * rZ
    pCoordsUpper = pCoords1 + pX * rX + pY * rY - pZ * rZ
    return pCoordsLower,pCoordsUpper

if len(sys.argv) < 8 or sys.argv[1] == "help":
	print("Usage: du_trilateration_calc.py [psa] [pos#1] [rng#1] [pos#2] [rng#2] [pos#3] [rng#3] [div]")
	print("[psa] is Planet's Surface Area in km² (can be found via Map → Planet's Information)")
	print("[pos] is Position that uses '::pos{system,planet,latitude,longitude,altitude}' game format")
	print("[rng] is Range to the ore you see via scanner. Can be set in pixels if optional divisor parameter is added")
	print("[div] optional parameter that tells script how much pixels in 500 meters of range in scanner's calibration mode")
	print("Advice: if in scanner you see range and not sure if its 290 or 295 (for example), always use higher value!")
	print("Example: 88888 ::pos{0,5,-11.1111,-11.1111,-11.1111} 111 ::pos{0,5,-22.2222,-22.2222,-22.2222} 222 ::pos{0,5,-33.3333,-33.3333,-33.3333} 333")
	sys.exit()

pRadius = sqrt(((float(sys.argv[1])/4)/pi))

print("##################################################")
print("## Dual Universe Trilateration Calculator v1.20 ##")
print("##################################################")
print("Planet's radius is " + str("%.1f" % pRadius) + " km")

xPos1 = str(sys.argv[2]).replace("::pos{","").replace("}","")
xPos2 = str(sys.argv[4]).replace("::pos{","").replace("}","")
xPos3 = str(sys.argv[6]).replace("::pos{","").replace("}","")
xRange1 = float(sys.argv[3]) / 1000
xRange2 = float(sys.argv[5]) / 1000
xRange3 = float(sys.argv[7]) / 1000

if len(sys.argv) > 8:
	xDivisor = float(sys.argv[8])
	xRange1 = xRange1 * 500 / xDivisor
	xRange2 = xRange2 * 500 / xDivisor
	xRange3 = xRange3 * 500 / xDivisor

xSystem, xPlanet, xLat1, xLon1, xAlt1 = xPos1.split(',')
_, _, xLat2, xLon2, xAlt2 = xPos2.split(',')
_, _, xLat3, xLon3, xAlt3 = xPos3.split(',')

xData1 = LLH_to_PCPF(pRadius, xLat1, xLon1, float(xAlt1) / 1000)
xData2 = LLH_to_PCPF(pRadius, xLat2, xLon2, float(xAlt2) / 1000)
xData3 = LLH_to_PCPF(pRadius, xLat3, xLon3, float(xAlt3) / 1000)

xCoords1 = numpy.array([xData1[0], xData1[1], xData1[2]])
xCoords2 = numpy.array([xData2[0], xData2[1], xData2[2]])
xCoords3 = numpy.array([xData3[0], xData3[1], xData3[2]])

xTemp = trilateratePCPFs(xCoords1, xCoords2, xCoords3, xRange1, xRange2, xRange3)

xResultLower = PCPF_to_LLH(pRadius, xTemp[0][0], xTemp[0][1], xTemp[0][2])
xResultUpper = PCPF_to_LLH(pRadius, xTemp[1][0], xTemp[1][1], xTemp[1][2])

print("Choose coordinates that seem more viable:")
print("::pos{" + xSystem + "," + xPlanet + "," + str("%.4f" % xResultLower[0]) + "," + str("%.4f" % xResultLower[1]) + "," + str("%.4f" % (xResultLower[2] * 1000)) + "}")
print("::pos{" + xSystem + "," + xPlanet + "," + str("%.4f" % xResultUpper[0]) + "," + str("%.4f" % xResultUpper[1]) + "," + str("%.4f" % (xResultUpper[2] * 1000)) + "}")
print("##################################################")
