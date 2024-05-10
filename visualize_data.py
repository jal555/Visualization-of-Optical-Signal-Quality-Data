'''
Project Title: Analysis and Visualization of Optical Signal Quality Data
File Name: visualize_data.py
Author: Jennifer Lawless

Description: Visualizes the optical signal data.
'''
####################################### Imports #######################################

from collections import defaultdict
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime
import os
import plotly.graph_objects as go
import sys

from optical_signal_data import Lab, DataTimestamp, NodeData, Measurements, Instantaneous, FifteenMinuteBin
import parse_data

####################################### Functions #######################################

def generate_graph_helper(lab, node_data_dict, graph_title, x_axis_key, y_axis_key, x_axis_title, y_axis_title):
    '''
    Description: Uses DCC and Plotly to generate a graph given some specifications.
    Input:
        lab - Lab class object.
        node_data_dict - dictionary of measurement data of each node in the lab.
        graph_title - title of the graph.
        x_axis_key - key to index into the measurement data dictionary for the x-axis data.
        y_axis_key - key to index into the measurement data dictionary for the y-axis data.
        x_axis_title - title of the x-axis.
        y_axis_title - title of the y-axis.
    Output:
        lab_graph - generated graph for a specific metric over time in this lab.
    '''
    
    # Configure the figure for the graph:
    fig = go.Figure()
    for node_name, data in node_data_dict.items():
        fig.add_trace(go.Scatter(
            x=data[x_axis_key],
            y=data[y_axis_key],
            mode='lines',
            name=node_name,
            line=dict(width=2)
        ))

    # Define the layout:
    fig.update_layout(
        title=go.layout.Title(
            text=f'<b>{graph_title}</b>',
            xref="paper",
            x=0.5,
            font=go.layout.title.Font(
                size=22,
                color="#007BFF",
                family='Arial'
            )
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text=f'<b>{x_axis_title}</b>',
                font=go.layout.xaxis.title.Font(
                    size=16,
                    color="#007BFF",
                    family='Arial'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=f'<b>{y_axis_title}</b>',
                font=go.layout.yaxis.title.Font(
                    size=16,
                    color="#007BFF",
                    family='Arial'
                )
            )
        ),
        legend=go.layout.Legend(
            title=go.layout.legend.Title(
                text=f'<b>Nodes</b>',
                font=go.layout.legend.title.Font(
                    color="#007BFF",
                    family='Arial'
                )
            )
        ),
        autosize=True,
        hovermode='closest',
        showlegend=True,
        plot_bgcolor='rgba(240,240,240,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(
            size=12,
            color="#7f7f7f",
            family="Arial"
        ),
    )

    # Generate the graph for this lab:
    lab_graph = dcc.Graph(
        id=f'{lab.lab_name}-{graph_title}',
        figure=fig
    )

    # Return the graph:
    return lab_graph


def generate_graphs(optical_signal_data_list):
    '''
    Description: Visualizes optical signal quality data by generating graphs.
    Input:
        optical_signal_data_list - list of Lab objects.
    Output:
        graphs - a dictionary of graphs for each lab, with the lab name as the key.
    '''
    # Create a dictionary to hold all the graphs:
    graphs = dict()

    # Loop through the lab data:
    for lab in optical_signal_data_list:

        # Create a dictionary to hold the data for each node:
        node_data_dict = defaultdict(lambda: {
            'timestamps': [], 
            'powers_instantaneous': [], 
            'bers_instantaneous': [],
            'snrs_instantaneous': [],
            'dgds_instantaneous': [],
            'qfactors_instantaneous': [],
            'chrom_disp_instantaneous': [],
            'carrier_offset_instantaneous': [],
        })

        # Create lists of all the keys for the node data dictionary and all the graph and axis titles:
        graph_titles = ["Optical Power Level vs. Time", "Bit Error Rate vs. Time", "Signal-to-Noise Ratio vs. Time", "Differential Group Delay vs. Time", 
                        "Q-Factor vs. Time", "Chromatic Dispersion vs. Time", "Carrier Offset vs. Time"]
        x_axis_key = "timestamps"
        x_axis_title = "Time"
        y_axis_keys = ["powers_instantaneous", "bers_instantaneous", "snrs_instantaneous", "dgds_instantaneous", "qfactors_instantaneous", 'chrom_disp_instantaneous', 'carrier_offset_instantaneous']
        y_axis_titles = ["Optical Power Level (measured in dB)", "Bit Error Rate (BER)", "Signal-to-Noise Ratio (SNR)", "Differential Group Delay (DGD)", "Q-Factor", "Chromatic Dispersion (measured in ps/nm/km)", "Carrier Offset (measured in Hz)"]

        # Loop through each timestamp and node within that timestamp:
        for data_timestamp in lab.timestamp_list:
            for node_data in data_timestamp.node_data_list:

                # Aggregate the data for this node:
                node_data_dict[node_data.node_name]['timestamps'].append(data_timestamp.timestamp)
                node_data_dict[node_data.node_name]['powers_instantaneous'].append(node_data.measurements.instantaneous.power)
                node_data_dict[node_data.node_name]['bers_instantaneous'].append(node_data.measurements.instantaneous.ber)
                node_data_dict[node_data.node_name]['snrs_instantaneous'].append(node_data.measurements.instantaneous.snr)
                node_data_dict[node_data.node_name]['dgds_instantaneous'].append(node_data.measurements.instantaneous.dgd)
                node_data_dict[node_data.node_name]['qfactors_instantaneous'].append(node_data.measurements.instantaneous.qfactor)
                node_data_dict[node_data.node_name]['chrom_disp_instantaneous'].append(node_data.measurements.instantaneous.chromatic_dispersion)
                node_data_dict[node_data.node_name]['carrier_offset_instantaneous'].append(node_data.measurements.instantaneous.carrier_offset)

        # Loop through the y-axis metrics:
        for i in range(0, len(graph_titles)):

            # Generate the graph for this metric:
            graph = generate_graph_helper(lab, node_data_dict, graph_titles[i], x_axis_key, y_axis_keys[i], x_axis_title, y_axis_titles[i])

            # Add the graph to the dictionary:
            if lab.lab_name in graphs:
                graphs[lab.lab_name].append(graph)
            else:
                graphs[lab.lab_name] = [graph]

    # Return the graphs:
    return graphs

    
