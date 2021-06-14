import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc
import plotly.graph_objects as go  
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_extensions.snippets import send_data_frame
import dash_table
import numpy as np


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
def load_data():
    dataset_name='complaints.csv'
    global df
    df=pd.read_csv(dataset_name)
    
    #df['Date And Time'] = pd.to_datetime(df['Date And Time'])
    #df['day'] = df['Date And Time'].dt.day
    #df['month'] = df['Date And Time'].dt.month
    #df['year']=df['Date And Time'].dt.year
    
    print(df.sample(5))
    global area_list
    area_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['Area'].unique().tolist() ) ]
    global department_list
    department_list=[{"label": str(i), "value": str(i)}  for i in sorted( df['Department'].unique().tolist() ) ]
    #print(complaint_no_list)
    global Department_data
    global array1
    global index1
    global figure
    global date_list
    global fd
    global figure1
    date_list = [{"label":x, "value":x} for x in range(1, 32)]
    global month_list
    month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
    month_list= [{"label":key, "value":values} for key,values in month.items()]
    global year_list
    year_list=[{"label":str(i), "value":i} for i in df['year'].unique().tolist()]
def open_browser():
    webbrowser.open_new( 'http://127.0.0.1:8050/')

def create_api_ui():
    main_layout=html.Div([
        html.H1(id='main_title',children='RMC ANALYSIS DASHBOARD',style={'textAlign': 'center','background-color':'#353C48','color':'white','font-size':'50px','font-weight':'bold'}),
        html.Hr(),
       dcc.Tabs(id="tabs-styled-with-props",style={'color':'white','font-weight':'bold','font-size':'15px'}, value='tab-1', children=[
        dcc.Tab(label='Department and Complaint Analysis',style={'background-color':'#353C48'}, value='tab-1',children=[html.Div(),
        dcc.Dropdown(
        id='area-dropdown', 
        options=area_list,
        placeholder='Select Area',
        multi=False,
  ),html.Br(),
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
    
)  ]),
        


        dcc.Tab(label='Area vs Area Analysis',style={'background-color':'#353C48'}, value='tab-2',children=[html.Div(),
        html.Br(),
dbc.Row(
    [
        dbc.Col(html.Div(dcc.Dropdown(
        id='area-dropdown1', 
        options=area_list,
        placeholder='Select Area',
        multi=False,
  )),md=6),
        dbc.Col(html.Div(dcc.Dropdown(
        id='area-dropdown2', 
        options=area_list,
        placeholder='Select Area',
        multi=False,
  )),md=6),
    ],
    no_gutters=True,
),
html.Br(),

dbc.Row(
            dbc.Col(
                html.Div(html.Button('Submit', id='btn-nclicks-1', n_clicks=0,style={
            'background-color': '#353C48',
            'color':'white',
            'align':'center',
            'border-radius': '8px',
            'font-weight': 'bold',
        })),
                width={"size": 3, "offset": 5},
            )
        )


        
        ,])
        
        ,


    dcc.Tab(label='Date Analysis',style={'background-color':'#353C48'}, value='tab-3',children=[html.Div(),
        dcc.Dropdown(
        id='date-dropdown', 
        options=date_list,
        placeholder='Select Date',
        multi=False,
  ),
  
  html.Br(),
 dcc.Dropdown(
        id='month-dropdown', 
        options=month_list,
        placeholder='Select Month',
        multi=False,
  ),
  html.Br(),
  dcc.Dropdown(
        id='year-dropdown', 
        options=year_list,
        placeholder='Select Year',
        multi=False,
  ),
  html.Br(),
  dcc.Input(id="search", placeholder="Search By Complaint Number",style={'height': '30px',
    'display':'flex',
    'flexWrap':'wrap',
	'width': '100%',
	'text-align': 'center',
	
	'position': 'relative',
    'margin-left': 'auto',
    'margin-right': 'auto',}),
    html.Br(),
    html.Br(),
  dash_table.DataTable(
        id='datatable-interactivity',
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    style_cell={
        'backgroundColor': 'rgb(150, 150, 150)',
        'color': 'white'
    },
        data=[],
        columns=[
            {"name": i, "id": i, "selectable": True} for i in df.columns[1:7]
        ],
        editable=True,
        filter_action="native",
        
        sort_action="native",
        sort_mode="single",
        #column_selectable="multi",
        #row_selectable='multi',
        
        #row_deletable=True,
        selected_columns=[],
        selected_rows=[],
       

    ),
  ]),
  dcc.Tab(label='Whole city problem analysis by date',style={'background-color':'#353C48'}, value='tab-4',children=[html.Div(),
   dcc.Dropdown(
        id='date-dropdown1', 
        options=date_list,
        placeholder='Select Date',
        multi=False,
  ),
  
  html.Br(),
 dcc.Dropdown(
        id='month-dropdown1', 
        options=month_list,
        placeholder='Select Month',
        multi=False,
  ),
  html.Br(),
  dcc.Dropdown(
        id='year-dropdown1', 
        options=year_list,
        placeholder='Select Year',
        multi=False,
  ),
  html.Br(),
  dcc.Graph(id='graph-object1'),
  ]),
  dcc.Tab(label='Solved Duration',style={'background-color':'#353C48'}, value='tab-5',children=[html.Div(),
  dcc.Graph(id='graph-object2')
  ])
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
        html.Br(),
    
        html.Hr(),
        
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
    dash.dependencies.Input('area-dropdown1','value'),
    dash.dependencies.Input('area-dropdown2','value'),
    dash.dependencies.Input('tabs-styled-with-props','value'),
    dash.dependencies.Input('btn-nclicks-1','n_clicks'),

    ]
    )
def update_api_ui(area_value,department_value,radio_value,area_value1,area_value2,tab_value,n_clicks):
    print(area_value)
    print(type(area_value))
    if tab_value=='tab-1':
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
    else:
        df1=df[df['Area']==area_value1]
        array1=df1['Department'].value_counts()
        index1=array1.index.tolist()
        print(array1)
        Department_data = array1.tolist()
        print(Department_data)
        df2=df[df['Area']==area_value2]
        array2=df2['Department'].value_counts()
        index2=array2.index.tolist()
        print(array2)
        Department_data1 = array2.tolist()
        print(Department_data1)
        figure = go.Figure(
        data=[go.Bar(
        x=index1,
        y=Department_data,
        name=area_value1,
        marker_color='indianred'
        ),
        go.Bar(
        x=index2,
        y=Department_data1,
        name=area_value2,
        marker_color='lightsalmon'
        )])
        figure.update_layout(barmode='group', xaxis_tickangle=90)
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if area_value1 and area_value2 is not None:
            if 'btn-nclicks-1' in changed_id:
                figure.show()
                
        return figure

@app.callback(
    dash.dependencies.Output('datatable-interactivity', 'data'),
    [
    dash.dependencies.Input('tabs-styled-with-props', 'value'),   
    dash.dependencies.Input('date-dropdown', 'value'),  
    dash.dependencies.Input('month-dropdown', 'value'),  
    dash.dependencies.Input('year-dropdown', 'value'),             
    dash.dependencies.Input('search', 'value'),             
     ]) 
def update_table(tab_value,date_value,month_value,year_value,search_value):
    global df
    if tab_value=='tab-3':
        if date_value is not None and month_value is None and year_value is None:
            fd=df[df['day']==date_value]
            if search_value is not None:
                #print(search_value)
                fd=fd[fd['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=fd.to_dict('records')
            
        elif date_value is not None and month_value is not None and year_value is None:
            fd=df[df['day']==date_value]
            fd=fd[fd['month']==month_value]
            if search_value is not None:
                #print(search_value)
                fd=fd[fd['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=fd.to_dict('records')
            
        elif date_value is None and month_value is not None and year_value is None:
            fd=df[df['month']==month_value]
            if search_value is not None:
                #print(search_value)
                fd=fd[fd['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=fd.to_dict('records')
            
        #elif date_value is None and month_value is None and year_value is None:
            
         #   data=df.to_dict('records')
        elif date_value is None and month_value is None and year_value is not None:
            if search_value is not None:
                #print(search_value)
                fd=df[df['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=df.to_dict('records')
        elif date_value is None and month_value is not None and year_value is not None:
            fd=df[df['month']==month_value]
            fd=fd[fd['year']==year_value]
            if search_value is not None:
                #print(search_value)
                fd=fd[fd['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=fd.to_dict('records')
            
        elif date_value is not None and month_value is not None and year_value is  not  None:
            fd=df[df['day']==date_value]
            fd=fd[fd['month']==month_value]
            fd=fd[fd['year']==year_value]
            if search_value is not None:
                #print(search_value)
                fd=fd[fd['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=fd.to_dict('records')
            
        elif date_value is not None and month_value is None and year_value is not None:
            fd=df[df['day']==date_value]
            fd=fd[fd['year']==year_value]
            if search_value is not None:
                #print(search_value)
                fd=fd[fd['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=fd.to_dict('records')
            
        else:
            
            if search_value is not None:
                #print(search_value)
                fd=df[df['Complaint No.'].astype(str).str.contains(search_value, case = False)]
                data=fd.to_dict('records')
            else:
                data=df.to_dict('records')
        return data

@app.callback(
    dash.dependencies.Output('graph-object1', 'figure'),
    [
    dash.dependencies.Input('date-dropdown1', 'value'),  
    dash.dependencies.Input('month-dropdown1', 'value'),  
    dash.dependencies.Input('year-dropdown1', 'value'),
    dash.dependencies.Input('tabs-styled-with-props', 'value'),
    ])
def update_ui(date_value,month_value,year_value,tab_value):
    global fig
    fig=go.Figure()
    if tab_value=='tab-4':
        print(tab_value)
        if date_value is not None and month_value is not None and year_value is not None:
            fd=df[df['day']==date_value]
            fd=fd[fd['month']==month_value]
            fd=fd[fd['year']==year_value]
            array1=fd['Department'].value_counts()
            index1=array1.index.tolist()
            Department_data = [( str(i),array1[i]) for i in index1]
            print(Department_data)
            fig=px.bar(pd.DataFrame(Department_data,columns=['Department','Total_problems']),x='Department',y='Total_problems',text='Total_problems',height=700,title='Whole City Analysis')
    return fig
    
@app.callback(
    dash.dependencies.Output('graph-object2', 'figure'),
    [
    dash.dependencies.Input('tabs-styled-with-props', 'value'),
    ])
def update_ui(tab_value):
    fig=go.Figure()
    if tab_value=='tab-5':
        department_list=df['Department'].unique().tolist()
        time_stamp1=[]
        for i in department_list:
            time_stamp1.append(int(df[df['Department']==i]['Duration day'].mean()))
        print(time_stamp1)
        #Department_data = [( department_list(i),time_stamp1[i]) for i in len(department_list)]
        fig = go.Figure([go.Bar(x=department_list, y=time_stamp1,text=time_stamp1,textposition='auto',)],layout=go.Layout(
        title="Whole city analysis",
        height=700
        ))
        
        #fig.show()
    return fig
    
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