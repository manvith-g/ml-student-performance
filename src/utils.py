import os,sys,dill
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import r2_score


def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    


def evaluate_models(X_train,y_train,X_test,y_test,models,params): # with params(hyperparameter tuning)
    try:
        logging.info("Evaluation started")
        report={}

        for i in range(len(list(models))):
            logging.info(f"{list(models.keys())[i]} Started")
            model=list(models.values())[i]                        # model is a refernce of AnyModel() insted of doinf like randomforest.fit() we are doing model.fit but insdie memoty it is saving in same place before it was not trained but after trained
            param=params[list(models.keys())[i]]


            grid=GridSearchCV(model,param,cv=5,n_jobs=-1) #other parameter u can give :    n_jobs=  ,  verbose=  ,  refit=   , etc 
            grid.fit(X_train,y_train)

            model.set_params(**grid.best_params_)
            model.fit(X_train,y_train)

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_model_score=r2_score(y_train,y_train_pred) # do something with this tooooooooo later
            test_model_score=r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]]= test_model_score
            logging.info(f"{list(models.keys())[i]} Ended | R2_SCORE : {test_model_score}")

        logging.info(f"Evaluation Ended | Model Trained succefully ")
        return report

    except Exception as e:
        raise CustomException(e,sys)




# def evaluate_models(X_train,y_train,X_test,y_test,models): # without params
#     try:
#         logging.info("Evaluation started")
#         report={}

#         for i in range(len(list(models))):
#             logging.info(f"{list(models.keys())[i]} Started")
#             model=list(models.values())[i] # model is a refernce of AnyModel() insted of doinf like randomforest.fit() we are doing model.fit but insdie memoty it is saving in same place before it was not trained but after trained

#             model.fit(X_train,y_train)

#             y_train_pred=model.predict(X_train)
#             y_test_pred=model.predict(X_test)

#             train_model_score=r2_score(y_train,y_train_pred) # do something with this tooooooooo later
#             test_model_score=r2_score(y_test,y_test_pred)

#             report[list(models.keys())[i]]= test_model_score
#             logging.info(f"{list(models.keys())[i]} Ended | R2_SCORE : {test_model_score}")

#         logging.info(f"Evaluation Ended | Model Trained succefully ")
#         return report

#     except Exception as e:
#         raise CustomException(e,sys)
    