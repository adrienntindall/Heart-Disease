import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

import pickle as pkl
import pandas as pd

fname = 'hd_model.pkl'
with open(fname, 'rb') as InFile:
    model = pkl.load(InFile)

fname = 'icdcodes.pkl'
with open(fname, 'rb') as InFile:
    codes = pkl.load(InFile)

fname = 'colnames.pkl'
with open(fname, 'rb') as InFile:
    cols = pkl.load(InFile)
    
app = dash.Dash()

app.layout = html.Div([
    html.Div(
        children='Heart Disease Risk Calculator',
        className='banner',
        style={'padding': '10px', 'color': '#d63333', 'font-size': '24px', 'text-align': 'center'}
    ),
    html.Label('Sex'),
    dcc.Dropdown(
     id='sex-id',
     options=[
      {'label': 'Male', 'value': 'gender_M'},
      {'label': 'Female', 'value': 'gender_F'}
     ]
    ),
    html.Label('Martial Status'),
    dcc.Dropdown(
        id='marital-id',
        options=[
            {'label': 'Single', 'value': 'marital_status_SINGLE'},
            {'label': 'Married', 'value': 'marital_status_MARRIED'},
            {'label': 'Life Partner', 'value': 'marital_status_LIFE PARTNER'},
            {'label': 'Widowed', 'value': 'marital_status_WIDOWED'},
            {'label': 'Separated', 'value': 'marital_status_SEPARATED'},
            {'label': 'Divorced', 'value': 'martial_status_DIVORCED'}
        ]
    ),
  html.Label('Religion'), 
   dcc.Dropdown(
       id='religion-id',
       options=[
           {'label': 'Catholic', 'value': 'religion_CATHOLIC'},
           {'label': 'Basptist', 'value': 'religion_BAPTIST'},
           {'label': 'Jewish', 'value': 'religion_JEWISH'},
           {'label': 'Muslim', 'value': 'religion_MUSLIM'},
           {'label': 'Buddhist', 'value': 'religion_BUDDHIST'},
           {'label': 'Hindu', 'value': 'religion_HINDU'},
           {'label': 'Unaffliated', 'value': 'religion_NOT SPECIFIED'},
           {'label': 'Protestant Quaker', 'value': 'religion_PROTESTANT QUAKER'},
           {'label': 'Jehovah\'s Witness', 'value': 'religion_JEHOVAH\'S WITNESS'},
           {'label': 'Greek Orthodox', 'value': 'religion_GREEK ORTHODOX'},
           {'label': 'Episcopalian', 'value': 'religion_EPISCOPALIAN'},
           {'label': 'Christain Scientist', 'value': 'religion_CHRISTIAN SCIENTIST'},
           {'label': '7th Day Adventist', 'value': 'religion_7TH DAY ADVENTIST'},
           {'label': 'Methodist', 'value': 'religion_METHODIST'},
           {'label': 'Unitarian-Universalist', 'value': 'religion_UNITARIAN-UNIVERSALIST'},
           {'label': 'Roman East Orthidox', 'value': 'religion_ROMANIAN EAST. ORTH'},
           {'label': 'Lutheran', 'value': 'religion_LUTHERAN'},
           {'label': 'Other', 'value': 'religion_OTHER'}
       ]
   ),
  html.Label('Ethnicity'),
    dcc.Dropdown(
        id='ethnic-id',
        options = [
            {'label': 'White/Caucasian', 'value': 'ethnicity_WHITE'},
            {'label': 'Black/Arican American', 'value': 'ethnicity_BLACK/AFRICAN AMERICAN'},
            {'label': 'Hispanic/Latino', 'value': 'ethnicity_HISPANIC OR LATINO'},
            {'label': 'Asian', 'value': 'ethnicity_ASIAN'},
            {'label': 'Middle Eastern', 'value': 'ethnicity_MIDDLE EASTERN'},
            {'label': 'Native American/Alaskan', 'value': 'ethnicity_AMERICAN INDIAN/ALASKA NATIVE FEDERALLY RECOGNIZED TRIBE'},
            {'label': 'Native Hawaiian/Pacific Islander', 'value': 'ethnicity_NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER'},
            {'label': 'Multiracial', 'value': 'ethnicity_MULTI RACE ETHNICITY'},
            {'label': 'Other', 'value': 'ethnicity_OTHER'}
        ]
   ),
   html.Label('icd9 Diagnostic Codes '), html.A('[Code Lookup]', href='http://www.icd9data.com/2015/Volume1/default.htm'),
    dcc.Dropdown(
        id='icd9-id',
        options = [
         {'label': x, 'value': 'icd9_'+x} for x in codes   
        ],
        multi=True
    ),
   
    html.Label('Age: '),
    dcc.Input(id='age-id', value='0', type='number'),
    html.Br(),
    
    html.Label('Time spent in the ICU (days) (est.): '),
    dcc.Input(id='los-id', value='0', type='number'),
    html.Br(),
    
    html.Label('ICU Visits (total): '),
    dcc.Input(id='visits-id', value='0', type='number'),
    html.Br(),
    
    html.Button(id='submit-button', children='Submit'),
    
    html.Div(id='output-a', 
             style = {
                 'font-size' : '36px',
                 'text-align' : 'center'
             }
            )
],
    style={'width': '40%',
          'margin-left': 'auto',
          'margin-right' : 'auto',
          'line-height' : '30px'}
)

@app.callback(
   Output('output-a', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('sex-id', 'value'),
     State('marital-id', 'value'),
     State('religion-id', 'value'),
     State('ethnic-id', 'value'),
     State('icd9-id', 'value'),
     State('age-id', 'value'),
     State('los-id', 'value'),
     State('visits-id', 'value')]
)
def predict_heart_disease_risk(n_clicks, sex, mar, relg, eth, icd, age, los, vis):
    imp = pd.DataFrame(columns=cols)
    imp.loc[1] = 0
    imp[sex].loc[1] = 1
    imp[mar].loc[1] = 1
    imp[relg].loc[1] = 1
    imp[eth].loc[1] = 1
    if icd is not None:
        for i in icd:
            imp[i].loc[1] = 1
    imp['age'].loc[1] = age
    imp['los'].loc[1] = los
    imp['total_stays'].loc[1] = vis
    X = imp
    probs = model.predict_proba(X)[0][1]*100
    return '{}% risk of heart disease'.format(round(probs, 2))

if __name__ == '__main__':
    app.run_server(debug=True)