import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from plotly.graph_objs import *


def run_dash(bales_graph_file_path, pie_chart_file_path, bar_chart_file_path, leader_chart_file_path, leader):
    df_bales = pd.read_csv(bales_graph_file_path)
    df_word = pd.read_csv(pie_chart_file_path)
    df_pos_neg = pd.read_csv(bar_chart_file_path)
    df_leader = pd.read_csv(leader_chart_file_path)

    leader_title = "Potential leader: Player " + str(leader)
    leadership_style = "There is a task-oriented positive leadership style"
    player_colors = ['#E06C75', '#98C379', '#E5C07B', '#C678DD', '#56B6C2']
    leader_color = player_colors[leader-1]

    app = dash.Dash(
        external_stylesheets=[dbc.themes.SUPERHERO]
    )

    layout_set = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Verdana",
            color="Black"
        )
    )

    df_line_graph = df_bales
    fig_bales = px.line(df_line_graph, x="Category", y="Amount", color="Player",
                        color_discrete_map={'Player 1': '#E06C75', 'Player 2': '#98C379', 'Player 3': '#E5C07B',
                                            'Player 4': '#C678DD', 'Player 5': '#56B6C2'},
                        title="Bales Interaction Process Analysis Profiles")

    df_pie_chart = df_word
    fig_pie_chart = px.pie(df_pie_chart, values="Words", names='Player', hole=.5, color='Player',
                           color_discrete_map={'Player 1': '#E06C75', 'Player 2': '#98C379', 'Player 3': '#E5C07B',
                                               'Player 4': '#C678DD', 'Player 5': '#56B6C2'},
                           title="Percentage of words "
                                 "said")

    df_bar_chart = df_pos_neg
    fig_bar_chart = px.bar(df_bar_chart, x="Amount", y="Polarity", color="Player", orientation="h",
                           color_discrete_map={'Player 1': '#E06C75', 'Player 2': '#98C379', 'Player 3': '#E5C07B',
                                               'Player 4': '#C678DD', 'Player 5': '#56B6C2'}, title="Amount of "
                                                                                                    "positive and "
                                                                                                    "negative "
                                                                                                    "statements")

    df_leader_chart = df_leader
    fig_leader_chart = px.bar(df_leader_chart, x="Category", y="Amount (%)", color='Category', color_discrete_map={'Sentences': leader_color, 'Positive': leader_color, 'Negative': leader_color}, title=leader_title)

    fig_bales.update_layout(layout_set)
    fig_pie_chart.update_layout(layout_set)
    fig_bar_chart.update_layout(layout_set)
    fig_leader_chart.update_layout(layout_set)
    fig_leader_chart.update_layout(showlegend=False)

    app.layout = html.Div([
        dbc.Row([
            html.Div([html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Logo_marine.svg/1200px-Logo_marine.svg.png',
                style={'margin-left': '70%', 'margin-right': 'auto', 'margin-bottom': '1%'}),
                html.Img(src='https://www.kiemt.nl/wp-content/uploads/2018/06/logos-partners_0000s_0017_UTwente.png',
                         style={'margin-left': 'auto', 'margin-right': '10%', 'margin-bottom': '1%'})],
                style={'background-color': '#ffffff', 'width': '100%', 'height': '90px', 'display': 'flex'}),
        ]),
        dbc.Row([
            html.Div(
                dbc.Col(html.H1("Communication and Leadership Competency Dashboard",
                                style={'textAlign': 'left', 'font-family': 'Verdana', 'background-color': '#0E61AA',
                                       'font-size': '30px', 'margin': '5px'}), width=12))
        ], style={'background-color': '#0E61AA', 'padding-left': '1%', 'padding-top': '10px', 'padding-bottom': '10px',
                  'box-shadow': '0px 5px 2px #888888'}),
        dbc.Row([
            html.Div(
                dbc.Col(dcc.Graph(
                    id="test",
                    figure=fig_bales)
                ),
                style={'background-color': 'white', 'width': '50%', 'border-radius': '25px', 'margin-left': '3%',
                       'margin-top': '2%', 'margin-bottom': '2%', 'box-shadow': '5px 10px 5px'}),
            html.Div(
                dbc.Col(dbc.Col(dcc.Graph(
                             id="test4",
                             figure=fig_leader_chart)
                         )),
                style={'background-color': 'white', 'width': '18.5%', 'border-radius': '25px', 'margin-left': '3%',
                       'margin-top': '2%', 'margin-bottom': '2%', 'box-shadow': '5px 10px 5px'}),
            html.Div(
                dbc.Col([html.H1("What type of leadership has the group leader?",
                                 style={'textAlign': 'center', 'color': 'black', 'margin': '5px', 'margin-top': '20px',
                                        'font-size': '25px'}),
                         html.Hr(style={'border': '1px solid black'}),
                         html.H2(leadership_style,
                                 style={'textAlign': 'center', 'color': 'black', 'margin': '5px', 'margin-top': '20px',
                                        'font-size': '20px'}),
                         html.H3("Source: Butler et al.",
                                 style={'textAlign': 'right', 'color': 'black', 'margin': '5px', 'margin-top': '75%',
                                        'font-size': '13px'})]),
                style={'background-color': 'white', 'width': '18.5%', 'border-radius': '25px', 'margin-left': '3%',
                       'margin-top': '2%', 'margin-bottom': '2%', 'box-shadow': '5px 10px 5px'})
        ]),
        dbc.Row([
            html.Div(
                dbc.Col(dcc.Graph(
                    id="test2",
                    figure=fig_pie_chart)
                ), style={'background-color': 'white', 'width': '35%', 'border-radius': '25px', 'margin-left': '3%',
                          'margin-bottom': '2%', 'box-shadow': '5px 10px 5px'}),
            html.Div(
                dbc.Col(dcc.Graph(
                    id="test3",
                    figure=fig_bar_chart)
                ),
                style={'background-color': 'white', 'box-shadow': '5px 10px 5px', 'width': '55%',
                       'border-radius': '25px',
                       'margin-left': '3%', 'margin-bottom': '2%'})
        ])
    ], style={'background-color': '#f3f3f3'})

    return app

