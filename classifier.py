import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from scipy.sparse import hstack


def train_and_predict(dftrained, dfpred):
    feat_list = ['description','tel', 'address', 'ftl', 'sc', 'ads', 'cart', 'sign', 'login', 'ar2k', 'ln20k']
    feat_list_full = ['description','tel', 'address', 'ftl', 'sc', 'ads', 'cart', 'sign', 'login', 'ar2k', 'ln20k', 'cloud', 'target']
    dftrained = dftrained[feat_list_full]
    dftrained['classified'] = 1
    dfpred['classified'] = 0
    vectlist = []
    sumdf = pd.concat([dftrained, dfpred], ignore_index=True)
    sumdf.cloud = sumdf.cloud.astype('string')
    for i in range(len(sumdf)):
        vectlist.append(sumdf.loc[[i], ['cloud']].values.item())
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(vectlist)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X)
    X_trained = X_train_tfidf[:len(dftrained)]
    X_pred = X_train_tfidf[len(dftrained):]
    y = sumdf['target'][:len(dftrained)]
    feat_train = sumdf[feat_list][:len(dftrained)]
    feat_pred = sumdf[feat_list][len(dftrained):]
    f_train = feat_train.to_numpy()
    f_pred = feat_pred.to_numpy()
    X_train_feat = hstack((X_trained, f_train))
    X_pred_feat = hstack((X_pred, f_pred))
    X_train, X_test, y_train, y_test = train_test_split(X_train_feat, y, test_size=0.25, random_state=42)
    clf=RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    score = metrics.f1_score(y_test, pred)
    res = y_test.to_frame()
    res['pred'] = pred
    #for index, row in res.iterrows():
    #    if row['target'] != row['pred']:
    #        print("index of error : ", index)
    #        listoferrors.append(index)
    #print ("accuracy:   %0.3f" % score)
    pred_res = clf.predict(X_pred_feat)
    dfpred['target'] = pred_res
    return dfpred[['target']]