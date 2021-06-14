import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc
import plotly.graph_objects as go  
import plotly.express as px
import dash_bootstrap_components as dbc


app=dash.Dash()

def load_data():
    dataset_name='complaints.csv'
    global df
    df=pd.read_csv(dataset_name)
    print(df.sample(5))
    global area_list
    area_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['Area'].unique().tolist() ) ]
    global department_list
    department_list=[{"label": str(i), "value": str(i)}  for i in sorted( df['Department'].unique().tolist() ) ]
    global Department_data
    global array1
    global index1
    global figure
def open_browser():
    webbrowser.open_new( 'http://127.0.0.1:8050/')

def create_api_ui():
    main_layout=html.Div([
        html.H1(id='main_title',children='RMC ANALYSIS DASHBOARD',style={'textAlign': 'center','color':'Blue','font-size':'50px'}),
        html.Hr(),
        html.Button('Button 1', id='btn-nclicks-1', n_clicks=0,style={
            'background-color': '#2dbecd',
            'padding': '10px 24px',
            'border-radius': '8px',
            'font-weight': 'bold',
            'margin-left':'700px',
            'margin-right':'50px',
        }),
        html.Button('Button 2', id='btn-nclicks-2', n_clicks=0,style={
            'background-color': '#2dbecd',
            'padding': '10px 24px',
            'border-radius': '8px',
            'font-weight': 'bold',
            'margin-right':'50px',
        }),
        html.Br(),
    
        html.Hr(),
        dcc.Dropdown(
        id='area-dropdown', 
        options=area_list,
        placeholder='Select Area',
        multi=False,
  ),
        dcc.Dropdown(
        id='department-dropdown', 
        options=department_list,
        placeholder='Select Department',
        multi=False,
  ),
        dcc.Graph(id='graph-object'),
        dcc.RadioItems(id='radio-button',
    options=[
        {'label': 'Bar', 'value': 'Bar'},
        {'label': 'Pie', 'value': 'Pie'},
    ],
    value='Bar',
    labelStyle={'display': 'inline-block','margin-left':'500px'},
    
)  
    ]
    )
    return main_layout
@app.callback(
    Output('department-dropdown', 'options'),
    [Input('area-dropdown', 'value')])
def set_country_options(area_value):
  # Making the country Dropdown data
  if area_value==None:
      return department_list
  else:
        return[{"label": str(i), "value": str(i)}  for i in df[df['Area']==area_value] ['Department'].unique().tolist() ]

@app.callback(
    dash.dependencies.Output('graph-object', 'figure'),
    [
    dash.dependencies.Input('area-dropdown', 'value'),
    dash.dependencies.Input('department-dropdown', 'value'),
    dash.dependencies.Input('radio-button', 'value'),
    ]
    )
def update_api_ui(area_value,department_value,radio_value):
    print(area_value)
    print(type(area_value))
    if radio_value=='Bar':
        if area_value==None and department_value==None:
            array1=df['Department'].value_counts()
            index1=array1.index.tolist()
            Department_data = [( str(i),array1[i]) for i in index1]
            print(Department_data)
            figure=px.bar(pd.DataFrame(Department_data,columns=['Department','Total_problems']),x='Department',y='Total_problems',text='Total_problems',height=700,title='Whole City Analysis')
        elif area_value==None and department_value is not None:
            df1=df[df['Department']==department_value]
            array1=df1['Complaint'].value_counts()
            index1=array1.index.tolist()
            Department_data = [( str(i),array1[i]) for i in index1]
            print(Department_data)
            figure=px.bar(pd.DataFrame(Department_data,columns=['Department','Total_problems']),x='Department',y='Total_problems',text='Total_problems',height=700,title='Whole City Analysis')
        else:
            if department_value is not None:
                df1=df[df['Area']==area_value]
                df2=df1[df1['Department']==department_value]
                array1=df2['Complaint'].value_counts()
                index1=array1.index.tolist()
                print(array1)
                Complaint_data = [( str(i),array1[i]) for i in index1]
                print(Complaint_data)
                figure=px.bar(pd.DataFrame(Complaint_data,columns=['Complaint','Total_problems']),x='Complaint',y='Total_problems',text='Total_problems',height=700,title='Area And Department Wise Analysis')

            else:
                print(area_value)
                df1=df[df['Area']==area_value]
                array1=df1['Department'].value_counts()
                index1=array1.index.tolist()
                print(array1)
                Department_data = [( str(i),array1[i]) for i in index1]
                print(Department_data)
                figure=px.bar(pd.DataFrame(Department_data,columns=['Department','Total_problems']),x='Department',y='Total_problems',text='Total_problems',height=700,title='Area Wise Analysis')
    else:
        if area_value==None and department_value==None:
            print(radio_value)
            #array1=df['Department'].value_counts()
            #index1=array1.index.tolist()
            #Department_data = [( str(i),array1[i]) for i in index1]
            #print(Department_data)
            figure=px.pie(df['Department'],names='Department',title='Whole City Department Analysis')
            figure.update_layout( width=1500,height=1000)
        elif area_value==None and department_value is not None:
            df1=df[df['Department']==department_value]
            figure=px.pie(df1['Complaint'],names='Complaint',title='Whole City Complaint  Analysis')
            figure.update_layout( width=1500,height=1000)
        else:
            if department_value is not None:
                df1=df[df['Area']==area_value]
                df2=df1[df1['Department']==department_value]
                figure=px.pie(df2['Complaint'],names='Complaint',title='Area and Department wise Complaint  Analysis')
                figure.update_layout( width=1500,height=1000)
            else:
                df1=df[df['Area']==area_value]
                figure=px.pie(df1['Department'],names='Department',title='Area wise Department Analysis')
                figure.update_layout( width=1500,height=1000)

    return figure
def main():
    print("Welocme to the Project")
    load_data()
    open_browser()
    global app
    app.layout=create_api_ui()
    app.title='RMC DASHBOARD'
    app.run_server()
 

    print("Thanks for using my Project")
    app=None
    df=None

if __name__ == '__main__':
    main()