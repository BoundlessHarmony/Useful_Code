import numpy
import numpy as np
import pandas as pd
import os

import pandas.core.frame

from load import *
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit

def split_train_test(data, test_ratio):
    shuffled_Indices = np.random.permutation(len(data))
    test_Set_size = int(len(data) * test_ratio)
    test_Indices = shuffled_Indices[:test_Set_size]
    train_Indices = shuffled_Indices[test_Set_size:]
    return data.iloc[train_Indices], data.iloc[test_Indices]


data = load_housing_data()
#train_set, test_set = split_train_test(data, 0.2) #this method is inconsistent (resampling produces different results)

train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)
#the above is purely random.
#what if we need to ensure representative sampling of a particularly strong variable?
#median income is one such variable. Lets cut it into representative categories

#brief chek
#print(len(train_set))
#print(len(test_set))
#print(len(data))

data["income_cat"] = pd.cut(data["median_income"], bins=[0., 1.5, 3.0, 4.5, 6., np.inf], labels=[1, 2, 3, 4, 5])
#print(type(data["income_cat"]))
#print(data["income_cat"], data["median_income"])
#data["income_cat"].value_counts()
#data["income_cat"].hist()
#plt.show()

# stratified sampling based on category, such that no one category is over represented and our model does not overtrain
# certain categories

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
#print(split)
for train_index, test_index in split.split(data, data["income_cat"]):
    strat_train_set = data.loc[train_index]
    strat_test_set = data.loc[test_index]

#print(strat_test_set["income_cat"].value_counts() / len(strat_test_set))

#the sampling bias comparison of overall, stratified, and random sampling reveals that the stratified sampling meth0d
# yields an order of magnitude less sampling error.

#remove the income_cat to return data to original state

#for set_ in (strat_train_set, strat_test_set):
    #set_.drop("income_cat", axis=1, inplace=True)

#save a copy of these training sets and test sets, and even the indexes for posterity and reproducibility!
def save_me_csv(your_Data):
    ''' copy ur stuff to csv for posterity. requires pandas '''
    import pandas as pd
    import numpy as np
    file_name = str(input("Enter desired CSV filename:"))
    csv_name = file_name + ".csv"
    if type(your_Data) == pandas.core.frame.DataFrame:
        try:
            your_Data.to_csv(csv_name, index = True)
            print("File saved")
        except:
            print("Something went wrong.....")
    elif type(your_Data == numpy.ndarray):
        try:
            df_data = pd.DataFrame(your_Data)
            df_data.to_csv(csv_name)
            print("File saved")
        except:
            print("Something went wrong.....")
    else:
        print("variable type mismatch, babe. Or hell, maybe something else?")

#save_me_csv(train_index)
#save_me_csv(test_index)
#save_me_csv(train_set)
#save_me_csv(test_set)

#all good! lets dig into some analysis

#data.plot(kind="scatter", x="longitude", y="latitude", alpha =0.1)
#plt.show()


