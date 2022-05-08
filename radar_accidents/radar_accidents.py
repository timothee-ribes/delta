import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


class Radar_Accidents():
    def __init__(self, application=None):
        df_radars = pd.read_csv("radar_accidents/radars.csv")

        # on garde seulement les colonnes intéressantes et on change le format de la date pour avoir juste l'année.
        # on met ça dans un nouveau dataframe.
        self.radars_year = df_radars[["date_installation", "emplacement", "latitude", "longitude", "id"]].copy()
        self.radars_year["date_installation"] = pd.DatetimeIndex(self.radars_year['date_installation']).year

        # des paramètres graphiques qui font du html visiblement.
        self.main_layout = html.Div(children=[
            html.H4('Interactive scatter plot with radars dataset'),  # ça c'est le titre du graphique.
            dcc.Graph(id="scatter-mapbox"),  # ça c'est l'identifiant du graphique.
            html.P("Filter by year:"),  # ça c'est le titre de la barre graduée, du slider pour changer l'année.
            dcc.Slider(2003, 2018, 1,  # borne gauche, borne droite, le pas.
                    value=2003,  # valeur au début.
                    id="range-slider",  # ça c'est l'identifiant du slider.
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
        # le dataset qui nous intéresse.
        df = self.radars_year

        # la valeur actuelle du slider.
        value = slider_range

        # le masque pour afficher seulement les radars installés à l'année indiquée par le slider
        # (y compris les années d'avant)
        mask = df['date_installation'] <= value

        # la fonction d'affichage du graphique avec ses paramètres.
        fig = px.scatter_mapbox(df[mask],
                                lat="latitude", lon="longitude",
                                hover_name="emplacement", color_discrete_sequence=["blue"],
                                zoom=5, height=850, width=850)

        # fonction pour afficher la map.
        fig.update_layout(mapbox_style="open-street-map")
        return fig


if __name__ == '__main__':
    rd_acc = Radar_Accidents()
    rd_acc.app.run_server(debug=True, port=8051)
