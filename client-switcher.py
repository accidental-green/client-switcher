import os
import requests
import re
import fnmatch
import json
import random
import tarfile
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

# Define valid execution clients and networks
valid_clients = ['GETH', 'BESU', 'NETHERMIND', 'NONE']
valid_networks = ['MAINNET', 'GOERLI', 'SEPOLIA']

# Ask the user for the execution client to DELETE
eth_client_delete = ""
while eth_client_delete not in valid_clients:
    eth_client_delete = input("\n1) Select Execution Client to REMOVE (Geth, Besu, Nethermind, None): ").upper()
    if eth_client_delete not in valid_clients:
        print("Invalid option, please try again.")

# Ask the user for the execution client to INSTALL
eth_client_install = ""
while eth_client_install not in valid_clients:
    eth_client_install = input("\n2) Select Execution Client to INSTALL (Geth, Besu, Nethermind, None): ").upper()
    if eth_client_install not in valid_clients:
        print("Invalid option, please try again.")

# Ask the user for the network to use
eth_network = ""
while eth_network not in valid_networks:
    eth_network = input("\n3) Select Ethereum network (mainnet, goerli, sepolia): ").upper()
    if eth_network not in valid_networks:
        print("Invalid option, please try again.")

# Confirmation
confirmation = ""
while confirmation not in ['Y', 'N', 'YES', 'NO']:
    confirmation = input(f"\nYou are about to REMOVE {eth_client_delete} and INSTALL {eth_client_install}. Would you like to continue (y/n)? ").upper()
    if confirmation not in ['Y', 'N', 'YES', 'NO']:
        print("Invalid option, please try again.")

if confirmation in ['N', 'NO']:
    print("Operation cancelled by the user.")
    sys.exit()


print("\nPlease note that some operations require sudo permissions to operate.")
print("You may be prompted to enter your password to execute sudo commands.\n")

# Commands for different clients
geth_cmds = [
    "sudo rm -rf /usr/local/bin/geth",
    "sudo rm -rf /var/lib/geth",
    "sudo rm -rf /etc/systemd/system/geth.service",
    "sudo userdel -r geth || true",
]

besu_cmds = [
    "sudo rm -rf /usr/local/bin/besu",
    "sudo rm -rf /var/lib/besu",
    "sudo rm -rf /etc/systemd/system/besu.service",
    "sudo userdel -r besu || true",
]

nethermind_cmds = [
    "sudo rm -rf /usr/local/bin/nethermind",
    "sudo rm -rf /var/lib/nethermind",
    "sudo rm -rf /etc/systemd/system/nethermind.service",
    "sudo userdel -r nethermind || true",
]

# Execute specific commands based on the user's choice
if eth_client_delete == 'GETH':
    for cmd in geth_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif eth_client_delete == 'BESU':
    for cmd in besu_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif eth_client_delete == 'NETHERMIND':
    for cmd in nethermind_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif eth_client_delete == 'NONE':
    print("No client selected for deletion")

# Execution Code
    
# Update and upgrade packages
subprocess.run(['sudo', 'apt', '-y', 'update'])
subprocess.run(['sudo', 'apt', '-y', 'upgrade'])


# Install New Client
print(f"\nInstalling client: {eth_client_install}\n")
print(f"Creating usernames, directories, and serfice files...\n")
print(eth_client_install.lower()) 

eth_client_install = eth_client_install.lower()


