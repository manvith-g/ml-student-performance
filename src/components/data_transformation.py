import sys,os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.utils import save_object

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfug:
    preprocessor_obj_filr_path=os.path.join('artifacts','preprocessor.pkl')


class DataTranformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfug()

    def get_data_tranformer_object(self):
        '''
        we did data transformation here
        '''
        try:
            numerical_columns=['writing_score','reading_score'] #math_core is output so not taken
            categorical_columns=[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]
            num_pipeline=Pipeline( #Creating pipeleine
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scalar",StandardScaler())
                ]
            )

            cat_pipline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False)) #why i am not understanding this line
                ]
            )

            logging.info('Pipline Created Succefully')
            logging.info('Pipelining Started ')


            preprocessor=ColumnTransformer( # combaining pipeline
                [
                    ('num_pipline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipline,categorical_columns)
                ]
            )
            logging.info('Pipelining Ended')
            logging.info("Numerical standard scaling is completed")
            logging.info("Categorical clumns encoding completed")

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_tranformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path) #train data
            test_df=pd.read_csv(test_path) #test data
            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object") 
            preprocessor_obj=self.get_data_tranformer_object()

            target_column_name='math_score'

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)

            #now we are getting data affter transformation we are combining output feature too casue we all need in one table but now its transformed data lator on you can slpit it again into traina nd test while training the model now our work is to just transform
            train_arr=np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr=np.c_[ 
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Saved preprocessor object")

            save_object( ##code of this objcet in the utils
                file_path=self.data_transformation_config.preprocessor_obj_filr_path,
                obj=preprocessor_obj
            )
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_filr_path
            )
        except Exception as e:
            raise CustomException(e,sys)
