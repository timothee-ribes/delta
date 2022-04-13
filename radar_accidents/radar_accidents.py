import dash

from dash import html


class Radar_Accidents():
    def __init__(self, application=None):
        self.main_layout = html.Div(children=[],
                                    style={
                                        'backgroundColor': 'white',
                                        'padding': '10px 50px 10px 50px'
                                    }
                                    )
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == '__main__':
    rd_acc = Radar_Accidents()
    rd_acc.app.run_server(debug=True, port=8051)
