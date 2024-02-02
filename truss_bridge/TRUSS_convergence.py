from dash import Dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def get_truss_data_for_iteration(TRUSS1, X_init_single, point_index):
    current_item = X_init_single[point_index]
    TRUSS1.Write_call_state(current_item.numpy(), final=False)
    return TRUSS1.state['nodes'], TRUSS1.state['member_df']

layout={
    'title': 'Hover over a point in the loss function to see the truss layout',
    'height': 500,  # Set the height of the figure
    'width': 1000,  # Set the width of the figure
    'plot_bgcolor': 'white',  # Set the plot background color
    'paper_bgcolor': 'white',  # Set the background color around the plot
}

def loss_function_figure(total_loss):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(len(total_loss)),  # Assuming each row corresponds to an iteration
        y=total_loss,
        mode='lines',
        name='Total Loss',
        line=dict(color='rgba(30, 136, 229, 0.8)')  # Fixed opacity
    ))
    fig.update_layout(
        title={
            'text': "Loss per Iteration",
            'font': {'size': 20, 'color': 'black', 'family': "Arial, sans-serif"},
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title="Iteration",
            showline=True,
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='black',
            linewidth=1,
            ticks='outside',
            tickfont=dict(size=12, color='black')
        ),
        yaxis=dict(
            title="Total Loss",
            showline=True,
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='black',
            linewidth=1,
            ticks='outside',
            tickfont=dict(size=12, color='black')
        ),
        plot_bgcolor='white',
        width=600,
        height=500,
        legend_title_text='Metric',
        legend_font_size=12,
        margin=dict(l=100, r=100, t=100, b=100)
    )
    return fig

def plot_truss_layout(nodes, member_df):
    fig = go.Figure()    
    for _, row in member_df.iterrows():
        node1 = row['Node #1']
        node2 = row['Node #2']
        x0, y0 = nodes[node1]
        x1, y1 = nodes[node2]
       
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines',
                                 line=dict(width=2, color='black'),
                                 name=f'Element between {node1} - {node2}'))

    node_x = [coord[0] for coord in nodes.values()]
    node_y = [coord[1] for coord in nodes.values()]
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', 
                             marker=dict(size=10, color='black', symbol='circle'),
                             name='Nodes'))

    fig.add_trace(go.Scatter(x=[node_x[0], node_x[-1]], y=[node_y[0], node_y[-1]], mode='markers',
                         marker=dict(size=30, color='#00B8C8', symbol='triangle-up'),
                         name='Supports'))

    fig.update_layout(
        title={
            'text': 'Truss Layout',
            'font': {'size': 20, 'color': 'black', 'family': "Arial, sans-serif"},
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='X Coordinate',
        yaxis_title='Y Coordinate',
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            zeroline=False,
            linecolor='black',
            linewidth=1
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            zeroline=False,
            linecolor='black',
            linewidth=1
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=500,
        width=1000
    )

    return fig