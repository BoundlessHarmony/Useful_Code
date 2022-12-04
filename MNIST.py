from sklearn.datasets import fetch_openml
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.base import clone
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix

np.random.seed(42)
mpl.rc('axes', labelsize=14)
mpl.rc('xtick', labelsize=12)
mpl.rc('ytick', labelsize=12)

PROJECT_ROOT_DIR = ""
CHAPTER_ID = "classification"
IMAGES_PATH = os.path.join(PROJECT_ROOT_DIR, "images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

# mnist = fetch_openml('mnist_784', version=1)
# print(type(mnist))
# # # # print(mnist.keys())
# # #
# X, y = mnist["data"], mnist["target"]
# print(type(X))
# print(type(y))
# #
# # # lets avoid fetching repeatedly #
# d = open("mnist_data.pkl", "wb")
# pickle.dump(X,d)
# d.close()
# #
# l = open("mnist_labels.pkl", "wb")
# pickle.dump(y,l)
# l.close()
# ----------------------------------------------------------------------------------------- #
#faster data hua #
with open("mnist_data.pkl", "rb") as praise:
    X = pickle.load(praise)
with open("mnist_labels.pkl", "rb") as worship:
    y = pickle.load(worship)
# print(type(X)) --> pandas.core.frame.DataFrame
# print(type(y)) --> pandas.core.series.Series

some_digit = X.iloc[0]

# pandas.core.series.Series do not have reshape method. convert to array, then reshape. #
some_im_array = some_digit.values
some_digit_image = some_im_array.reshape((28,28))
plt.imshow(some_digit_image, cmap=mpl.cm.binary)
plt.axis("off")
# plt.show()

# y labels are strings # --> coerce int type
y = y.astype(np.uint8) # -> np.uint8 = unsigned int 0-255

# must split data! data set comes pre shuffled.

X_train, X_Test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
# print(type(X_train)) --> pandas.core.frame.DataFrame
# test index error fix -> convert entire DF to array before split, check type before .split() call
X_train_vals = X_train.to_numpy()
X_Test_vals = X_Test.to_numpy()
y_train_vals = y_train.to_numpy()
y_test_vals = y_test.to_numpy()

# ----------------------------------------------------------------------------------------- #
## Binary Classifier Example ##

y_train_5 = (y_train == 5)
y_test_5 = (y_test == 5)
sgd_clf =SGDClassifier(random_state=42)
sgd_clf.fit(X_train_vals, y_train_5)

# print(sgd_clf.predict([some_digit])) ---> model predicts 5, huzzah
# ----------------------------------------------------------------------------------------- #
#                               cross - validation by hand                                  #
# skfolds = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
#
# for train_index, test_index in skfolds.split(X_train_vals, y_train_5):
#     clone_clf = clone(sgd_clf)
#     X_train_folds = X_train_vals[train_index] # --> index error, index --> repaired
#     y_train_folds = y_train_5[train_index]
#     X_test_fold = X_train_vals[test_index]
#     y_test_fold = y_train_5[test_index]
#
#     clone_clf.fit(X_train_folds, y_train_folds)
#     y_pred = clone_clf.predict(X_test_fold)
#     n_correct = sum(y_pred == y_test_fold)
#     print(n_correct/ len(y_pred))
#
# # results
# # 0.9669
# # 0.91625
# # 0.96785
#
# # ----------------------------------------------------------------------------------------- #
# #                               cross - validation sklearn                                  #
# print(cross_val_score(sgd_clf, X_train_vals, y_train_5, cv=3, scoring="accuracy")) # --> [0.95035 0.96035 0.9604 ]
# print(cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")) # --> [0.95035 0.96035 0.9604 ]
# Accuracy is not the best metric. What if we guessed nothing was 5? 90% accuracy rating. --> Confusion Matrix

# ----------------------------------------------------------------------------------------- #
#                                         Confusion Matrix                                  #
# y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)
# print(confusion_matrix(y_train_5, y_train_pred))
# [[53892   687]
#  [ 1891  3530]]
# # for demo of confusion matrix
# y_train_perfect_predictions = y_train_5
# print(confusion_matrix(y_train_5, y_train_perfect_predictions))
# [[54579     0]
#  [    0  5421]]



print("conclude")