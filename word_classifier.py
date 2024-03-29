import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import constants as c
import helper_funtions as h


def train(conf):
    if not os.path.isfile(c.svm_model):
        label_encoder = LabelEncoder()

        feature_vectors = h.load_obj("training_data")

        data_frame_feature_vectors = pd.DataFrame.from_records(feature_vectors, columns=c.word_features)

        training_data = data_frame_feature_vectors.sample(conf.size_training_data)

        word_feature = training_data[c.word_features[0]].values
        encoded_word_feature = label_encoder.fit_transform(word_feature.astype(str))

        y = training_data[c.word_features[-1]].values
        x = training_data.drop([c.word_features[-1], c.word_features[0]], axis=1)

        x[c.word_features[0]] = encoded_word_feature
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train)
        x_test = scaler.transform(x_test)

        svm_model = SVC(kernel=conf.svm_kernal, C=conf.c_value, gamma=conf.gamma, verbose=1)
        svm_model.fit(x_train, y_train)

        y_pred = svm_model.predict(x_test)
        performace_report = classification_report(y_test, y_pred)

        h.save_obj(svm_model, "svm_model")
        h.save_obj(performace_report, c.svm_performance_report)

        print(confusion_matrix(y_test, y_pred))
        print(performace_report)

    else:
        svm_model = h.load_obj("svm_model")
        performace_report = h.load_obj(c.svm_performance_report)

    return svm_model, performace_report


def predict(input_feature_vectors, svm_model):

    if len(input_feature_vectors) == 0:
        return []
    label_encoder = LabelEncoder()
    data_frame_feature_vectors = pd.DataFrame.from_records(input_feature_vectors, columns=c.word_features[:-1])

    words = data_frame_feature_vectors[c.word_features[0]].values
    word_feature = data_frame_feature_vectors[c.word_features[0]].values
    encoded_word_feature = label_encoder.fit_transform(word_feature.astype(str))

    X = data_frame_feature_vectors.drop(c.word_features[0], axis=1)

    X[c.word_features[0]] = encoded_word_feature

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    y_pred = svm_model.predict(X)

    return list(zip(words, y_pred))
