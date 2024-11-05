## This DFT signals detection method relies upon the class defined in Paramiko_ssh_netflow_data_retrieval_and_parsing.py under Data Aquisition, and is re-pasted here for utility and continuitiy ## 
# The process requries tuning the bin size of the data slices based on the periodicity of the signal you are attempting to detect #

import paramiko
from io import StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================================ 
# Define a reusable SSHCommand class for executing commands over SSH

class SSHCommand:
    """
    SSHCommand class to manage SSH connections, execute commands, and parse command outputs.
    """

    def __init__(self, address="127.0.0.1", username="none", password="none"):
        """
        Initialize SSH connection parameters.
        """
        self.address = address
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh.connect(hostname=address, username=username, password=password)

    def execute(self, command=""):
        """
        Execute a command on the SSH server and return the output as a string.
        """
        _, stdout, _ = self.ssh.exec_command(command)
        result = stdout.read()
        return result.decode('ascii')

    def execute_and_parse(self, command="", delimiter=","):
        """
        Execute a command on the SSH server, parse the output into a DataFrame, and return the DataFrame.
        """
        result = self.execute(command)
        return pd.read_csv(StringIO(result), sep=delimiter)

    def close_connection(self):
        """
        Close the SSH connection.
        """
        self.ssh.close()

# ================================
# Define the time range for analysis

start_date = "<start_date>"  # Replace with the actual start date, e.g., "2024/01/01"
end_date = "<end_date>"      # Replace with the actual end date, e.g., "2024/12/31"

# ================================
# Function to calculate bin size in seconds

def calculate_bin_size(minutes):
    """
    Calculate bin size in seconds based on specified minute intervals.
    """
    return minutes * 60

# ================================
# Fetch netflow data for FFT analysis

def fetch_netflow_data(ssh_connection, start_date, end_date, flags="S/SA", bin_minutes=10):
    """
    Fetch netflow data based on parameters and return as a DataFrame.
    """
    bin_size = calculate_bin_size(bin_minutes)
    command = (
        f"/bin/rwfilter --type=all --flags-initial {flags} "
        f"--start-date={start_date} --end-date={end_date} --pass=stdout | "
        f"/bin/rwcount -delimited=, --bin-size={bin_size}"
    )
    return ssh_connection.execute_and_parse(command)

# Example usage with 10-minute bins
df = fetch_netflow_data(ssh_connection, start_date=start_date, end_date=end_date, bin_minutes=10)

# ================================
# Plot data, with and without logarithmic scaling

def plot_data(df, y_col="Packets", x_col="Date", logy=False):
    """
    Plot data with optional logarithmic scaling, setting y-limit based on data range.
    """
    max_y = df[y_col].max() + df[y_col].std()
    plot_title = "Packet Frequency (Log Scale)" if logy else "Packet Frequency"
    df.plot(x=x_col, y=y_col, logy=logy, rot=90, figsize=(12, 4), ylim=(0, max_y), title=plot_title)
    plt.show()

# Plot normal and log-transformed data
plot_data(df, logy=False)
plot_data(df, logy=True)

# ================================
# Perform FFT on the packet data and calculate Nyquist frequency

def calculate_fft(df, y_col="Packets", bin_seconds=10):
    """
    Perform FFT on packet data, calculate Nyquist frequency, and return FFT results and frequency bins.
    """
    packets = df[y_col]
    fft_result = np.fft.rfft(packets)
    
    # Calculate Nyquist frequency:
    # The Nyquist frequency is half of the sampling rate. Since we're sampling data in bins of 10 seconds, 
    # our maximum observable frequency is one cycle every 20 seconds.
    nyquist_freq = (86400 / bin_seconds) / 2  # 86400 seconds in a day, divided by bin size, then halved.
    
    # Calculate the width of each frequency bin
    num_bins = len(fft_result)
    bin_width = nyquist_freq / num_bins
    
    # Define the frequency range in which each bin corresponds to its respective frequency component
    frequencies = np.array([i * bin_width for i in range(num_bins)])

    return fft_result, frequencies

fft_result, frequencies = calculate_fft(df)

# ================================
# Plot FFT results to visualize frequency components

def plot_fft(frequencies, fft_result, bins_to_skip=500):
    """
    Plot the FFT results starting from a specified bin to ignore high-frequency noise.
    """
    max_y = abs(fft_result[bins_to_skip:]).max() + abs(fft_result[bins_to_skip:]).std()
    plt.figure(figsize=(12, 5))
    plt.ylim(0, max_y)
    plt.plot(frequencies[bins_to_skip:], abs(fft_result[bins_to_skip:]))
    plt.title("Frequency Spectrum of Packet Data")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.show()

plot_fft(frequencies, fft_result)

# ================================
# Detect significant signals in frequency domain based on threshold

def detect_significant_signals(fft_result, bins_to_skip=500, threshold_multiplier=5):
    """
    Detect significant frequency components using mean and standard deviation thresholding.
    """
    truncated_fft = abs(fft_result[bins_to_skip:])
    mean_val = np.mean(truncated_fft)
    stddev_val = np.std(truncated_fft)
    threshold = mean_val + threshold_multiplier * stddev_val

    signal_indices = np.argwhere(truncated_fft > threshold).flatten()
    return signal_indices, threshold

signal_indices, threshold = detect_significant_signals(fft_result)
print(f"Significant signals detected at indices: {signal_indices}")

# ================================
# Process IP addresses individually to check for strong signals

def process_ip_address(ssh_connection, ip_address, start_date, end_date, threshold, bin_minutes=10):
    """
    Fetch netflow data for a specific IP address, perform FFT, and check for strong signals.
    """
    bin_size = calculate_bin_size(bin_minutes)
    command = (
        f"/bin/rwfilter --type=all --saddress={ip_address} --flags-initial S/SA "
        f"--start-date={start_date} --end-date={end_date} --pass=stdout | "
        f"/bin/rwcount -delimited=, --bin-size={bin_size}"
    )
    ip_df = ssh_connection.execute_and_parse(command)
    packets = ip_df['Packets']
    fft_result = np.fft.rfft(packets)
    
    # Return FFT result for further analysis
    return fft_result

# Get a list of IP addresses initiating connections
def get_initiating_ips(ssh_connection, start_date, end_date, flags="S/SA"):
    """
    Retrieve IP addresses seen initiating connections in a specific time period.
    """
    command = (
        f"/bin/rwfilter --type=all --flags-initial {flags} "
        f"--start-date={start_date} --end-date={end_date} --pass=stdout | "
        f"/bin/rwuniq --fields=sip --delimited=','"
    )
    hosts_df = ssh_connection.execute_and_parse(command)
    return hosts_df['sIP'].values

# Retrieve IP addresses and check for signals
ips = get_initiating_ips(ssh_connection, start_date=start_date, end_date=end_date)

for ip in ips:
    # Use the threshold from detected significant signals
    fft_result = process_ip_address(ssh_connection, ip, start_date=start_date, end_date=end_date, threshold=threshold)
    
    # Check for signal strength and detect the frequency of the strongest signal
    truncated_fft = abs(fft_result[500:])
    strong_signal = np.any(truncated_fft > threshold)
    
    if strong_signal:
        # Find the frequency of the strongest detected signal
        max_freq_index = np.argmax(truncated_fft) + 500
        signal_frequency = frequencies[max_freq_index]
        print(f"Potential signal detected for IP address {ip} with frequency {signal_frequency} Hz.")

# Close SSH connection
ssh_connection.close_connection()
