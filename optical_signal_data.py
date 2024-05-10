'''
Project Title: Analysis and Visualization of Optical Signal Quality Data
File Name: optical_signal_data.py
Author: Jennifer Lawless

Description: Contain class objects to hold and organize the optical signal data.
'''
####################################### Imports #######################################

from datetime import datetime

####################################### Classes #######################################

class Lab:
    def __init__(self, lab_name):
        self.lab_name = lab_name        # Name of the lab where measurements were taken
        self.timestamp_list = []        # List of timestamps when the data was collected

    def __str__(self):
        return f"Lab Name: {self.lab_name}, Timestamp List: {self.timestamp_list}"
    
    def add_timestamp(self, timestamp):
        # Add a DataTimestamp object to the list:
        self.timestamp_list.append(timestamp)
    
class DataTimestamp:
    def __init__(self, timestamp, node_data_list):
        self.timestamp = datetime.fromtimestamp(float(timestamp))   # Unix timestamp when the data was collected
        self.node_data_list = node_data_list                        # list of NodeData objects representing data for a node

    def __str__(self):
        return f"Timestamp: {self.timestamp}, Node Data List: {self.node_data_list}"

class NodeData:
    def __init__(self, node_name, measurements):
        self.node_name = node_name          # Name of the node
        self.measurements = measurements    # Measurements object representing measurements taken at a node

    def __str__(self):
        return f"Node Name: {self.node_name}, Measurements: {self.measurements}"

class Measurements:
    def __init__(self, instantaneous, fifteen_minute_bin):
        self.instantaneous = instantaneous              # Instantaneous object representing current measurements
        self.fifteen_minute_bin = fifteen_minute_bin    # FifteenMinuteBin object representing data over the last 15 minutes

    def __str__(self):
        return f"Instantaneous: {self.instantaneous}, Fifteen Minute Bin: {self.fifteen_minute_bin}"

class Instantaneous:
    def __init__(self, power, ber, snr, dgd, qfactor, chromatic_dispersion, carrier_offset):
        self.power = power                                  # Optical power level (measured in decibels (dB))
        self.ber = ber                                      # Bit Error Rate = performance measure of a system
        self.snr = snr                                      # Signal-to-Noise Ratio = measure of signal strength relative to background noise
        self.dgd = dgd                                      # Differential Group Delay = measure of difference in travel time between fastest and slowest signals
        self.qfactor = qfactor                              # Q-factor = measure of quality of a signal
        self.chromatic_dispersion = chromatic_dispersion    # Chromatic dispersion = measure of how light pulses spread out as they travel down the fiber
        self.carrier_offset = carrier_offset                # Carrier offset = measure of offset of the carrier frequency from original frequency

    def __str__(self):
        return f"Power: {self.power}, BER: {self.ber}, SNR: {self.snr}, DGD: {self.dgd}, QFactor: {self.qfactor}, Chromatic Dispersion: {self.chromatic_dispersion}, Carrier Offset: {self.carrier_offset}"

class FifteenMinuteBin:
    def __init__(self, power, ber, snr, dgd, qfactor, chromatic_dispersion, carrier_offset):
        self.power = RangeData(**power)                                  # Optical power level (measured in decibels (dB))
        self.ber = RangeData(**ber)                                      # Bit Error Rate = performance measure of a system
        self.snr = RangeData(**snr)                                      # Signal-to-Noise Ratio = measure of signal strength relative to background noise
        self.dgd = RangeData(**dgd)                                      # Differential Group Delay = measure of difference in travel time between fastest and slowest signals
        self.qfactor = RangeData(**qfactor)                              # Q-factor = measure of quality of a signal
        self.chromatic_dispersion = RangeData(**chromatic_dispersion)    # Chromatic dispersion = measure of how light pulses spread out as they travel down the fiber
        self.carrier_offset = RangeData(**carrier_offset)                # Carrier offset = measure of offset of the carrier frequency from original frequency

    def __str__(self):
        return f"Power: {self.power}, BER: {self.ber}, SNR: {self.snr}, DGD: {self.dgd}, QFactor: {self.qfactor}, Chromatic Dispersion: {self.chromatic_dispersion}, Carrier Offset: {self.carrier_offset}"

class RangeData:
    def __init__(self, low, median, high):
        self.low = low          # low measurement
        self.median = median    # median measurement
        self.high = high        # high measurement

    def __str__(self):
        return f"Low: {self.low}, Median: {self.median}, High: {self.high}"
