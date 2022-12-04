import numpy as np
import pandas as pd
import os
from load import *
from splitdata import save_me_csv
from pandas.plotting import scatter_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

# C:\Users\Boundless\PycharmProjects\ML\Project_1_Housing\datasets\housing\Data_Index_bck

def load_data(File=None):
    if File is None:
        print("No input provided!")
        path_name = str(input("Input Path:"))
        file_name = str(input("Input file name"))
        file_call = os.path.join(path_name, file_name)
        data = pd.read_csv(file_call)
    else:
        print("God is love")
        data = pd.read_csv(File)
    return data

data = load_data("C:\\Users\\Boundless\\PycharmProjects\\ML\\Project_1_Housing\\datasets\\housing\\Data_Index_bck\\Train_Set.csv")
# successful import of stratified training set

# We are about to transform the data : But we don't want to transform the predictors and the labels the same way,
# so we will instead drop the median house value and make a copy so we can explore a bit and compare

d_data = data.drop("median_house_value", axis = 1)
data_labels = data["median_house_value"].copy(deep=True)
dl = pd.DataFrame(data = data_labels)

#save_me_csv(dl)

### Success ###

# d_data.dropna(subset=["total_bedrooms"]) # Option 1, remove the entire district (row) with a missing bedroom value
# d_data.drop("total_bedrooms", axis=1) # Option 2, nuclear, remove the entire attribute

median = d_data["total_bedrooms"].median() # Option 3, replace missing values with median - step 1
d_data["total_bedrooms"].fillna(median, inplace=True)
imputer = SimpleImputer(strategy="median")
# we will run it on the whole thing to ensure no missing values, but we therefore need to drop non numerical data
d_data_num = d_data.drop("ocean_proximity", axis = 1) # remove entire attribute, no non-numerical data allowed

#imputer.fit(d_data_num)

# The Imputer just calculates the median value of each attribute, which we can also do with .median.values -> confirm
# print(imputer.statistics_)
# print(d_data_num.median().values)

#X = imputer.transform(d_data_num)
# outputs numpy array of transformed features (must restore dataframe format)
#d_tr = pd.DataFrame(X, columns=d_data_num.columns, index=d_data_num.index)
#print(d_tr)

#how to handle text and categorical attributes
#data_cat = d_data[["ocean_proximity"]]
#print(data_cat.head(10))

### Need to encode the categorical attributes into a numerical one for machine learning ###
#ordinal_encoder = OrdinalEncoder()
#data_cat_enc = ordinal_encoder.fit_transform(data_cat)
#print(data_cat_enc[:10])

### ML Algs tend to assume nearby values are more similar than two distant values. but the way we just encoded, 0 and 4 are more similar, contradicting this ###

#cat_encoder = OneHotEncoder()
#data_cat_1hot = cat_encoder.fit_transform(data_cat)
#print(data_cat_1hot)

### Custom Transformer Example ###
rooms_ix, bedrooms_ix, population_ix, households_ix = 3,4,5,6

class CombineAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True): # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        return self # nothing else to do
    def transform(self, X):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:,households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

#attr_addr = CombineAttributesAdder(add_bedrooms_per_room=False)
#data_extra_attribs = attr_addr.transform(d_data.values)

### ML Algs generally don't fit well with different scales of numerical input, ex 0-15 vs 1-60,000 ###
### mix max or standardization are the options ###

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('attribs_addr', CombineAttributesAdder()),
    ('std_scaler', StandardScaler()),
])

data_num_tr = num_pipeline.fit(d_data_num)

### Instead of handling numerical and categorical columns separately, lets design a single transformer capable of handling all columns

nums_attribs = list(d_data_num)
cat_attribs = ['ocean_proximity']

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, nums_attribs),
    ("cat", OneHotEncoder(), cat_attribs),
])


data_prepared = full_pipeline.fit_transform(data) ### Here is the culmination ###

### success save ###
#save_me_csv(data_prepared)

lin_reg = LinearRegression()
lin_reg.fit(data_prepared, data_labels)

some_data = data_prepared[:5]
some_labels = data_labels[:5]
some_pata = full_pipeline.transform(some_data)

print("Predictions:", lin_reg.predict(some_pata))
print("Labels:", list(some_labels))