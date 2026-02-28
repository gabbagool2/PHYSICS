
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import numpy as np

n = 60 #oscillations

#inital dictionaries of current vs time {i:t}

run1 = {2: 11.39, 1.8: 11.91, 1.6: 12.76, 1.4: 13.60, 1.2: 14.59, 1: 16.41, 0.8: 18.56, 0.6: 21.11, 0.4: 26.07, 0.2: 37.9, 0.1: 58.40}
run2 = {2: 11.34, 1.8: 11.99, 1.6: 12.76, 1.4: 13.54, 1.2: 14.65, 1: 16.16, 0.8: 18.02, 0.6: 21.14, 0.4: 25.95, 0.2: 37.73, 0.1: 58.56}
run3 = {2: 11.35, 1.8: 11.97, 1.6: 12.73, 1.4: 13.75, 1.2: 14.66, 1: 16.17, 0.8: 18.02, 0.6: 20.95, 0.4: 26.07, 0.2: 37.96, 0.1: 58.31}

def period(dict, n):
    #finds period
    Period_Dict = {}
    for i, t in dict.items():
        T = round((t/n), 10)  #time/oscillations
        Period_Dict[i] = T
    return Period_Dict

def frequency(dict):
    #finds inverse of the period
    freqDict = {}
    for i, T in dict.items():
        invT = round(1/(T**2), 10)
        freqDict[i] = invT
    return freqDict



#prints period results
getT1 = period(run1, n)
getT2 = period(run2, n)
getT3 = period(run3, n)
print(f"RUN1 +=+ current : time/oscillations\n{getT1}\n")
print(f"RUN2 +-+ current : time/oscillations\n{getT2}\n")
print(f"RUN3 +*+ current : time/oscillations\n{getT3}\n")
#prints inverse period results
getinvT1 = frequency(getT1)
getinvT2 = frequency(getT2)
getinvT3 = frequency(getT3)
print(f"RUN1 +=+ current : time/1/T\n{getinvT1}\n")
print(f"RUN2 +-+ current : time/1/T\n{getinvT2}\n")
print(f"RUN3 +*+ current : time/1/T\n{getinvT3}\n")



#gets current. only needed once as remains unchanged across dictionaries
x_axis = sorted(getinvT1.keys())
#gets # y values in form of 1/T^2
Y1 = [getinvT1[i] for i in x_axis]
Y2 = [getinvT2[i] for i in x_axis]
Y3 = [getinvT3[i] for i in x_axis]
#combines the lists
Yarray = [Y1, Y2, Y3]
xline = np.array([0, 2.1])


titles = ["RUN1", "RUN2", "RUN3"]
colors = ["blue", "green", "purple"]

for i in range(3):
    plt.figure(figsize=(8, 6)) 
    slope, inter = np.polyfit(x_axis, Yarray[i], 1)
    yline = (slope * xline + inter)
    plt.plot(xline, yline, color="red", linestyle="solid", alpha=0.6, 
             label=(f"bf line = {slope:.6f}"))
    plt.scatter(x_axis, Yarray[i], color=colors[i], label=titles[i], marker="+")
    plt.title(f"1/T^2 vs current (i) - {titles[i]}")
    plt.xlabel("current(i) through coil (A)")
    plt.ylabel("1/T^2 (s^-2)")
    # Setting axis limits
    plt.xlim(0, 2.2)
    plt.ylim(0, 30)
    plt.grid(True, linestyle=":", alpha=0.9)
    plt.legend()
plt.show()
