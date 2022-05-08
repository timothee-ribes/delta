import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


class Radar_Accidents():
    def __init__(self, application=None):
        self.df_radars = pd.read_pickle("data/lptr_radars.pkl")

        self.main_layout = html.Div(children=[
            html.H4('Interactive scatter plot with radars dataset'),
            dcc.Graph(id="scatter-mapbox"),
            html.P("Filter by year:"),
            dcc.Slider(2003, 2018, 1,
                    value=2003,
                    id="range-slider",
                    marks={x:str(x) for x in range(2003,2019)}
                    )])

        if application:
            self.app = application
        else:
            self.app = Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            Output("scatter-mapbox", "figure"),
            Input("range-slider", "value")) (self.update_bar_chart)

    # fonction à appliquer lorsque le callback arrive.
    def update_bar_chart(self, slider_range):
        # le masque pour afficher seulement les radars installés à l'année indiquée par le slider
        # (y compris les années d'avant)
        mask = self.df_radars['date_installation'] <= slider_range

        # la fonction d'affichage du graphique avec ses paramètres.
        fig = px.scatter_mapbox(self.df_radars[mask],
                                lat="latitude", lon="longitude",
                                hover_name="emplacement", color_discrete_sequence=["blue"],
                                zoom=5, height=850, width=850)

        # fonction pour afficher la map.
        fig.update_layout(mapbox_style="open-street-map")
        return fig


if __name__ == '__main__':
    rd_acc = Radar_Accidents()
    rd_acc.app.run_server(debug=True, port=8051)
