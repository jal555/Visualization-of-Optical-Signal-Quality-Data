'''
Project Title: Analysis and Visualization of Optical Signal Quality Data
File Name: parse_data.py
Author: Jennifer Lawless

Description: Connects to the server and parses the optical signal data contained
             in the numerous JSON files.
'''
####################################### Imports #######################################

from datetime import datetime
import json
import os
import paramiko
import sys
import time

from optical_signal_data import Lab, DataTimestamp, NodeData, Measurements, Instantaneous, FifteenMinuteBin

####################################### Constants #######################################

HOST = "lambda1.cs.cornell.edu"
DATA_DIR = "/data/ymm26/adva-performance-monitoring"
TIME_DELAY = 1.5
BREAK_LEVEL = 5000

####################################### Functions #######################################

def connect_to_server(host, username, password):
    '''
    Description: Connects to the server via SSH.
    Input:
        host - the IP address of the server to connect to.
        username - the username of the account.
        password - the password associated with the account.
    Output:
        client - the SSH client connected to the server.
    '''

    # Start an SSH client:
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Try connecting to the server and running a command:
    try:
        # Connect to the server:
        print(f"Connecting to {username}@{host}........")
        client.connect(host, username=username, password=password, timeout=90)

        # Execute a command:
        _stdin, _stdout, _stderr = client.exec_command("echo Connection successful!")

        # Print the output from the command:
        print(_stdout.read().decode())

    # Print that the connection failed and exit the program:
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # Return the client:
    return client


def parse_data(client, data_dir):
    '''
    Description: Parses the JSON optical signal quality data and creates 
                 a list of OpticalSignalData objects.
    Input:
        client - the SSH client connected to the server.
        data_dir - the directory holding the JSON files.
    Output:
        optical_signal_data_list - list of Lab objects.
        lab_names - set of all lab names.
        node_names - dictionary of all node names in each lab.
    '''

    # Navigate to the correct directory and list all JSON files:
    _stdin, _stdout, _stderr = client.exec_command(f"cd {data_dir} && ls")

    # Compile a list of all the JSON files:
    json_files = _stdout.read().decode().splitlines()

    # Create a set to hold all of the lab names:
    lab_names = set()

    # Create a dictionary to hold all of the node names for each lab:
    node_names = dict()

    # Create a list to hold the Lab objects:
    optical_signal_data_list = []

    # Loop through the files:
    break_ctr = 0
    for json_file in json_files:

        # Limit the number of files to read (if necessary):
        if break_ctr >= BREAK_LEVEL:
            break
        break_ctr += 1

        # Introduce a delay to limit the rate of requests:
        time.sleep(TIME_DELAY)

        try:
            # Read the file and decode the data:
            _stdin, _stdout, _stderr = client.exec_command(f"cd {data_dir} && cat {json_file}")
            decoded_data = _stdout.read().decode()

        # Handle if there is a timeout due to rate of requests:
        except paramiko.ssh_exception.SSHException as e:
            print(f"SSHException on {json_file}: {e}")
            print("Returning the current optical signal data.")
            return optical_signal_data_list, lab_names, node_names

        # Continue to next file if empty:
        if not decoded_data.strip():
            continue

        # Load the data:
        else:
            try:
                data = json.loads(decoded_data)
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError on {json_file}: {e}")
                print("Skipping and continuing to next file.")
                continue

            # Print status:
            print(f"Parsing {json_file}........", end="")

            # Loop through all the data:
            for timestamp, labs in data.items():
                for lab in labs:

                    # Get the lab name:
                    lab_name = list(lab.keys())[0]

                    # Get the node data:
                    nodes = lab[lab_name]
                    node_data_list = []

                    # Loop through the nodes:
                    for node in nodes:

                        # Get the node name:
                        node_name = list(node.keys())[0]

                        # Add the node name to the dict:
                        if lab_name in node_names:
                            node_names[lab_name].add(node_name)
                        else:
                            node_names[lab_name] = set()
                            node_names[lab_name].add(node_name)

                        # Get the measurements data:
                        measurements_data = node[node_name]
                        instantaneous_data = measurements_data["instantaneous"]
                        fifteen_minute_bin_data = measurements_data["fifteen_minute_bin"]

                        # Instantiate class objects for the node data for this specific lab:
                        instantaneous = Instantaneous(**instantaneous_data)
                        fifteen_minute_bin = FifteenMinuteBin(**fifteen_minute_bin_data)
                        measurements = Measurements(instantaneous, fifteen_minute_bin)
                        node_data = NodeData(node_name, measurements)
                        node_data_list.append(node_data)

                    # Instantiate a class object for the timestamp:
                    data_timestamp = DataTimestamp(timestamp, node_data_list)

                    # Lab object already exists for this lab:
                    if lab_name in lab_names:

                        # Add to the list of timestamps within the Lab object:
                        for lab_obj in optical_signal_data_list:
                            if lab_name == lab_obj.lab_name:
                                lab_obj.add_timestamp(data_timestamp)

                    # Lab object needs to be created:
                    else:

                        # Add the lab name to the set of lab names:
                        lab_names.add(lab_name)

                        # Instantiate a class object for the lab:
                        lab_obj = Lab(lab_name)

                        # Add the timestamp object to this list within this lab:
                        lab_obj.add_timestamp(data_timestamp)

                        # Add to the list of Lab objects:
                        optical_signal_data_list.append(lab_obj)

            # Print status:
            print("complete!")

    # Return the optical signal data and the set of all lab and node names:
    return optical_signal_data_list, lab_names, node_names

    
####################################### Main Program #######################################

def main(USER, PASSWORD):

    # Print program status:
    script_name = os.path.basename(__file__)
    start_time = datetime.now()
    start_time_str = str(start_time)
    start_msg = f"********* STARTING {script_name} at {start_time_str} "
    star = "*"
    print(f"{star:*<{80}}")
    print(f"{start_msg:*<{80}}")

    # Connect to the server:
    client = connect_to_server(HOST, USER, PASSWORD)

    # Parse the data:
    optical_signal_data_list, lab_names, node_names = parse_data(client, DATA_DIR)

    # Close the connection:
    print(f"\nDisconnecting from {USER}@{HOST}........")
    client.close()
    print("Disconnected!")

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

    # Return the optical signal data and set of lab and node names:
    return optical_signal_data_list, lab_names, node_names