####################################### Main Program #######################################

def main(args):
    # Get username and password from the input arguments:
    USER = sys.argv[1]
    PASSWORD = sys.argv[2]

    # Call parse_data:
    optical_signal_data_list, lab_names, node_names = parse_data.main(USER, PASSWORD)

    # Sort the lab names:
    lab_names = sorted(list(lab_names))

    # Sort the node names:
    sorted_node_names = dict()
    for lab_name in node_names:
        sorted_node_names[lab_name] = sorted(list(node_names[lab_name]))

    # Print program status:
    script_name = os.path.basename(__file__)
    start_time = datetime.now()
    start_time_str = str(start_time)
    start_msg = f"********* STARTING {script_name} at {start_time_str} "
    star = "*"
    print(f"{star:*<{80}}")
    print(f"{start_msg:*<{80}}\n")

    # Import external stylesheets:
    external_stylesheets = [dbc.themes.BOOTSTRAP]

    # Initialize the Dash app:
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # Generate the graphs:
    print("Generating the graphs for each lab........")
    graphs = generate_graphs(optical_signal_data_list)
    print("Generation complete!\n")

    # Create a Card for each lab:
    lab_cards = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(lab_name, className="card-title", style={"color": "#3abf5b", 'fontWeight': 'bold'}),  # Light green color for the lab name
                            html.P(", ".join(sorted_node_names[lab_name]), className="card-text"),  # List of nodes for this lab
                        ]
                    ),
                    style={'marginTop': '20px', "marginBottom": "20px", "backgroundColor": "#e7f8eb"}  # Light green background color
                ), width=4
            ) for lab_name in lab_names
        ],
        style={'marginTop': '20px', "marginBottom": "20px", "backgroundColor": "#E9ECEF"}  # Lighter grey background color
    )

    # Define the metrics with sample values:
    metrics = [
        {"name": "Optical Power Level", "description": "The optical power level, measured in decibels (dB). The power levels are negative due to the very small amounts of power used in optical systems.", "sample_value": "-13.2 dB"},
        {"name": "Bit Error Rate (BER)", "description": "The number of bit errors divided by the total number of transferred bits during a time interval. It does not have a measurement unit.", "sample_value": "0.000104"},
        {"name": "Signal-to-Noise Ratio (SNR)", "description": "The measure of signal strength relative to background noise. The higher the SNR, the less obtrusive the background noise is. It is measured in decibels (dB).", "sample_value": "19.0"},
        {"name": "Differential Group Delay (DGD)", "description": "The measure of the difference in travel time between the fastest and slowest transmitted signals. It is measured in picoseconds (ps).", "sample_value": "11 ps"},
        {"name": "Q-Factor", "description": "The measure of the quality of a signal. Higher Q-Factors indicate lower distortion and better signal quality. It does not have a measurement unit.", "sample_value": "11.4"},
        {"name": "Chromatic Dispersion", "description": "A phenomenon in which light pulses spread out as they travel due to colors traveling at different speeds. It is measured in picoseconds per nanometer per kilometer (ps/nm/km).", "sample_value": "-169 ps/nm/km"},
        {"name": "Carrier Offset", "description": "A measure of how much the carrier frequency has been offset, or shifted, from its original frequency. It is measured in Hertz (Hz).", "sample_value": "-0.372 Hz"},
    ]

    # Create a Card for each metric:
    cards = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(metric["name"], className="card-title", style={"color": "#3abf5b", 'fontWeight': 'bold'}),  # Light green color for the metric name
                            html.P(metric["description"], className="card-text"),
                            html.P([html.B('Sample Value: '), metric["sample_value"]], className="card-text text-primary"),
                        ]
                    ),
                    style={'marginTop': '20px', "marginBottom": "20px", "backgroundColor": "#e7f8eb"}  # Light green background color
                ), width=4
            ) for metric in metrics
        ],
        style={'marginTop': '20px', "marginBottom": "20px", "backgroundColor": "#E9ECEF"}  # Lighter grey background color
    )

    # Create a list of Tabs to display the graphs:
    tab_components = html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(
                        [
                            dbc.Row([dbc.Col(graph)], style={'marginTop': '20px', "marginBottom": "20px", 'fontWeight': 'bold'}) for graph in graphs[lab_name]
                        ],
                        label = lab_name,
                        label_style={"color": "#3abf5b"},  # Light green color for the lab name
                        active_label_class_name="bg-success text-white"
                    ) for lab_name in lab_names
                ],
                style={"backgroundColor": "#ffffff"}  # White background color
            )
        ]
    )

    # Define the layout:
    app.layout = html.Div(
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(children='Visualization of Optical Signal Quality Data', className='card-title', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontFamily': 'Arial', 'color': '#007BFF', 'fontSize': '3em'}),  # Blue color for the title, larger font size
                        html.P(
                            "Dashboard created by Jennifer Lawless",
                            className="lead",
                            style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': '1.5em'}  # Larger font size for the subtitle
                        ),
                    ]
                ),
                style={'backgroundColor': '#E9ECEF', 'marginBottom': '20px', 'padding': '20px'}  # Lighter grey background color, more padding
            ),

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H2(children='Overview', className='card-title', style={'fontWeight': 'bold', 'fontFamily': 'Arial', 'color': '#007BFF'}),  # Blue color for the title
                            html.P('This dashboard visualizes optical signal quality data collected over the past year in various labs across New York state. Those labs and their associated nodes are as follows:', className="card-text", style={'size': 16}),
                            lab_cards
                        ]
                    )
                ],
                style={'backgroundColor': '#E9ECEF', 'marginBottom': '20px'}  # Lighter grey background color
            ),

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H2(children='Optical Signal Quality Metrics', className='card-title', style={'fontFamily': 'Arial', 'marginTop': '20px', 'fontWeight': 'bold', 'color': '#007BFF'}),  # Blue color for the title
                            html.P('For each node in a lab, seven different metrics were recorded to analyze the optical signal quality. Those metrics are as follows:', className="card-text", style={'size': 16}),
                            cards
                        ]
                    )
                ],
                style={'backgroundColor': '#E9ECEF', 'marginBottom': '20px'}  # Lighter grey background color
            ),

            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H2(children='Visualized Lab Data', className='card-title', style={'fontFamily': 'Arial', 'marginTop': '20px', 'fontWeight': 'bold', 'color': '#007BFF'}),  # Blue color for the title
                            html.P('For each lab, there is a clickable tab below that displays various graphs representing relationships between the optical signal quality metrics. Each of the graphs is interactive, allowing for zoom, removal of nodes from the display, and various other functions.', className="card-text", style={'size': 16}),
                            tab_components
                        ]
                    )
                ],
                style={'backgroundColor': '#E9ECEF'}  # Lighter grey background color
            )
        ],
        style={'fontFamily': 'Arial'}
    )

    # Run the Dash app:
    print("Creating the dashboard........")
    app.run_server(debug=True, use_reloader=False)
    print("\nDashboard closed.")

    # Print program status:
    end_time = datetime.now()
    end_time_str = str(end_time)
    elapsed_time = end_time - start_time
    elapsed_time_str = str(elapsed_time)
    end_msg = f"\n********* ENDING {script_name} at {end_time_str} "
    elapsed_time_msg = f"\n********* Elapsed Time: {elapsed_time_str} "
    print(f"{end_msg:*<{80}}")
    print(f"{elapsed_time_msg:*<{80}}")
    print(f"{star:*<{80}}")


if __name__ == "__main__":
    main(sys.argv[1:])