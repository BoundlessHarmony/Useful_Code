from sklearn.linear_model import LinearRegression
from load import load_data
import pandas as pd


dpath = 'C:\\Users\\Boundless\\PycharmProjects\\ML\\Project_1_Housing\\datasets\\housing\\prepared_data.csv'
lpath = "C:\\Users\\Boundless\\PycharmProjects\\ML\\Project_1_Housing\\datasets\\housing\\data_labels.csv"

pata = load_data(dpath)
pata_labels = load_data(lpath)
print(type(pata_labels))
print(pata_labels.columns)


lin_reg = LinearRegression()
lin_reg.fit(pata, pata_labels)

some_data = pata.iloc[:5]
some_labels = pata_labels.iloc[:5]
some_pata = full_pipeline.transform
