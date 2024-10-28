import paramiko

# ================================
# Define an SSH client and connect to a remote server
# Generalized SSH parameters with placeholders

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# Define server connection parameters
HOSTNAME = "<your_server_address>"  # Replace with target server address
USERNAME = "<your_username>"        # Replace with SSH username
PASSWORD = "<your_password>"        # Replace with SSH password

# Connect to the SSH server
try:
    ssh.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
    
    # Define arguments for the rwfilter command
    filter_type = "<type of record>"                # Type of flow records to select
    flags_initial = "<flags to match>"             # Initial flags to match (e.g., SYN flag for TCP connection attempts)
    start_date = "<start date>"          # Start date for filtering data
    end_date = "<end date>"            # End date for filtering data
    output_format = "stdout"           # Specify stdout to pipe the output
    bin_size = "<bin time size, example: 3600>"   # Size of time bins (in seconds) for aggregation (e.g., 3600 for hourly bins)
    delimiter = ","                    # Delimiter for separating output fields

    # Construct the command with format strings for dynamic argument substitution
    command = (
        f"/bin/rwfilter --type={filter_type} --flags-initial={flags_initial} "
        f"--start-date={start_date} --end-date={end_date} --pass={output_format} | "
        f"/bin/rwcount -delimited={delimiter} --bin-size={bin_size}"
    )

    # Execute the command
    _, stdout, _ = ssh.exec_command(command)
    result = stdout.read()

    # Print the command output
    print(result.decode('ascii'))

except Exception as e:
    print(f"Error occurred during SSH connection or command execution: {e}")

finally:
    ssh.close()

# ================================ 
# Instead of defining the query over and over, we can define an object ! #
# Define a reusable SSHCommand class for executing commands over SSH

class SSHCommand:
    """
    SSHCommand class to manage SSH connections and execute commands.
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
        Execute a command on the SSH server and return the output.
        """
        _, stdout, _ = self.ssh.exec_command(command)
        result = stdout.read()
        return result.decode('ascii')

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
    username="<your_username>",       # Repla
