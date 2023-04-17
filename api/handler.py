import pickle
import os
import pandas as pd
from flask                    import Flask, request, Response
from churn_prediction         import churn_prediction

# loading model
model = pickle.load( open( '/Users/luishmq/Documents/repos/churn_prediction/churn_clients_predict/models/model_churn.pkl', 'rb') )

# initialize API
app = Flask( __name__ )

@app.route( '/churn_prediction/predict', methods=['POST'] )
def churn_prediction():
    test_json = request.get_json()
   
    if test_json: # there is data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        # Instantiate churn prediction class
        pipeline = churn_prediction()
        
        # data cleaning
        df1 = pipeline.data_cleaning( test_raw )
        
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # prediction
        df_response = pipeline.get_predict( model, test_raw, df3 )
        
        return df_response
        
        
    else:
        return Reponse( '{}', status=200, mimetype='application/json' )

if __name__ == '__main__':
    app.run( '0.0.0.0' )