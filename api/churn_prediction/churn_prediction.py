import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime

class churn_prediction():
    def __init__(self):
        self.home_path = '/Users/luishmq/Documents/repos/churn_prediction/churn_clients_predict/'
        self.credit_score                = pickle.load(open(self.path + 'src/features/credit_score.pkl'))
        self.balance                     = pickle.load(open(self.path + 'src/features/balance.pkl'))
        self.estimated_salary            = pickle.load(open(self.path + 'src/features/estimated_salary.pkl'))
        self.estimated_monthly_salary    = pickle.load(open(self.path + 'src/features/estimated_monthly_salary.pkl'))
        self.tenure                      = pickle.load(open(self.path + 'src/features/tenure.pkl'))
        self.age                         = pickle.load(open(self.path + 'src/features/age.pkl'))             
    
    def data_cleaning(self, df1):
        
        # Rename Columns
        old_cols = ['RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography',
       'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
       'IsActiveMember', 'EstimatedSalary', 'Exited']

        snake_case = lambda x: inflection.underscore(x)

        new_cols = list( map(snake_case, old_cols))
        df1.columns = new_cols

        return df1

    def feature_engineering(self, df2):

        # Feature Engineering 
        # High Age Feature - Tendem a realizar o churn mais facilmente
        df2['high_age'] = df2['age'].apply(lambda x: 1 if x > 48 else 0)

        # Medium Balance Feature - Tendem a realizar o churn mais facilmente
        df2['medium_balance'] = df2['balance'].apply(lambda x: 1 if 100000.00 < x < 150000.00 else 0)

        # Null Balance Feature - Tendem a não realizar o churn de forma significativa
        df2['null_balance'] = df2['balance'].apply(lambda x: 1 if x == 0 else 0)

        # Number of Products Feature
        df2['low_products'] = df2['num_of_products'].apply(lambda x: 1 if x == 1 or x == 2 else 0)
        df2['high_products'] = df2['num_of_products'].apply(lambda x: 1 if x == 3 or x == 4 else 0)

        # Estimated Monthly Salary Feature
        df2['estimated_monthly_salary'] = df2['estimated_salary'].apply(lambda x: x / 12)
        
        # Filtragem de colunas
        cols_drop = ['row_number', 'customer_id', 'surname']
        df3 = df3.drop(cols_drop, axis=1)
        
        return df2
    
    
    def data_preparation(self, df5):

        # Rescaling
        # credit_score
        df5['credit_score'] = self.credit_score.fit_transform( df5[['credit_score']].values )

        # balance
        df5['balance'] = self.balance.fit_transform(df5[['balance']].values )

        # estimated_salary
        df5['estimated_salary'] = self.estimated_salary.fit_transform( df5[['estimated_salary']].values )

        # estimated_monthly_salary
        df5['estimated_monthly_salary'] = self.estimated_monthly_salary.fit_transform( df5[['estimated_monthly_salary']].values )

        # tenure
        df5['tenure'] = self.tenure.fit_transform( df5[['tenure']].values )

        # age
        df5['age'] = self.age.fit_transform( df5[['age']].values )

        # Encoding
        # gender - Label Encoding
        df5['gender'] = self.gender.fit_transform( df5['gender'] )

        # geography - Ordinal Encoding
        geography_dict = {'France': 1, 'Spain': 2, 'Germany': 3}
        df5['geography'] = df5['geography'].map( geography_dict )
        
        return df5

    def get_predict(self, model, original_data, test_data):
        
        # model prediction
        pred = model.predict(test_data)
        
        # join prediction into original data
        original_data['prediction'] = pred
        
        return original_data.to_json(orient='records', date_format='iso')
        