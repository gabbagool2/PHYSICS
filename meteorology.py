import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Keys are Elapsed Time in Hours (0 to 168 scale)
Tstat = {0.0: 7.74, 18.5: 10.36, 25.42: 14.35, 29.42: 15.14, 49.17: 15.15, 52.25: 13.30, 61.18: 10.67, 66.98: 11.59, 74.8: 14.35, 77.26: 16.13, 81.21: 10.09, 83.91: 11.23, 89.08: 9.91, 91.51: 10.42, 98.61: 13.75, 104.03: 10.09, 108.81: 8.72, 118.91: 11.52, 122.03: 13.68, 126.48: 14.67, 128.41: 13.11, 133.51: 10.19, 139.41: 9.71, 146.36: 13.53, 148.85: 14.94, 152.8: 12.63, 158.48: 10.44}
Hstat = {0.0: 76.0, 18.5: 86.0, 25.42: 49.92, 29.42: 50.83, 49.17: 56.33, 52.25: 63.0, 61.18: 79.92, 66.98: 72.25, 74.8: 70.58, 77.26: 64.50, 81.21: 86.50, 83.91: 70.83, 89.08: 80.83, 91.51: 69.33, 98.61: 58.33, 104.03: 86.50, 108.81: 71.92, 118.91: 71.08, 122.03: 63.17, 126.48: 59.0, 128.41: 49.0, 133.51: 64.0, 139.41: 73.50, 146.36: 65.75, 148.85: 61.83, 152.8: 59.17, 158.48: 59.92}
Pstat = {0.0: 1025.93, 18.5: 1022.0, 25.42: 1020.69, 29.42: 1021.93, 49.17: 1021.83, 52.25: 1023.22, 61.18: 1021.30, 66.98: 1021.71, 74.8: 1024.72, 77.26: 1025.23, 81.21: 1024.79, 83.91: 1028.33, 89.08: 1029.27, 91.51: 1030.13, 98.61: 1030.87, 104.03: 1024.79, 108.81: 1030.41, 118.91: 1029.91, 122.03: 1029.75, 126.48: 1028.90, 128.41: 1026.28, 133.51: 1029.07, 139.41: 1027.11, 146.36: 1025.76, 148.85: 1024.52, 152.8: 1020.33, 158.48: 1021.80}
# Met Office Readings
Tmet = {0.0: 7.0, 18.5: 6.0, 25.42: 12.0, 29.42: 9.0, 49.17: 11.0, 52.25: 11.0, 61.18: 9.0, 66.98: 11.0, 74.8: 12.0, 77.26: 12.0, 81.21: 11.0, 83.91: 8.0, 89.08: 8.0, 91.51: 8.0, 98.61: 10.0, 104.03: 10.0, 108.81: 6.0, 118.91: 11.0, 122.03: 13.0, 126.48: 13.0, 128.41: 11.0, 133.51: 7.0, 139.41: 6.0, 146.36: 13.0, 148.85: 13.0, 152.8: 11.0, 158.48: 7.0}
Hmet = {0.0: 85.0, 18.5: 86.0, 25.42: 58.0, 29.42: 70.0, 49.17: 72.0, 52.25: 72.0, 61.18: 88.0, 66.98: 78.0, 74.8: 82.0, 77.26: 84.0, 81.21: 96.0, 83.91: 93.0, 89.08: 90.0, 91.51: 89.0, 98.61: 72.0, 104.03: 72.0, 108.81: 82.0, 118.91: 73.0, 122.03: 65.0, 126.48: 59.0, 128.41: 65.0, 133.51: 87.0, 139.41: 92.0, 146.36: 63.0, 148.85: 62.0, 152.8: 67.0, 158.48: 84.0}
Pmet = {0.0: 1027.0, 18.5: 1022.0, 25.42: 1023.0, 29.42: 1023.0, 49.17: 1024.0, 52.25: 1023.0, 61.18: 1023.0, 66.98: 1024.0, 74.8: 1026.0, 77.26: 1027.0, 81.21: 1028.0, 83.91: 1030.0, 89.08: 1031.0, 91.51: 1032.0, 98.61: 1033.0, 104.03: 1033.0, 108.81: 1033.0, 118.91: 1032.0, 122.03: 1032.0, 126.48: 1031.0, 128.41: 1031.0, 133.51: 1031.0, 139.41: 1029.0, 146.36: 1028.0, 148.85: 1026.0, 152.8: 1024.0, 158.48: 1023.0}
# Time of Day (t1 = 8am-4pm, t2 = 4pm-12am, t3 = 12am-8am)
t1 = {0.0: True, 18.5: False, 25.42: True, 29.42: False, 49.17: True, 52.25: True, 61.18: False, 66.98: False, 74.8: True, 77.26: True, 81.21: False, 83.91: False, 89.08: False, 91.51: False, 98.61: True, 104.03: False, 108.81: False, 118.91: True, 122.03: True, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: True, 148.85: True, 152.8: False, 158.48: False}
t2 = {0.0: False, 18.5: False, 25.42: False, 29.42: True, 49.17: False, 52.25: False, 61.18: True, 66.98: False, 74.8: False, 77.26: False, 81.21: True, 83.91: True, 89.08: False, 91.51: False, 98.61: False, 104.03: True, 108.81: True, 118.91: False, 122.03: False, 126.48: True, 128.41: True, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: True, 158.48: False}
t3 = {0.0: False, 18.5: True, 25.42: False, 29.42: False, 49.17: True, 52.25: False, 61.18: False, 66.98: True, 74.8: False, 77.26: False, 81.21: False, 83.91: False, 89.08: True, 91.51: True, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: True, 139.41: True, 146.36: False, 148.85: False, 152.8: False, 158.48: True}
# Cloud Cover (c1 = clear, c2 = mild/patchy, c3 = full)
c1 = {0.0: False, 18.5: False, 25.42: False, 29.42: False, 49.17: False, 52.25: True, 61.18: True, 66.98: False, 74.8: False, 77.26: False, 81.21: False, 83.91: False, 89.08: False, 91.51: False, 98.61: False, 104.03: True, 108.81: True, 118.91: True, 122.03: True, 126.48: True, 128.41: True, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
c2 = {0.0: True, 18.5: False, 25.42: True, 29.42: False, 49.17: False, 52.25: False, 61.18: False, 66.98: False, 74.8: True, 77.26: False, 81.21: True, 83.91: False, 89.08: False, 91.51: False, 98.61: True, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: True, 139.41: True, 146.36: True, 148.85: True, 152.8: True, 158.48: True}
c3 = {0.0: False, 18.5: True, 25.42: False, 29.42: True, 49.17: True, 52.25: False, 61.18: False, 66.98: True, 74.8: False, 77.26: True, 81.21: False, 83.91: True, 89.08: True, 91.51: True, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
# Wind (w1 = no/mild, w2 = mid, w3 = heavy)
w1 = {0.0: False, 18.5: False, 25.42: False, 29.42: False, 49.17: False, 52.25: False, 61.18: True, 66.98: False, 74.8: True, 77.26: False, 81.21: True, 83.91: False, 89.08: False, 91.51: False, 98.61: True, 104.03: False, 108.81: False, 118.91: True, 122.03: True, 126.48: False, 128.41: False, 133.51: True, 139.41: False, 146.36: True, 148.85: False, 152.8: False, 158.48: True}
w2 = {0.0: True, 18.5: True, 25.42: True, 29.42: True, 49.17: True, 52.25: True, 61.18: False, 66.98: True, 74.8: False, 77.26: True, 81.21: False, 83.91: True, 89.08: True, 91.51: True, 98.61: False, 104.03: True, 108.81: True, 118.91: False, 122.03: False, 126.48: True, 128.41: True, 133.51: False, 139.41: True, 146.36: False, 148.85: True, 152.8: True, 158.48: False}
w3 = {0.0: False, 18.5: False, 25.42: False, 29.42: False, 49.17: False, 52.25: False, 61.18: False, 66.98: False, 74.8: False, 77.26: False, 81.21: False, 83.91: False, 89.08: False, 91.51: False, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
# Precipitation (r1 = none, r2 = light, r3 = heavy)
r1 = {0.0: True, 18.5: True, 25.42: True, 29.42: True, 49.17: True, 52.25: True, 61.18: True, 66.98: True, 74.8: True, 77.26: False, 81.21: True, 83.91: True, 89.08: True, 91.51: True, 98.61: True, 104.03: True, 108.81: True, 118.91: True, 122.03: True, 126.48: True, 128.41: True, 133.51: True, 139.41: True, 146.36: True, 148.85: True, 152.8: True, 158.48: True}
r2 = {0.0: False, 18.5: False, 25.42: False, 29.42: False, 49.17: False, 52.25: False, 61.18: False, 66.98: False, 74.8: False, 77.26: True, 81.21: False, 83.91: False, 89.08: False, 91.51: False, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
r3 = {0.0: False, 18.5: False, 25.42: False, 29.42: False, 49.17: False, 52.25: False, 61.18: False, 66.98: False, 74.8: False, 77.26: False, 81.21: False, 83.91: False, 89.08: False, 91.51: False, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
# Visibility (v1 = none, v2 = 5-10m, v3 = horizon)
v1 = {0.0: True, 18.5: False, 25.42: False, 29.42: False, 49.17: False, 52.25: False, 61.18: True, 66.98: False, 74.8: False, 77.26: False, 81.21: False, 83.91: False, 89.08: False, 91.51: False, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
v2 = {0.0: False, 18.5: True, 25.42: False, 29.42: False, 49.17: False, 52.25: True, 61.18: False, 66.98: False, 74.8: False, 77.26: False, 81.21: True, 83.91: True, 89.08: True, 91.51: False, 98.61: False, 104.03: False, 108.81: False, 118.91: False, 122.03: False, 126.48: False, 128.41: False, 133.51: False, 139.41: False, 146.36: False, 148.85: False, 152.8: False, 158.48: False}
v3 = {0.0: False, 18.5: False, 25.42: True, 29.42: True, 49.17: True, 52.25: False, 61.18: False, 66.98: True, 74.8: True, 77.26: True, 81.21: False, 83.91: False, 89.08: False, 91.51: True, 98.61: True, 104.03: True, 108.81: True, 118.91: True, 122.03: True, 126.48: True, 128.41: True, 133.51: True, 139.41: True, 146.36: True, 148.85: True, 152.8: True, 158.48: True}

def analyse(station_dict, met_dict):
    diff_dict = {}
    for time_key in station_dict:
        diff_dict[time_key] = round(station_dict[time_key] - met_dict[time_key], 2)
    #dictionary of difference values
    diff_values = np.array(list(diff_dict.values()))
    #average difference over that dict
    av_diff = np.mean(diff_values)
    #std_dev over that dict
    #ddof=1 = n-1 for s^2 calc
    std_dev_diff = np.std(diff_values, ddof=1)
    return diff_dict, round(av_diff, 3), round(std_dev_diff, 3)

def calculate_accuracy_probability(mean_diff, std_dev, tolerance):
    #Calculates the probability that the weather forecast error falls within an acceptable +/- tolerance, assuming a Normal Dist.
    # 1. tolerance bounds
    lower_bound = -tolerance
    upper_bound = tolerance
    # 2. Calculate the Z-scores for these bounds
    z_lower = (lower_bound - mean_diff) / std_dev
    z_upper = (upper_bound - mean_diff) / std_dev
    # 3. Calculate the cumulative probability area between the Z-scores
    probability = stats.norm.cdf(z_upper) - stats.norm.cdf(z_lower)
    # 4. Convert to a readable percentage
    return round(probability * 100, 2)

def calculate_empirical_probability(diff_dict, tolerance):
#this is just for finding humidity probability 
    successes = 0
    total_readings = len(diff_dict)
    for error in diff_dict.values():
        if -tolerance <= error <= tolerance:
            successes += 1   
    probability = successes / total_readings
    return round(probability * 100, 2)


#these call the analyse() function and create 3 dictionaries that contain the differences between station and met readings
Dt, av_T, std_T = analyse(Tstat, Tmet)
Dh, av_H, std_H = analyse(Hstat, Hmet)
Dp, av_P, std_P = analyse(Pstat, Pmet)

# debug - keep eye for anomalies graph might not catch!
print(f"Temperature Differences: {Dt}")
print(f"Temp Bias (av): {av_T}°C, Temp Std Dev: {std_T}°C\n")
print(f"Humidity Differences: {Dh}")
print(f"Humidity Bias (av): {av_H}%, Humidity Std Dev: {std_H}%\n")
print(f"Pressure Differences: {Dp}")
print(f"Pressure Bias (av): {av_P}hPa, Pressure Std Dev: {std_P}hPa\n")


# Define tolerance
tol_T = 1.5  #c
tol_H = 5.0  #%
tol_P = 2.0  #hpa

prob_T = calculate_accuracy_probability(av_T, std_T, tol_T)
prob_P = calculate_accuracy_probability(av_P, std_P, tol_P)

prob_H = calculate_empirical_probability(Dh, tol_H)

print(f"--- OVERALL FORECAST ACCURACY PROBABILITIES ---")
print(f"Probability the Met Temp is within +/- {tol_T}°C (Normal Dist): {prob_T}%")
print(f"Probability the Met Humidity is within +/- {tol_H}% (Empirical): {prob_H}%")
print(f"Probability the Met Pressure is within +/- {tol_P}hPa (Normal Dist): {prob_P}%")

# 1. Extract the X-axis (Elapsed Time) and Y-axes (Differences)
time_hours = list(Dt.keys())
diff_T = list(Dt.values())
diff_H = list(Dh.values())
diff_P = list(Dp.values())
#create matplot parameters
# 2. Create the Figure and Stacked Subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

#Top Temperature
ax1.plot(time_hours, diff_T, marker='o', color='firebrick', linestyle='-', label='Temp Diff')
ax1.axhline(y=0, color='black', linestyle='-', linewidth=2, label='Perfect Match (Zero Error)')
ax1.set_ylabel('Temp Diff (°C)')
ax1.set_title('Weather Forecast Residuals (Station Reading - Met Office)')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')
# Middle Humidity
ax2.plot(time_hours, diff_H, marker='o', color='dodgerblue', linestyle='-', label='Humidity Diff')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax2.set_ylabel('Humidity Diff (%)')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend(loc='upper right')

#Bottom Pressure
ax3.plot(time_hours, diff_P, marker='o', color='forestgreen', linestyle='-', label='Pressure Diff')
ax3.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax3.set_ylabel('Pressure Diff (hPa)')
ax3.set_xlabel('Elapsed Time (Hours)')
ax3.grid(True, linestyle=':', alpha=0.6)
ax3.legend(loc='upper right')
#shows graph 
plt.tight_layout()
plt.show()