############ GETH INSTALL##################
if eth_client_install == 'geth':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'geth'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/geth'])
    subprocess.run(['sudo', 'chown', '-R', 'geth:geth', '/var/lib/geth'])

    # Define the URL of the Geth download page
    url = 'https://geth.ethereum.org/downloads/'

    # Send a GET request to the download page and retrieve the HTML response
    response = requests.get(url)
    html = response.text

    # Use regex to extract the URL of the latest Geth binary for Linux (amd64)
    match = re.search(r'href="(https://gethstore\.blob\.core\.windows\.net/builds/geth-linux-amd64-[0-9]+\.[0-9]+\.[0-9]+-[0-9a-f]+\.tar\.gz)"', html)
    if match:
        download_url = match.group(1)
        filename = os.path.expanduser('~/geth.tar.gz')
        print(f'Downloading {download_url}...')
        response = requests.get(download_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Done! Binary saved to {filename}.')

        # Extract the contents of the tarball to the user's home folder
        with tarfile.open(filename, 'r:gz') as tar:
            dirname = tar.getnames()[0].split('/')[0]
            tar.extractall(os.path.expanduser('~'))

        # Remove the existing geth executable from /usr/local/bin if it exists
        if os.path.exists('/usr/local/bin/geth'):
            subprocess.run(['sudo', 'rm', '/usr/local/bin/geth'])
            print('Existing geth executable removed from /usr/local/bin.')

        # Copy the geth executable to /usr/local/bin
        src = os.path.expanduser(f'~/{dirname}/geth')
        subprocess.run(['sudo', 'cp', src, '/usr/local/bin/'])
        print('Geth executable copied to /usr/local/bin.')

        # Remove the downloaded file and extracted directory
        os.remove(filename)
        shutil.rmtree(os.path.expanduser(f'~/{dirname}'))
        print(f'Removed {filename} and directory {dirname}.')
    else:
        print('Error: could not find download URL.')

############ BESU INSTALL##################
if eth_client_install == 'besu':
	# Create User and directories
	subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'besu'])
	subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/besu'])
	subprocess.run(['sudo', 'chown', '-R', 'besu:besu', '/var/lib/besu'])

	# Get the latest version number
	url = "https://api.github.com/repos/hyperledger/besu/releases/latest"
	response = urllib.request.urlopen(url)
	data = json.loads(response.read().decode("utf-8"))
	latest_version = data['tag_name']

	besu_version = latest_version

	# Download the latest version
	download_url = f"https://hyperledger.jfrog.io/hyperledger/besu-binaries/besu/{latest_version}/besu-{latest_version}.tar.gz"
	urllib.request.urlretrieve(download_url, f"besu-{latest_version}.tar.gz")

	# Extract the tar.gz file
	with tarfile.open(f"besu-{latest_version}.tar.gz", "r:gz") as tar:
	    tar.extractall()

	# Copy the extracted besu folder to /usr/local/bin/besu
	subprocess.run(["sudo", "cp", "-a", f"besu-{latest_version}", "/usr/local/bin/besu"], check=True)

	# Remove the downloaded .tar.gz file
	os.remove(f"besu-{latest_version}.tar.gz")

	# Install OpenJDK-17-JRE
	subprocess.run(["sudo", "apt", "-y", "install", "openjdk-17-jre"])

	# Install libjemalloc-dev
	subprocess.run(["sudo", "apt", "install", "-y", "libjemalloc-dev"])

