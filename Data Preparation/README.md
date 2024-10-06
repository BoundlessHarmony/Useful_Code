# Data Preparation and Cleaning Code

This folder contains Python scripts and utilities for preparing and cleaning data to ensure it is ready for analysis or machine learning workflows. The scripts in this folder handle common tasks such as handling missing data, normalization, standardization, and feature engineering.

## Contents

- `missing_data_handler.py`: A script to detect and handle missing values using different strategies (mean, median, mode, etc.).
- `outlier_removal.py`: A utility to identify and remove or treat outliers using methods like z-scores or interquartile ranges (IQR).
- `normalization.py`: A script to normalize data between 0 and 1 or scale it using other techniques such as Min-Max scaling.
- `standardization.py`: A utility to standardize features to have zero mean and unit variance.
- `feature_encoding.py`: A script to encode categorical variables using one-hot encoding, label encoding, or target encoding.
- `data_splitter.py`: A script to split the dataset into training, validation, and testing sets.

## Getting Started

### Prerequisites

To use these scripts, ensure you have the following Python libraries installed. You can install them by running:

```bash
pip install -r requirements.txt
