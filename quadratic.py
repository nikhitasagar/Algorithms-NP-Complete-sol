import math
import string

def QuadS (a,b,c):
	d = b**2 - 4*a*c
	if a==0:
		return None
	if d >= 0:
		x1 = (-b + math.sqrt(d)) / (2 * a)
		x2 = (-b - math.sqrt(d)) / (2 * a)
		return(x1, x2)
	x1 = complex((-b + math.sqrt(d)) / (2 * a))
	x2 = complex((-b + math.sqrt(d)) / (2 * a))
	return(x1,x2)

def QuadA (a,b,c):
	d = b**2 - 4*a*c
	if a==0:
		return None
	if b >=0:
		x1 = (2*c) / (-b - math.sqrt(d))
		x2 = (-b - math.sqrt(d)) / (2 * a)
		return(x1,x2)
	x2 = (2*c) / (-b + math.sqrt(d))
	x1 = (-b + math.sqrt(d)) / (2 * a)
	return(x1, x2)

print ("QuadS:", QuadS(6,5,-4),"\t","QuadA:", QuadA(6,5,-4))
print ("QuadS:",QuadS(6*(10**30), 5*(10**30), -4*(10**30)),"\t", "QuadA:",QuadA(6*(10**30), 5*(10**30), -4*(10**30)))
print ("QuadS:",QuadS(0, 1, 1),"\t","QuadA:", QuadA(0,1,1))
print ("QuadS:",QuadS(1, -10**5, 1),"\t","QuadA:", QuadA(1, -10**5, 1))
print ("QuadS:",QuadS(1, -4, 3.999999),"\t", "QuadA:",QuadA(1,-4,3.999999))
print ("QuadS:",QuadS(10**-30, -10**30, 10**30),"\t", "QuadA:",QuadA(10**-30, -10**30, 10**30))


