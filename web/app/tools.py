import plotly
import plotly.express as px
import pandas as pd
import json

Config = dict( REDIS_KWARGS = {'host': 'redis', 'port': 6379, 'db': 0})

def read_labels_db(db):
       labels = [lbl for lbl in db.smembers('labels') if lbl != ''] 
       return labels

def read_db(db):
       labels = read_labels_db(db) 
       info = {lbl: db.hgetall(lbl) for lbl in labels if db.hgetall(lbl)}
       return labels, info


def create_map(labels, info):
    if not labels:
           r = [1, 1]
           theta = ['Нет', 'информации']
    else:
           theta = labels
           r = [1]*len(labels)
           for i in range(len(labels)):
                  if theta[i] in info:
                         for _ in info[theta[i]]:
                            r[i] += 1

    df = pd.DataFrame(dict(r=r, theta=theta))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON