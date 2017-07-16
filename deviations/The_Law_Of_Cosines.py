# The Law of Cosines

# a^2 = b^2 + c^2 - 2bc cos A
from math import pi
from trianglesolver import solve, degree

acc = 10
angle = 10


def trajectory(acc, angle):

	a,b,c,A,B,C = solve (b = acc, c = acc, A = angle*degree)
	foundLength = a 
	otherAngle = (180 - angle)/2


	a,b,c,A,B,C = solve (a = foundLength, B = otherAngle*degree, A = 90*degree)


	#working out y movement
	y = acc - c

	#working out x movement
	x = b

	return(x,y)

hiya = trajectory(acc, angle)
x = hiya[0]
y = hiya[1]

print(x)
print(y)
