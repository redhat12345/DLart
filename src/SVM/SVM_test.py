from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from scipy import misc
import numpy as np
from collections import defaultdict
from sklearn.externals import joblib
import utils
import h5py as h5
import sys


def predToH5(features, classes, clf, outFile, report=False):
    y_true, y_pred = classes, clf.predict(features)
    if report:
        print(classification_report(y_true, y_pred))

    probabilities = np.empty(shape=(len(classes), len(set(classes))))
    results = clf.predict_proba(features)

    for i in range(len(classes)):
        # get the probabilities matrix for each image
        probabilities[i] = results[i]

    h5f = h5.File(outFile, "w")
    h5f.create_dataset("prediction", data=probabilities)
    h5f.close()


def predToH5_1(features, outFile, clf, folder=False):
    if folder:
        results = clf.predict_proba(features)
    else:
        results = clf.predict_proba([features])
    h5f = h5.File(outFile, "w")
    h5f.create_dataset("prediction", data=results)
    h5f.close()


def main():
    # Read the arguments
    dataPath = sys.argv[1] # not in use
    net = sys.argv[2]
    name = sys.argv[3]  # noisy23 / noisy/ curated
    dataset = sys.argv[4]

    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))

    test = ""
    # dataPath = '/media/mlagunas/a0148b08-dc3a-4a39-aee5-d77ee690f196/TFG/test'
    # net = "trainf"
    # name = "curated"  # noisy23 / noisy/ curated
    # dataset = "curated"
    # clf = joblib.load(dataPath + "/SVM/SVM.pkl")

    # Load the pre-trained SVM
    print "========> Loading SVM pickle"
    if net == "vgg19":
        clf = joblib.load(dir_path + "../models/SVM/SVMft_curated.pkl")
    elif net == "trainf":
        clf = joblib.load("../models/SVM/SVMft_train.pkl")
    else:
        print "ERROR loading pickle"

    features = "models/h5/curated/features/trainf/curated_trainf_"

    if sys.argv[5] != None:
        features = sys.argv[5]
        out = sys.argv[6]
        folder = sys.argv[7]
        feat = utils.getFeatures(features, "features")
        predToH5_1(feat, out, clf, folder)
    else:
        features = "../models/h5/" + dataset + "/features/" + \
            net + "/" + name + "_" + net + "_"
        cl = "../../data/paths/" + dataset + "/" + name + "_paths"

        # Get features
        feat = utils.getFeatures(features + "42.h5", "features")
        feat_train = utils.getFeatures(features + "train_42.h5", "features")
        feat_crossv = feat_train[:int(len(feat_train) * 0.2)]
        feat_test = utils.getFeatures(features + "test_42.h5", "features")

        # Load classes
        classes, path = utils.getClasses(cl + ".txt")
        classes_train, path_train = utils.getClasses(cl + "_train.txt")
        classes_crossv, path_crossv = classes_train[
            :int(len(classes_train) * 0.2)], path_train[:int(len(path_train) * 0.2)]
        classes_test, path_test = utils.getClasses(cl + "_test.txt")

        predToH5(feat_test, classes_test, clf, "../models/h5/" + dataset + "/svm/" +
                 net + "/" + name + test + "_" + net + "_probabilities_test.h5")
        predToH5(feat_train, classes_train, clf, "../models/h5/" + dataset +
                 "/svm/" + net + "/" + name + test + "_" + net + "_probabilities_train.h5")
        predToH5(feat, classes, clf, "../models/h5/" + dataset + "/svm/" +
                 net + "/" + name + test + "_" + net + "_probabilities.h5")


#
# dataPath = '/media/mlagunas/a0148b08-dc3a-4a39-aee5-d77ee690f196'
# net = "train1"
# name = "noisy23"  # noisy23 / noisy/ curated
# test = ""
# dataset = "noisy"

if __name__ == "__main__":
    main()                                        
