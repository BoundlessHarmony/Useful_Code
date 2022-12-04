# now we go a bit more in depth into the data set

import numpy as np
import pandas as pd
import os
from load import *
from splitdata import save_me_csv
from pandas.plotting import scatter_matrix

data = load_housing_data()
# data.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4, s=data["population"]/100,
# label="Population", figsize=(10,7), c="median_house_value", cmap=plt.get_cmap("jet"), colorbar =True)
# plt.show()

# plot indicates a clustering algorithm may be useful, and so might ocean proximity, but it's not as effective up North
# check r, the coefficient of correlation between every pair of attributes

#                                                                           #
# ~~~~~~~~~~~~~~~~~~~~~~~LOOKING FOR CORRELATIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                           #

corr_matrix = data.corr()
# print(corr_matrix)
# check just median house value, since that's our target prediction variable

# print(corr_matrix["median_house_value"].sort_values(ascending=False))

# print(type(corr_matrix))
# save_me_csv(corr_matrix) # to preserve the coefficient information for later documentation / justification

attributes = ["median_house_value", "median_income", "total_rooms", "housing_median_age"]
scatter_matrix(data[attributes], figsize=(12, 8))
# plt.show()
# income appears to have a good correlation to median house value, confirmed by r matrix
data.plot(kind="scatter", x="median_income", y="median_house_value", alpha=0.1)
# plt.show()

# experiment with attribute combinations

data["rooms_per_household"] = data["total_rooms"] / data["households"]
data["bedrooms_per_room"] = data["total_bedrooms"] / data["total_rooms"]
data["population_per_household"] = data["population"] / data["households"]
corr_matrix = data.corr()
print(corr_matrix["median_house_value"].sort_values(ascending=False))
