# Netflow Data Signal Detection Using Discrete Fourier Transform (DFT)

This script analyzes network flow data to detect periodic signals that may indicate Command and Control (C2) activity or other types of beaconing behaviors. The process involves fetching netflow data, performing frequency analysis using Discrete Fourier Transform (DFT), and identifying IP addresses with strong signals that could be of interest for further investigation.

## Overview

The script connects to a remote server to execute netflow queries, retrieves network traffic data, and then performs signal processing on this data. By transforming network traffic patterns into the frequency domain, the script helps identify recurring traffic patterns that are challenging to detect with standard time-domain analysis.

## Core Concepts

### Netflow Data

Netflow data records IP-based traffic information such as source and destination IPs, packet counts, and time of connection. This data is useful for identifying patterns in network behavior.

### Discrete Fourier Transform (DFT)

The DFT is a mathematical transformation that converts time-domain signals into the frequency domain. In this case, we apply the DFT to netflow data to detect periodic signals (e.g., beaconing) that may be indicative of malicious behavior. 

### Nyquist Frequency

The Nyquist frequency is half the sampling rate. Given a sampling interval (bin size), the Nyquist frequency represents the maximum observable frequency, which helps in determining which frequencies we can detect within the network data.

## Process

1. **Connect to Remote Server**: Use SSH to connect to a server with netflow data.
2. **Fetch Netflow Data**: Retrieve netflow data within a specified time range and bin size (sampling interval).
3. **Preliminary Analysis**: Plot the data with and without logarithmic scaling to identify any extreme variance.
4. **Frequency Analysis**:
   - Calculate the Discrete Fourier Transform (DFT) of packet counts.
   - Determine the Nyquist frequency based on the sampling interval.
   - Identify significant frequencies using a threshold (mean + n*standard deviation).
5. **Identify and Analyze IPs**:
   - Retrieve IP addresses initiating connections in the specified time range.
   - For each IP, perform frequency analysis and detect the strongest signal.
6. **Output**: Print IPs with detected signals, including the frequency of the strongest signal.

## Inputs

- **Start Date** (`start_date`): The beginning of the time range for analysis. Format as `YYYY/MM/DD`.
- **End Date** (`end_date`): The end of the time range for analysis. Format as `YYYY/MM/DD`.
- **Bin Size**: Set as minutes, converted internally to seconds. Determines the sampling interval for binning netflow data.
- **Threshold Multiplier**: Defines the sensitivity of signal detection. Higher values reduce sensitivity, while lower values increase it.
- **SSH Connection Parameters**: Server address, username, and password to connect to the remote server.

## Outputs

- **Data Plots**: 
  - Packet frequency over time, with and without logarithmic scaling.
  - Frequency spectrum plot displaying amplitude versus frequency.
- **Alert Messages**: For each IP with detected periodic signals, output the IP address and frequency of the strongest detected signal.

## Usage

1. **Define Parameters**:
   At the top of the script, set `start_date` and `end_date` to define the time range for analysis. Adjust other parameters as needed.
   
2. **Run the Script**:
   The script will:
   - Connect to the server,
   - Fetch netflow data,
   - Plot and analyze packet data,
   - Identify and alert on IPs with significant signals.
   
3. **Interpret Results**:
   For each IP address, the script will display a message if a strong signal is detected, providing the frequency of the signal for potential further investigation.

## Example

Assuming a 10-minute bin size and a date range of `2024/01/01` to `2019/12/31`, the script will process each IP initiating connections within this range, perform FFT analysis, and print out any IPs with significant signals.

Example output:
```plaintext
Potential signal detected for IP address 192.168.1.10 with frequency 0.0025 Hz.
