#coding=utf-8
# import math
# from scipy import stats

# p = stats.poisson.pmf(15, 20)
# print("接到15个骚扰电话的概率：", p)
#
# p = stats.poisson.cdf(24, 20)
# print("接到24个骚扰电话以下的概率：", p)

# def p_possion(k, m):
#     kjie = 1  # k!
#     for i in range(1, k + 1):
#         kjie *= i
#     pk = math.pow(m, k) / kjie * math.e ** (-m)
#     return pk
#
#
# p = p_possion(15, 20)
# print("接到15个骚扰电话的概率：", p)
#
# p = 0
# for i in range(0, 25):
#     p += p_possion(i, 20)
# print("接到24个骚扰电话以下的概率：", p)


#----------------------方法一----------------------------
# import numpy as np
# from scipy.spatial import cKDTree as kdtree
# import matplotlib.pyplot as plt
#
# Nx, Ny, n_cells_reject_criteria = 1000, 1000, 3
# valid = False
#
# while not valid:
#     rate_lambda = 0.02
#     #===========generate random samples from homogeneous poisson process===========
#     mean_poisson = rate_lambda*Nx*Ny
#     n_events_pp = np.random.poisson(lam=mean_poisson)
#     x_pp = np.round(np.random.uniform(low=0, high=Nx-1, size=n_events_pp)) # generate n uniformly distributed points
#     y_pp = np.round(np.random.uniform(low=0, high=Ny-1, size=n_events_pp)) # generate n uniformly distributed points
#     coords_random_ji = ([np.int(j) for j in y_pp], [np.int(i) for i in x_pp])
#
#     #===========test there are no adjacent cells===========
#     valid = len(kdtree(coords_random_ji).query_pairs(n_cells_reject_criteria)) == 0
#
# #===========plot resuls===========
# #------- create an empty mesh
# grid = np.zeros((Ny, Nx), dtype=np.bool)
#
# #------- superimpose the results from rejection sampling
# grid[coords_random_ji] = True
#
# #------- create empty figure
# fig = plt.figure(figsize=(5, 5)) # in inches
# #------- plot
# plt.imshow(grid)
# plt.show()

#----------------------方法二----------------------------

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
# Simulation window parameters
xMin = 0;
xMax = 1000;
yMin = 0;
yMax = 1000;
xDelta = xMax - xMin;
yDelta = yMax - yMin;  # rectangle dimensions
areaTotal = xDelta * yDelta;
# Point process parameters
lambda0 = 3 * 10 ** (-5);  # intensity (ie mean density) of the Poisson process
# Simulate Poisson point process
numbPoints = scipy.stats.poisson(lambda0 * areaTotal).rvs()  # Poisson number of points
print "numbPoints",numbPoints
xx = xDelta * scipy.stats.uniform.rvs(0, 1, ((numbPoints, 1))) + xMin  # x coordinates of Poisson points
yy = yDelta * scipy.stats.uniform.rvs(0, 1, ((numbPoints, 1))) + yMin  # y coordinates of Poisson points
# Plotting
plt.scatter(xx, yy, edgecolor='b', facecolor='none', alpha=0.5)
plt.xlabel("x")
plt.ylabel("y")
plt.show()