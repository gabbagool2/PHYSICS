import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


frequency = 10000
period = 1/frequency
L1 = L2 = 0.3
LT = L1 + L2
bucket_for_graph = {} # takes all the results from each dictionary and stores them for the graph


def red_wood(period, L1, L2, LT):
    P = period
    #n1 pulses
    n1 = {'test1': 1702, 'test2': 1712, 'test3': 1710}
    #results for t1
    t1 = {}
    for key, value in n1.items():
        t1[key] = round(value*P, 4)
    #n2 pulses
    n2 = {'test1': 978, 'test2': 989, 'test3': 982}
    #results for t2
    t2 = {}
    for key, value in n2.items():
        t2[key] = round(value*P, 4)
    print(f"""n1 TEST RESULTS====\n {n1}\nn2 TEST RESULTS====\n{n2}\n+++T1+++ (P x n1)\n{t1}\nn+++T2 (P x n2)+++\n{t2}""")
    #acceleration due to gravity
    g = {}
    for key in t1:
        g[key] = round((LT*(t1[key]-t2[key]))/((t1[key]*t2[key])*(t1[key]+t2[key])), 3)
    #print results
    print(f'\n-----acceleration due to gravity-----\n{g}[m/s]')
    bucket_for_graph['Red Wood'] = g 


def glass_marble(period, L1, L2, LT):
    P = period
    #n1 pulse
    n1 = {'test1': 1696, 'test2': 1708, 'test3': 1680}
    #results for t1
    t1 = {}
    for key, value in n1.items():
        t1[key] = round(value*P, 4)
    #n2 pulses
    n2 = {'test1': 972, 'test2': 972, 'test3': 969}
    #results for t2
    t2 = {}
    for key, value in n2.items():
        t2[key] = round(value*P, 4)
    print(f"""n1 TEST RESULTS====\n {n1}\nn2 TEST RESULTS====\n{n2}\n+++T1+++ (P x n1)\n{t1}\nn+++T2 (P x n2)+++\n{t2}""")
    #acceleration due to gravity
    g = {}
    for key in t1:
        g[key] = round((LT*(t1[key]-t2[key]))/((t1[key]*t2[key])*(t1[key]+t2[key])), 3)
    #print results
    print(f'\n-----acceleration due to gravity-----\n{g}[m/s]')
    bucket_for_graph['Glass Marble'] = g


def pp_ball(period, L1, L2, LT):
    P = period
    #n1 pulse
    n1 = {'test1': 1789, 'test2': 1793, 'test3': 1782}
    #results for t1
    t1 = {}
    for key, value in n1.items():
        t1[key] = round(value*P, 4)
    #n2 pulses
    n2 = {'test1': 1035, 'test2': 1035, 'test3': 1034}
    #results for t2
    t2 = {}
    for key, value in n2.items():
        t2[key] = round(value*P, 4)
    print(f"""n1 TEST RESULTS====\n {n1}\nn2 TEST RESULTS====\n{n2}\n+++T1+++ (P x n1)\n{t1}\nn+++T2 (P x n2)+++\n{t2}""")
    #acceleration due to gravity
    g = {}
    for key in t1:
        g[key] = round((LT*(t1[key]-t2[key]))/((t1[key]*t2[key])*(t1[key]+t2[key])), 3)
    #print results
    print(f'\n-----acceleration due to gravity-----\n{g}[m/s]')
    bucket_for_graph['Ping Pong Ball'] = g


def metal(period, L1, L2, LT):
    P = period
    #n1 pulse
    n1 = {'test1': 1693, 'test2': 1692, 'test3': 1681, 'test4' : 1712, 'test5' : 1699, 'test6' : 1714 }
    #results for t1
    t1 = {}
    for key, value in n1.items():
        t1[key] = round(value*P, 4)
    #n2 pulses
    n2 = {'test1': 980, 'test2': 4398, 'test3': 3806, 'test4' : 3756, 'test5' : 973, 'test6' : 974}
    #results for t2
    t2 = {}
    for key, value in n2.items():
        t2[key] = round(value*P, 4)
    print(f"""n1 TEST RESULTS====\n {n1}\nn2 TEST RESULTS====\n{n2}\n+++T1+++ (P x n1)\n{t1}\nn+++T2 (P x n2)+++\n{t2}""")
    #acceleration due to gravity
    g = {}
    for key in t1:
        g[key] = round((LT*(t1[key]-t2[key]))/((t1[key]*t2[key])*(t1[key]+t2[key])), 3)
    bucket_for_graph['Metal'] = g
    #print results
    print(f'\n-----acceleration due to gravity-----\n{g}[m/s]')
    #checks if results are close as we have error when doing experiment
    target = 9.81
    tolerance = 0.5
    valid_results = {}
    for key, value in g.items():
        if abs(value - target) <= tolerance:
            valid_results[key] = value
    print(f' !!! VALID RESULTS FOR METAL BALL [within {tolerance} of {target}] !!!\n{valid_results}')
    bucket_for_graph['Metal (Valid Only)'] = valid_results 

#executes
print(f"\n\nFREQUENCY = {frequency}\nPERIOD = {period} seconds\n\n\n")
print('\n\n%%         RED WOODEN BALL         %%')
red_wood(period, L1, L2, LT)
print('\n\n%%         Glass Marble         %%')
glass_marble(period, L1, L2, LT)
print('\n\n%%         PING PONG BALL        %%')
pp_ball(period, L1, L2, LT)
print('\n\n%%         METAL BALL         %%')
metal(period, L1, L2, LT)
#graph handling
materials = list(bucket_for_graph.keys())
all_test_names = set()
for m in materials:
    all_test_names.update(bucket_for_graph[m].keys())
sorted_tests = sorted(list(all_test_names))
x = np.arange(len(materials))
width = 0.12 
multip = 0
fig, ax = plt.subplots(figsize=(12, 10)) 
for test in sorted_tests:
    offset = width * multip
    values = [bucket_for_graph[m].get(test, np.nan) for m in materials]
    ax.bar(x + offset, values, width, label=test)
    multip += 1
ax.axhline(y=9.81, color='red', linestyle='-', linewidth=1.5, label='Theoretical g (9.81)')
ax.axhline(y=0, color='black', linestyle='-', linewidth=2, label='zero')
ax.set_ylabel('Calculated g ($m/s^2$)')
ax.set_title(' Acceleration due to gravity for each material ')
ax.set_xticks(x + width * 2.5) 
ax.set_xticklabels(materials)
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))
ax.grid(which='major', axis='y', linestyle='-', alpha=0.6, color='gray')
ax.grid(which='minor', axis='y', linestyle=':', alpha=0.4, color='gray')

#executes graph
plt.tight_layout()
#plt.show()
plt.savefig('plot.png')