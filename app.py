from turtle import color

from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
import calendar

app = Dash(__name__)

app.layout = html.Div('I am alive!!')

df = pd.read_csv('us_counties_processed.csv')
df = df[["state","county","year","month","mean_temp_1"]]
states = df.state.unique()

df = df.groupby(["state","month"], as_index=False).agg({"mean_temp_1":"mean"})

app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='state-widget',
        multi=True,
        value=['Alabama','Arizona'],  # REQUIRED to show the plot on the first page load
        options=[
            {'label': state, 'value': state} for state in states])])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('state-widget', 'value'))
def plot_altair(states):
    for state in states:
        df_filtered = df[df['state'].isin(states)]
    chart = alt.Chart(df_filtered).mark_line().encode(
        color = alt.Color('state',
            legend=alt.Legend(
            title='States')
        ),
        x=alt.X('month', title="Month"),
        y=alt.Y('mean_temp_1', title="Mean Temperature (F°)")).properties(
            title="USA: Mean Monthly Temperature by State")
    return chart.to_html()

# dropdown select state
# dropdown select county
# plot months bottom mean teps left

if __name__ == '__main__':
    app.run_server(debug=True)