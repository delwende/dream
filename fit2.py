import numpy as np
from sklearn.ensemble import RandomForestRegressor,ExtraTreesRegressor

import scoring

def rfc_(X_train,Y_train,X_test_int,X_test_other,Y_test,max_features=1500,n_estimators=1000,max_depth=None,min_samples_leaf=1):
    print(max_features)
    def rfc_maker():
        return RandomForestRegressor(max_features=max_features,
                                     n_estimators=n_estimators,
                                     max_depth=max_depth,
                                     min_samples_leaf=min_samples_leaf,
                                     n_jobs=-1,
                                     oob_score=True,
                                     random_state=0)
        
    rfc = rfc_maker()
    rfc.fit(X_train,Y_train)
    scores = {}
    for phase,X,Y in [('train',X_train,Y_train),('test',(X_test_int,X_test_other),Y_test)]:
        if phase == 'train':
            predicted = rfc.oob_prediction_
        else:
            predicted = rfc.predict(X[1])
            predicted_int = rfc.predict(X[0])
            predicted[:,0] = predicted_int[:,0]
            predicted[:,21] = predicted_int[:,21]
        observed = Y
        score = scoring.score2(predicted,observed)
        r_int = scoring.r2('int','mean',predicted,observed)
        r_ple = scoring.r2('ple','mean',predicted,observed)
        r_dec = scoring.r2('dec','mean',predicted,observed)
        r_int_sig = scoring.r2('int','sigma',predicted,observed)
        r_ple_sig = scoring.r2('ple','sigma',predicted,observed)
        r_dec_sig = scoring.r2('dec','sigma',predicted,observed)
        print("For subchallenge 2, %s phase, score = %.2f (%.2f,%.2f,%.2f,%.2f,%.2f,%.2f)" \
                % (phase,score,r_int,r_ple,r_dec,r_int_sig,r_ple_sig,r_dec_sig))
        scores[phase] = (score,r_int,r_ple,r_dec,r_int_sig,r_ple_sig,r_dec_sig)

    return rfc,scores['train'],scores['test']

def scan(X_train,Y_train,X_test_int,X_test_other,Y_test,max_features=None,n_estimators=100):
    rfcs_max_features = {}
    ns = np.logspace(1,3.48,15)
    scores_train = []
    scores_test = []
    for n in ns:
        rfc_max_features,score_train,score_test = rfc_(X_train,Y_train['mean_std'],
                                          X_test_int,X_test_other,
                                          Y_test['mean_std'],
                                          max_features=int(n),n_estimators=100)
        scores_train.append(score_train)
        scores_test.append(score_test)
        rfcs_max_features[n] = rfc_max_features
    rs = ['int_m','ple_m','dec_m','int_s','ple_s','dec_s']
    for i,ri in enumerate(rs):
        print(ri)
        print('maxf ',ns.round(2))
        print('train',np.array(scores_train)[:,i].round(3))
        print('test ',np.array(scores_test)[:,i].round(3))
   
    return rfc_max_features,scores_train,scores_test
    #for n,train,test in zip(ns,scores_train,scores_test):
    #    print("max_features = %d, train = %.2f, test = %.2f" % (int(n),train,test))
    #return rfcs_max_features