############ NETHERMIND INSTALL##################
if eth_client_install == 'nethermind':
    # Create User and directories
    subprocess.run(["sudo", "useradd", "--no-create-home", "--shell", "/bin/false", "nethermind"])
    subprocess.run(["sudo", "mkdir", "-p", "/var/lib/nethermind"])
    subprocess.run(["sudo", "chown", "-R", "nethermind:nethermind", "/var/lib/nethermind"])
    subprocess.run(["sudo", "apt-get", "install", "libsnappy-dev", "libc6-dev", "libc6", "unzip", "-y"], check=True)

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/NethermindEth/nethermind/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Search for the asset with the name that ends in linux-x64.zip
    assets = response.json()['assets']
    download_url = None
    zip_filename = None
    for asset in assets:
        if asset['name'].endswith('linux-x64.zip'):
            download_url = asset['browser_download_url']
            zip_filename = asset['name']
            break

    if download_url is None or zip_filename is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to a temporary file
    with tempfile.NamedTemporaryFile('wb', suffix='.zip', delete=False) as temp_file:
        temp_file.write(response.content)
        temp_path = temp_file.name

    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract the binary to the temporary directory
        with zipfile.ZipFile(temp_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Copy the contents of the temporary directory to /usr/local/bin/nethermind using sudo
        subprocess.run(["sudo", "cp", "-a", f"{temp_dir}/.", "/usr/local/bin/nethermind"])

    # chown nethermind:nethermind /usr/local/bin/nethermind
    subprocess.run(["sudo", "chown", "nethermind:nethermind", "/usr/local/bin/nethermind"])

    # chown nethermind:nethermind /usr/local/bin/nethermind/Nethermind.Runner
    subprocess.run(["sudo", "chown", "nethermind:nethermind", "/usr/local/bin/nethermind/Nethermind.Runner"])

    # chmod a+x /usr/local/bin/nethermind/Nethermind.Runner
    subprocess.run(["sudo", "chmod", "a+x", "/usr/local/bin/nethermind/Nethermind.Runner"])

    # Remove the temporary zip file
    os.remove(temp_path)

    nethermind_version = os.path.splitext(zip_filename)[0]    
 
###### CREATE SERVICE FILES ######

eth_network = eth_network.lower()

###### GETH SERVICE FILE #############
if eth_client_install == 'geth':
    geth_service_file_lines = [
        '[Unit]',
        'Description=Geth Execution Client (Mainnet)',
        'Wants=network.target',
        'After=network.target',
        '',
        '[Service]',
        'User=geth',
        'Group=geth',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'TimeoutStopSec=600',
        'ExecStart=/usr/local/bin/geth \\',
        f'    --{eth_network} \\',
        '    --datadir /var/lib/geth \\',
        '    --authrpc.jwtsecret /var/lib/jwtsecret/jwt.hex',
        '',
        '[Install]',
        'WantedBy=default.target',
    ]

    geth_service_file = '\n'.join(geth_service_file_lines)

    geth_temp_file = 'geth_temp.service'
    geth_service_file_path = '/etc/systemd/system/geth.service'

    with open(geth_temp_file, 'w') as f:
        f.write(geth_service_file)

    os.system(f'sudo cp {geth_temp_file} {geth_service_file_path}')
    os.remove(geth_temp_file)

############ BESU SERVICE FILE ###############
if eth_client_install == 'besu':
    besu_service_file_lines = [
        '[Unit]',
        'Description=Besu Execution Client (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=besu',
        'Group=besu',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'Environment="JAVA_OPTS=-Xmx5g"',
        'ExecStart=/usr/local/bin/besu/bin/besu \\',
        f'    --network={eth_network} \\',
        '    --sync-mode=X_SNAP \\',
        '    --data-path=/var/lib/besu \\',
        '    --data-storage-format=BONSAI \\',
        '    --engine-jwt-secret=/var/lib/jwtsecret/jwt.hex',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    besu_service_file = '\n'.join(besu_service_file_lines)

    besu_temp_file = 'besu_temp.service'
    besu_service_file_path = '/etc/systemd/system/besu.service'

    with open(besu_temp_file, 'w') as f:
        f.write(besu_service_file)

    os.system(f'sudo cp {besu_temp_file} {besu_service_file_path}')
    os.remove(besu_temp_file)

####### NETHERMIND SERVICE FILE ###########
if eth_client_install == 'nethermind':
    nethermind_service_file_lines = [
        '[Unit]',
        'Description=Nethermind Execution Client (Mainnet)',
        'Wants=network.target',
        'After=network.target',
        '',
        '[Service]',
        'User=nethermind',
        'Group=nethermind',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'WorkingDirectory=/var/lib/nethermind',
        'Environment="DOTNET_BUNDLE_EXTRACT_BASE_DIR=/var/lib/nethermind"',
        'ExecStart=/usr/local/bin/nethermind/Nethermind.Runner \\',
        f'    --config {eth_network.lower()} \\',
        '    --datadir /var/lib/nethermind \\',
        '    --Sync.SnapSync true \\',
        '    --Sync.AncientBodiesBarrier 11052984 \\',
        '    --Sync.AncientReceiptsBarrier 11052984 \\',
        '    --JsonRpc.JwtSecretFile /var/lib/jwtsecret/jwt.hex',
        '',
        '[Install]',
        'WantedBy=default.target',
    ]

    nethermind_service_file = '\n'.join(nethermind_service_file_lines)

    nethermind_temp_file = 'nethermind_temp.service'
    nethermind_service_file_path = '/etc/systemd/system/nethermind.service'

    with open(nethermind_temp_file, 'w') as f:
        f.write(nethermind_service_file)

    os.system(f'sudo cp {nethermind_temp_file} {nethermind_service_file_path}')

    os.remove(nethermind_temp_file)

#### END SERVICE FILES #####

# Extract the part before the period
client_name = eth_client_install.lower().split('.')[0]

# Run post-install commands
subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=False)

# Print the final output
inbound_ports = subprocess.run(["sudo", "ufw", "status", "numbered"], stdout=subprocess.PIPE).stdout
if inbound_ports is not None:
    inbound_ports = inbound_ports.decode()
else:
    inbound_ports = ""
print(f'\nFirewall Status:\nInbound Ports: {inbound_ports}Outbound Ports: 9000, 30303, 6673/tcp\n')

print("Installation successful! Details below:\n")

print(f'Removed: {eth_client_delete.upper()}\n')

print(f'Installed: {eth_client_install.upper()}\n')

if eth_client_install == 'geth':
    geth_version = subprocess.run(["geth", "--version"], stdout=subprocess.PIPE).stdout
    if geth_version is not None:
        geth_version = geth_version.decode()
        geth_version = geth_version.split(" ")[-1]
    else:
        geth_version = ""
    print(f'Geth Version: v{geth_version}')

if eth_client_install == 'besu':
    print(f'Besu Version: {besu_version}\n')
    
if eth_client_install == 'nethermind':
    print(f'Nethermind Version: \n{nethermind_version}\n')


print(f"Client switch was successful! {eth_client_install.upper()} is now installed and ready to sync!\n")


