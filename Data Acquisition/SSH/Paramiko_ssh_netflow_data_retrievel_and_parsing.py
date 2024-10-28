import paramiko
from io import StringIO
import pandas as pd

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

        # Connect to the SSH server
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
# Instantiate the SSHCommand class and execute a command with generalized rwfilter arguments

# Define SSH connection parameters
ssh_connection = SSHCommand(
    address="<your_server_address>",  # Replace with target server address
    username="<your_username>",       # Replace with SSH username
    password="<your_password>"        # Replace with SSH password
)

# Define the rwfilter command with arguments
filter_type = "<type of record>"          # Type of flow records to select
flags_initial = "<flags to match>"        # Initial flags to match
start_date = "<start date>"               # Start date for filtering data
end_date = "<end date>"                   # End date for filtering data
output_format = "stdout"                  # Specify stdout to pipe the output
bin_size = "<bin time size, e.g., 3600>"  # Size of time bins in seconds
delimiter = ","                           # Delimiter for separating output fields

# Construct the command with format strings for dynamic argument substitution
remote_command = (
    f"/bin/rwfilter --type={filter_type} --flags-initial={flags_initial} "
    f"--start-date={start_date} --end-date={end_date} --pass={output_format} | "
    f"/bin/rwcount -delimited={delimiter} --bin-size={bin_size}"
)

# Execute the command and parse the result into a DataFrame
try:
    df = ssh_connection.execute_and_parse(remote_command, delimiter=delimiter)
    print(df)

finally:
    # Ensure SSH connection is closed
    ssh_connection.close_connection()
