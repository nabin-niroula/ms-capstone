from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.metrics import confusion_matrix


def stacking_classifier():
    base_model = []
    base_model.append(('rf', RandomForestClassifier(n_estimators=100,random_state=42,max_depth=15, n_jobs=-1)))
    base_model.append(('dt', DecisionTreeClassifier(random_state=42,max_depth=15)))
    meta_learner = MLPClassifier(hidden_layer_sizes=(100), activation="relu", max_iter=500, learning_rate="invscaling")
    model = StackingClassifier(estimators=base_model, final_estimator=meta_learner, cv=5)
    return model

# Standardize the datasets
X_scaled = StandardScaler()
X = X_scaled.fit_transform(X)

#separate the dataset into train and test set
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.7, random_state=42)

#Analyze differnt features and decide on the best 7 features that can be used to predict malicious DoH traffics
# select_feature = SelectKBest(mutual_info_classif, k=19).fit(X_train,y_train)
select_feature = SelectKBest(mutual_info_classif, k=7).fit(X_train,y_train)
X_train = select_feature.transform(X_train)
X_test = select_feature.transform(X_test)

#pass data to the model
model = stacking_classifier()
model = model.fit(X_train,y_train)
y_pred = model.predict(X_test)

#validate the model for its possibility to continue with the simulation
accuracy = model.score(X_test, y_test)
accuracy

# verify how good model is at predicting - false positive, false negative, true positive, and true negatives
confusion_matrix(y_test,y_pred)

# does this model suffice to generalize the output over a big set of dataset and features
# this provides cross validation score
cv_score = cross_val_score(model, X, y, cv=5,scoring="recall_macro")
cv_score.mean()
