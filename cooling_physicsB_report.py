import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import numpy as np


Tr = 19.028 #roomtemp 'C
a = 3.925e-3 # temperature coefficient of resistance
x = 293.82 # ref resistor (ohms)

run_1 = {0: 90, 2: 86.1, 4: 83.4, 6: 81.1, 8: 79.7, 10: 78.2, 12: 76.5, 14: 75.5} #full mug, no extra cooling
run_2 = {0: 86.3, 2: 81.5, 4: 78.2, 6: 76.6, 8: 74.9, 10: 73.5, 12: 72.1, 14: 70.1}# half full mug / occasional blowing

def finding_T(a, x, data):
# finds T values    
    probe_temp = {}
    for t, r in data.items():
        T = round((1/a)*(((2*r)-100)/(x-r)),3)
        probe_temp[t] = T
    return probe_temp

def finding_ln(probe_temp, Tr):
#finds ln(T-Tr) values
    probe_ln = {}
    for t, T in probe_temp.items():
        excess = T-Tr
        if excess > 0: #cant have log < 0
            probe_ln[t] = round(math.log(excess), 3)
        else:
            probe_ln[t] = None
    return probe_ln

#prints findings in terminal for debugging
temps_1 = finding_T(a, x, run_1)
print(f"\nRUN1: T in celsius in format minutes:temperature\n{temps_1}")
ln_temp_1 = finding_ln(temps_1, Tr)
print(f"\nRUN1: T-Tr in celsius in fromat minutes:T-Tr\n{ln_temp_1}")
temps_2 = finding_T(a, x, run_2)
print(f"\nRUN2: T in celsius in format minutes:temperature\n{temps_2}")
ln_temp_2 = finding_ln(temps_2, Tr)
print(f"\nRUN2: T-Tr in celsius in fromat minutes:T-Tr\n{ln_temp_2}")

# give T vs t #
xt_axis = list(temps_1.keys())
yt_axis = list(temps_1.values())
xt2_axis = list(temps_2.keys())
yt2_axis = list(temps_2.values())
plt.figure(figsize=(7, 6))
plt.plot(xt_axis, yt_axis, color='blue', label=':RUN 1 T: Full Mug ')
plt.plot(xt2_axis, yt2_axis, color='purple', label=':RUN 2 T: Half mug, with blowing to cool')
plt.title("Temperature vs time")
plt.xlabel("TIME(mins)")
plt.ylabel("T 'C")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()



# give ln(T-Tr) vs t #
x_axis = list(ln_temp_1.keys())
y_axis = list(ln_temp_1.values())
x2_axis = list(ln_temp_2.keys())
y2_axis = list(ln_temp_2.values())

t_array = np.array(list(ln_temp_1.keys())) # cant reuse x_Axis list cuz numpy and cant be bothered changing them back
ln_array = np.array(list(ln_temp_1.values()))
slope, inter = np.polyfit(t_array, ln_array, 1)
bf_line = slope * t_array + inter
k1 = round(-slope,3)

t2_array = np.array(list(ln_temp_2.keys())) 
ln2_array = np.array(list(ln_temp_2.values()))
slope2, inter2 = np.polyfit(t2_array, ln2_array, 1)
bf_line2 = slope2 * t2_array + inter2
k2 = round(-slope2, 3)

#generates image using following parameters
plt.figure(figsize=(7, 6))
plt.scatter(x_axis, y_axis, color='blue', marker='+', label=':RUN 1 ln(T-Tr): Full Mug')
plt.scatter(x2_axis, y2_axis, color='purple', marker='+', label=':RUN 2 ln(T-Tr): half mug, with blowing to cool')
plt.plot(t_array, bf_line, color = 'red',label=f'::k = {k1} min^-1::') #prints k1 abd k2 here instead of in terminal
plt.plot(t2_array, bf_line2, color = 'green',label=f'::k2 = {k2} min^-1::')
plt.xlabel("TIME(mins)")
plt.ylabel("EXCESS TEMP 'C --> 'ln(T-Tr)'")
plt.grid(True, linestyle=':', alpha=0.6)
plt.title("excese temperature vs time")
plt.legend()
plt.show()


# finds half life # 
half_lifeT1=round((math.log(2)/k1), 2)
half_lifeT2=round((math.log(2)/k2), 2)
print(f"half life of excess temperature from run 1 = {half_lifeT1}(mins)\n half life of excess temperature from run 2 = {half_lifeT2}(mins)\n")