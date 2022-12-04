import os
import pandas
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

housing_Path = os.path.join("../datasets", "housing")

def load_housing_data(housing_path=housing_Path):
    csv_path = os.path.join(housing_path, "housing.csv")
    data = pd.read_csv(csv_path)
    #housing_dataframe = pd.DataFrame(csv_path,)
    return data

#generalized data import
def load_data(path):
    data = pd.read_csv(path)
    return data



#see all columns, please
#pd.set_option('display.max_columns', None)
#housing = load_housing_data()

#Get to know our data
#print(housing.head())
#print(housing.info())                           # a quick showing of the columns and number of entries, + type
#print(housing["ocean_proximity"].value_counts())  # lets check out the black sheep, the python object data type column
#quick summary of every numerical attribute#print(housing.describe())
# generate a set of histograms to check out the data distributions for each data column
#housing.hist(bins=50, figsize=(20,15))
#plt.show()

#now that we've looked at our data, we must separate a chunk and never look at (although i think
# it better if we fixed the 500k cap on housing first)