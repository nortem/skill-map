import plotly
import plotly.express as px
import pandas as pd
import json


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