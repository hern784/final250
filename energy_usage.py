import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import time
import csv


indoor_temp = []
outdoor_temp = []
desired_temp = []
t= [1,2,3,4,5,6]
f = open("example.csv","r")
cost = 0


for i in range(6):
    lineText = f.readline().split(",")
    indoor = float (lineText[0])
    outdoor = float (lineText[1])
    desire = float (lineText[2])

    indoor_temp.append(indoor)
    outdoor_temp.append(outdoor)
    desired_temp.append(desire)

    if(indoor_temp[i] > desired_temp[i]):
    	if(outdoor_temp[i] < desired_temp[i]):
    		hvac = "wind"
    		flag = 1
    		cost = cost + 0.05
    		
    	else:
    		hvac = "AC"
    		flag = 2
    		cost = cost + 0.45
    		

    if(indoor_temp[i] < desired_temp[i]):
    	if(outdoor_temp[i] < desired_temp[i]):
    		hvac = "heat"
    		flag = 2
    		cost = cost + 0.35
    		

    	else:
    		hvac = "wind"
    		flag = 1
    		cost = cost + 0.05
    		
    		
    if(indoor_temp[i] == desired_temp[i]):
    	flag = 2
    	hvac = "fan"
    	cost = cost + 0.05
    	

print(cost)
    	


if __name__ == '__main__':

	plt.plot(t,indoor_temp,'r',label = 'indoortemp')
	plt.plot(t,outdoor_temp,'b',label = 'outdoortemp')
	plt.plot(t,desired_temp,'g',label = 'desiredtemp')
	plt.ylabel('temperature (Farenheit)')
	plt.xlabel('time (hours)')
	plt.title('temperature vs time')
	plt.legend()
	plt.show()
	plt.close()

 


