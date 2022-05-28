import json
import sys
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import datetime

fname = 'data/' + datetime.date.today().strftime('%b-%d-%Y') + '.json'
# fname = 'data/May-27-2022.json'
with open(fname, 'r') as infile:
    fields = json.load(infile)
    fields_df = pd.DataFrame.from_dict(fields)
    fields_df = fields_df.rename_axis("subfield").reset_index()

def matplotlib_pie(field):
    comp_sci = fields[field]
    labels, values = list(comp_sci.keys()), list(comp_sci.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def plotly_pie(field):
    fig = px.pie(fields_df, values=field, names='subfield', title=f'{field} recent paper submissions')
    fig.show()

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Too few arguments'
    assert len(sys.argv) < 4, 'Too many arguments'
    assert sys.argv[1] in ['plotly', 'matplotlib'], 'module must be either plotly or matplotlib'
    module = sys.argv[1]
    field = sys.argv[2]
    
    if module == 'plotly':
        print('running plotly visualizations...')
        plotly_pie(field)
    elif module == 'matplotlib':
        print('running matplotlib visualizations...')
        matplotlib_pie(field)
