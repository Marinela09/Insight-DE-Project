import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import psycopg2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

''' establish a connect to the  database'''
file = open("credentials.txt", "r")
f = file.readlines()
l = [line.strip() for line in f]

conn = psycopg2.connect(dbname =l[0], user = l[1], host = l[2], password = l[3])
cur = conn.cursor()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#FEF8FE',
    'text': '#000000',
    'pagebackground': '#EFFBE9',
    'marker':'#53682A'
}


'''application layout'''
app.layout = html.Div(style={'color': colors['text'], 'backgroundColor': colors['pagebackground']}, children=[

   html.H1(children='Common Crawl Database Trends'),
   html.H2(children='Database Ranking by Month'),
   html.Label('Select a month:'),
   dcc.Dropdown(
        id='month-dropdown',
        options=[
            {'label': 'January', 'value': 'january'},
            {'label': 'February', 'value': 'february'},
            {'label': 'March', 'value': 'march'},
	        {'label': 'April', 'value': 'april'},
	        {'label': 'May', 'value': 'may'},
            {'label': 'June', 'value': 'june'},
	        {'label': 'July', 'value': 'july'},
            {'label': 'August', 'value': 'august'},
            {'label': 'September', 'value': 'september'},
            {'label': 'October', 'value': 'october'},
            {'label': 'November', 'value': 'november'},
	        {'label': 'December', 'value': 'december'}
        ],
        value=' '
    ),
    html.Div(id='output-month'),
   
    html.H2(children='Database Trends in 2018'),
    html.Label('Select a database:'),
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'Hazelcast', 'value': 'Hazelcast'},
            {'label': 'Riak', 'value': 'Riak'},
            {'label': 'HBase', 'value': 'HBase'},
            {'label': 'Memcached', 'value': 'Memcached'},
            {'label': 'PosrgreSQL', 'value': 'PostgreSQL'},
            {'label': 'JanusGraph', 'value': 'JanusGraph'},
            {'label': 'OrientDB', 'value': 'OrientDB'},
            {'label': 'Oracle Database', 'value': 'Oracle Database'},
            {'label': 'Amazon Redshift', 'value': 'Amazon Redshift'},
            {'label': 'Redis', 'value': 'Redis'},
            {'label': 'Couchbase', 'value': 'Couchbase'},
            {'label': 'DynamoDB', 'value': 'DynamoDB'},
            {'label': 'Neo4j', 'value': 'Neo4j'},
            {'label': 'MongoDB', 'value': 'MongoDB'},
            {'label': 'ArangoDB', 'value': 'ArangoDB'},
            {'label': 'Apache Druid', 'value': 'Apache Druid'},
            {'label': 'InfluxDB', 'value': 'InfluxDB'},
            {'label': 'MySQL', 'value': 'MySQL'},
            {'label': 'Apache Solr', 'value': 'Apache Solr'},
            {'label': 'Apache Cassandra', 'value': 'Apache Cassandra'},
        ],
        value=' '
    ),


    html.Div(id ='output-category')
])

 
@app.callback(
    dash.dependencies.Output('output-month', 'children'),
    [dash.dependencies.Input('month-dropdown', 'value')])

def update_monthly_output(value):
  if value != ' ':
     data = select_monthly_data(value)
     return  html.Div(children = [
        dcc.Graph(
           id='frequency-graph',
           figure={
              'data':[{'x':data[0], 'y': data[1], 'type': "bar", 'marker': {'color': colors['marker']}}],
              'layout':{'title':'Database Popularity per Month', 'plot_bgcolor': colors['background'], 'paper_bgcolor': colors['pagebackground']},
	       }
        )
     ])


@app.callback(
    dash.dependencies.Output('output-category', 'children'),
    [dash.dependencies.Input('category-dropdown', 'value')])

def update_cat_output(value):
  if value != ' ':
     data = select_cat_data(value)
     return  html.Div(children = [
        dcc.Graph(
           id='historical-graph',
           figure={
	          'data':[{'x': data[0], 'y': data[1], 'type': 'line', 'marker': {'color': colors['marker']}}],
	          'layout': {'title' : 'Database Popularity Over Time', 'plot_bgcolor': colors['background'], 'paper_bgcolor': colors['pagebackground']}
	       }
        )
     ])






'''  get freq data per month from the database '''
def select_monthly_data(mon):
  table = "results" + mon
  q1 = "Select name from " + table
  q2 = "Select frequency from " + table
  cur.execute(q1)
  databases = cur.fetchall()
  xData = [database[0] for database in databases]
  cur.execute(q2)
  frequencies = cur.fetchall()
  yData = [freq[0] for freq in frequencies]
  return [xData, yData]



''' get historcal freq data per category from the database '''
def select_cat_data(cat):
  months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 
            'august', 'september', 'october', 'november', 'december']
  yData = []

  for mon in months:
     table =  "results" +  mon
     q = "Select frequency from " + table + " where name =" + "\'" + cat + "\';"
     cur.execute(q)
     freq = cur.fetchall()
     if freq:
     	yData.append(freq[0][0])
     else:
        yData.append(0)

  return [months, yData]


if __name__ == '__main__':
    app.run_server(debug=True, port=80, host='0.0.0.0')
