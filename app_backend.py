import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
pd.options.mode.chained_assignment = None  # default='warn'
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import time

# main logic
def predict_action_taken(short_description):

    # As we are getting 100% accuracy level and minimum time-execution with Decision Tree Classifier, so we are choosing that for building our app
    data = pd.read_csv('dataset_LabelEncoder.csv')
    model = DecisionTreeClassifier()

    # as 'Short Description' is in text, so we need to convert it into text features using CountVectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data['Short Description'])
    y = data['Action Taken Encoded']

    # model fitting
    model.fit(X,y)

    # reverse mapping for label encoder
    reverse_mapping = {}
    for i in data.index:
        if int(data['Action Taken Encoded'][i]) not in reverse_mapping:
            reverse_mapping[int(data['Action Taken Encoded'][i])] = str(data['Action Taken'][i])

    for k,v in reverse_mapping.items():
        print(k,'-->',v)

    # preprocessing user input
    input_vector = vectorizer.transform([short_description])
    
    # make prediction
    predicted_encoded_action = model.predict(input_vector)[0]
    
    predicted_action = reverse_mapping.get(predicted_encoded_action,'unknown')
    
    return predicted_action

# Testing
# user_input = 'grapes.ggn.is.smartgurucool.com C:\ Label:OS Disk  Serial Number 884ECD66 8 %'
# predicted_action = predict_action_taken(user_input)
# print(f"Predicted Action Taken: {predicted_action}")