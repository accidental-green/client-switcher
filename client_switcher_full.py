import os
import re
import fnmatch
import json
import random
import tarfile
import getpass
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
import pwd
from pathlib import Path
import requests
import tkinter as tk
from tkinter import filedialog, font
from html.parser import HTMLParser

# Change to the home folder
os.chdir(os.path.expanduser("~"))

# Check sudo privileges
print("Checking sudo privileges")
try:
    subprocess.run(['sudo', '-v'], check=True)
    print("Sudo credentials authenticated.")
except subprocess.CalledProcessError:
    print("Failed to verify sudo credentials.")
    exit(1)

# Define variables
execution_clients = ["geth", "nethermind", "besu"]
execution_clients_cap = [client.capitalize() for client in execution_clients]
exec_labels = [client.capitalize() for client in execution_clients] + ["None"]

consensus_clients = ["nimbus", "teku", "prysm", "lighthouse"]
consensus_clients_cap = [client.capitalize() for client in consensus_clients]
cons_labels = [client.capitalize() for client in consensus_clients] + ["None"]

mevboost_client = ["mevboost"]

usernames_all = [
    "geth", "besu", "nethermind", "teku", "nimbus",
    "prysmbeacon", "prysmvalidator", "lighthousebeacon", "lighthousevalidator", "mevboost"
]

# Define temp keystore variables
temp_keystore_dir = f'{os.environ["HOME"]}/validator_keys_temp'

# Define the keystore_button as a global variable
keystore_button = None

def check_keystore_directory():
    global keystore_button  # Define keystore_button as a global variable
    if keystore_button is not None:
        if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):
            # Directory exists and is not empty
            keystore_button.config(text="Keystore successfully imported!", bg="#90EE90", fg="#282C34") # Light green with changed text
        else:
            keystore_button.config(text="Import Keystore", bg="#61afef", fg="#282C34")  # Original color and text

# GUI Code
def open_menu(event):
    event.widget.tk.call('tk::MenuInvoke', event.widget._nametowidget(event.widget.cget("menu")), 0)

def get_usb_mount_point():
    user = os.getlogin()
    return f"/media/{user}"

def import_keystore():
    file_path = filedialog.askopenfilename(title="Select a Keystore", initialdir=get_usb_mount_point(), filetypes=[("Keystore files", "*.json"), ("All files", "*.*")])

    if not file_path:  # If user cancels the dialog
        return None

    # Ensure the 'validator_keys_temp' directory exists
    if not os.path.exists(temp_keystore_dir):
        os.makedirs(temp_keystore_dir)

    # Copy the imported file into the 'validator_keys_temp' directory
    destination_path = os.path.join(temp_keystore_dir, os.path.basename(file_path))
    shutil.copy(file_path, destination_path)

    # Update the button after importing the keystore
    update_keystore_button()

    # Returns the path where the file was copied to
    return destination_path

def update_keystore_button():
    home_dir = os.path.expanduser('~')
    
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):
        # Directory exists and is not empty
        keystore_button.config(text="Keystore successfully imported!", bg="#90EE90", fg="#282C34") # Light green with changed text
    else:
        keystore_button.config(text="Import Keystore", bg="#61afef", fg="#282C34")  # Original color and text

# Create Root Window
root = tk.Tk()
root.title("Ethereum Client Switcher")
root.configure(background="#282C34")

# Define a variable to store data
saved_data = []

# Add a variable to store Ethereum Address
eth_address_var = tk.StringVar()

def submit():
    eth_network = network_var.get()
    execution_client_delete = execution_delete_var.get()
    consensus_client_delete = consensus_delete_var.get()  # Get consensus client to delete
    execution_client_install = execution_install_var.get()
    consensus_client_install = consensus_install_var.get()  # Get consensus client to install
    mevboost = mevboost_var.get()  # Get Mevboost option
    eth_address = eth_address_var.get()  # Get Ethereum Address
    
    saved_data.extend([eth_network, execution_client_delete, consensus_client_delete, execution_client_install, consensus_client_install, mevboost, eth_address])
    root.destroy()

# Define variables
network_var = tk.StringVar()
execution_delete_var = tk.StringVar()
consensus_delete_var = tk.StringVar()
execution_install_var = tk.StringVar()
consensus_install_var = tk.StringVar()
mevboost_var = tk.StringVar()
eth_address_var = tk.StringVar()

label_font = font.nametofont("TkDefaultFont").copy()
label_font.config(size=20)

# Ethereum network selection label
network_label = tk.Label(root, text="Ethereum Network:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
network_label.grid(column=0, row=0, padx=30, pady=30, sticky='e')

networks = ('Mainnet', 'Goerli', 'Sepolia', 'Holesky')
network_menu = tk.OptionMenu(root, network_var, *networks)
network_menu.config(bg="#9370DB", fg="#FFFFFF", activebackground="#9370DB", activeforeground="#FFFFFF", font=label_font, takefocus=True)
network_menu["menu"].config(bg="#9370DB", fg="#FFFFFF", activebackground="#9370DB", activeforeground="#FFFFFF", font=label_font)
network_menu.grid(column=1, row=0, padx=30, pady=30, ipadx=40, ipady=10)

# Add a separator (thicker white line) below Ethereum Network
separator3 = tk.Frame(root, height=40, bg="white", relief="sunken", borderwidth=40)
separator3.grid(column=0, row=1, columnspan=2, sticky="ew", padx=30, pady=20)

# Execution client selection (to delete) - Second Section with Updated Color Scheme
execution_delete_label_2 = tk.Label(root, text="Execution Client to DELETE:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
execution_delete_label_2.grid(column=0, row=2, padx=30, pady=30, sticky='e')

execution_delete_menu_2 = tk.OptionMenu(root, execution_delete_var, *exec_labels)
execution_delete_menu_2.config(bg="#FF5722", fg="#FFFFFF", activebackground="#FF7043", activeforeground="#FFFFFF", font=label_font, takefocus=True)
execution_delete_menu_2["menu"].config(bg="#FF5722", fg="#FFFFFF", activebackground="#FF7043", activeforeground="#FFFFFF", font=label_font)
execution_delete_menu_2.grid(column=1, row=2, padx=30, pady=30, ipadx=40, ipady=10)

# Consensus client selection (to delete)
consensus_delete_label = tk.Label(root, text="Consensus Client to DELETE:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
consensus_delete_label.grid(column=0, row=3, padx=30, pady=30, sticky='e')

consensus_clients = ('Lighthouse', 'Prysm', 'Nimbus', 'Teku', 'None')
consensus_delete_menu = tk.OptionMenu(root, consensus_delete_var, *cons_labels)
consensus_delete_menu.config(bg="#FF5722", fg="#FFFFFF", activebackground="#FF7043", activeforeground="#FFFFFF", font=label_font, takefocus=True)
consensus_delete_menu["menu"].config(bg="#FF5722", fg="#FFFFFF", activebackground="#FF7043", activeforeground="#FFFFFF", font=label_font)
consensus_delete_menu.grid(column=1, row=3, padx=30, pady=30, ipadx=40, ipady=10)

# Separator (thicker white line)
separator = tk.Frame(root, height=40, bg="white", relief="sunken", borderwidth=40)
separator.grid(column=0, row=4, columnspan=2, sticky="ew", padx=30, pady=20)

# Execution client selection (to install)
execution_install_label = tk.Label(root, text="Execution Client to INSTALL:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
execution_install_label.grid(column=0, row=5, padx=30, pady=30, sticky='e')

execution_install_menu = tk.OptionMenu(root, execution_install_var, *exec_labels)
execution_install_menu.config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font, takefocus=True)
execution_install_menu["menu"].config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font)
execution_install_menu.grid(column=1, row=5, padx=30, pady=30, ipadx=40, ipady=10)


# Consensus client selection (to install)
consensus_install_label_2 = tk.Label(root, text="Consensus Client to INSTALL:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
consensus_install_label_2.grid(column=0, row=6, padx=30, pady=30, sticky='e')

consensus_install_menu_2 = tk.OptionMenu(root, consensus_install_var, *cons_labels)
consensus_install_menu_2.config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font, takefocus=True)
consensus_install_menu_2["menu"].config(bg="#4CAF50", fg="#FFFFFF", activebackground="#8BC34A", activeforeground="#FFFFFF", font=label_font)
consensus_install_menu_2.grid(column=1, row=6, padx=30, pady=30, ipadx=40, ipady=10)

# Mevboost label
mevboost_label = tk.Label(root, text="Mevboost Settings (On/Off):", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
mevboost_label.grid(column=0, row=7, padx=30, pady=30, sticky='e')

# Mevboost options
mevboost_options = ('On', 'Off')
mevboost_menu = tk.OptionMenu(root, mevboost_var, *mevboost_options)
mevboost_menu.config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=label_font, takefocus=True)
mevboost_menu["menu"].config(bg="#2196F3", fg="#FFFFFF", activebackground="#64B5F6", activeforeground="#FFFFFF", font=label_font)
mevboost_menu.grid(column=1, row=7, padx=30, pady=30, ipadx=40, ipady=10)

# Add a separator (thicker white line) between Mevboost and Ethereum Address
separator4 = tk.Frame(root, height=40, bg="white", relief="sunken", borderwidth=40)
separator4.grid(column=0, row=8, columnspan=2, sticky="ew", padx=30, pady=20)

# Address for Validator Tips input
eth_address_label = tk.Label(root, text="ETH Address for Validator Tips:", bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
eth_address_label.grid(column=0, row=9, padx=30, pady=30, sticky='e')

eth_address_entry = tk.Entry(root, textvariable=eth_address_var, font=label_font)
eth_address_entry.grid(column=1, row=9, padx=30, pady=30, ipadx=40, ipady=10)

# Keystore import
keystore_label = tk.Label(root, text='Import existing keystore (optional):', bg="#282C34", fg="#ABB2BF", font=label_font, anchor='e')
keystore_label.grid(column=0, row=10, padx=30, pady=30, sticky='e')

keystore_button = tk.Button(root, text="Import Keystore", command=import_keystore, bg="#61afef", fg="#282C34", activebackground="#282C34", activeforeground="#ABB2BF", font=label_font, takefocus=True)
keystore_button.grid(column=1, row=10, padx=30, pady=30)

# Submit button
submit_button = tk.Button(root, text="Install", command=submit, bg="#C0C0C0", fg="#000000", activebackground="#61AFEF", activeforeground="#000000", font=label_font, takefocus=True)
submit_button.grid(column=1, row=11, padx=30, pady=60)

root.mainloop()

eth_network, execution_client_delete, consensus_client_delete, execution_client_install, consensus_client_install, mev_on_off, eth_address = saved_data

# Define User Input Variables
eth_network = saved_data[0]
execution_client_delete = saved_data[1]
consensus_client_delete = saved_data[2]
execution_client_install = saved_data[3]
consensus_client_install = saved_data[4]
mev_on_off = saved_data[5]
eth_address = saved_data[6]  # Ethereum Address

# Print User Input Variables including Ethereum Address
print("\n##### User Selected Inputs #####")
print(f"Ethereum Network: {eth_network}")
print(f"Execution Client to DELETE: {execution_client_delete}")
print(f"Consensus Client to DELETE: {consensus_client_delete}")
print(f"Execution Client to INSTALL: {execution_client_install}")
print(f"Consensus Client to INSTALL: {consensus_client_install}")
print(f"Mevoost: {mev_on_off}")
print(f"Ethereum Fee Address: {eth_address}\n")

######## VALIDATE USER INPUTS #########################

# Valid groups
valid_execution_clients = {'geth', 'besu', 'nethermind', 'none'}
valid_consensus_clients = {'lighthouse', 'nimbus', 'prysm', 'teku', 'none'}
valid_networks = {'mainnet', 'goerli', 'sepolia', 'holesky'}
valid_mev = {'on', 'off'}

# Make variables lowercase
eth_network = eth_network.lower()
execution_client_delete = execution_client_delete.lower()
execution_client_install = execution_client_install.lower()
consensus_client_delete = consensus_client_delete.lower()
consensus_client_install = consensus_client_install.lower()
mev_on_off = mev_on_off.lower()
fee_address = eth_address

# Validate user inputs
if eth_network not in valid_networks:
    raise ValueError(f"Invalid Ethereum Network: {eth_network}")

if execution_client_delete not in valid_execution_clients:
    raise ValueError(f"Invalid Execution Client to DELETE: {execution_client_delete}")

if consensus_client_delete not in valid_consensus_clients:
    raise ValueError(f"Invalid Consensus Client to DELETE: {consensus_client_delete}")

if execution_client_install not in valid_execution_clients:
    raise ValueError(f"Invalid Execution Client to INSTALL: {execution_client_install}")

if consensus_client_install not in valid_consensus_clients:
    raise ValueError(f"Invalid Consensus Client to INSTALL: {consensus_client_install}")

if mev_on_off not in valid_mev:
    raise ValueError(f"Invalid MEV Setting: {mev_on_off}")

print("\n##### Validated User Inputs #####")
print(f"Ethereum Network: {eth_network}")
print(f"Execution Client to DELETE: {execution_client_delete}")
print(f"Consensus Client to DELETE: {consensus_client_delete}")
print(f"Execution Client to INSTALL: {execution_client_install}")
print(f"Consensus Client to INSTALL: {consensus_client_install}")
print(f"Mevboost: {mev_on_off}")
print(f"Ethereum Address: {eth_address}\n")

#############################################
# Check if the temp_keystore_dir exists
if os.path.exists(temp_keystore_dir):
    # Count the number of JSON files in the directory
    num_json_files = len([file for file in os.listdir(temp_keystore_dir) if file.endswith(".json")])
    
    if num_json_files > 0:
        print(f"Validator Keystores to import: {num_json_files}")
    else:
        print("No Validator Keystores to import.")
else:
    print("No Validator Keystores to import.")

############################################################
# MEV SETTINGS AND INSTALLATION (if necessary)

# Mev service file path
mev_service_file = '/etc/systemd/system/mevboost.service'

# Check if the MEV service file exists
if os.path.exists(mev_service_file):
    mev_service_exists = True
else:
    mev_service_exists = False

# Determine the value of mev_install based on conditions
if mev_on_off == 'on' and not mev_service_exists:
    mev_install = 'yes'
else:
    mev_install = 'no'

# Check if MEV service exists and mev_on_off is 'on'
if mev_service_exists and mev_on_off == 'on':
    print("MEV already installed, configuring new clients for MEV")
elif mev_install == 'yes':
    print("Installing MEV and GO")

##### MEV INSTALL SETTINGS #####
# Check if a user exists
def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

class GoReleaseLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.linux_links = []
        self.capture = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and 'linux-amd64' in attr[1]:
                    self.linux_links.append(attr[1])
                    break

def get_latest_go_linux_release():
    """Fetch the latest Go release URL for Linux."""
    try:
        response = requests.get("https://go.dev/dl/")
        response.raise_for_status()
        parser = GoReleaseLinkParser()
        parser.feed(response.text)
        
        if parser.linux_links:
            return "https://go.dev" + parser.linux_links[0]
        raise Exception("No 64-bit Linux release found")
    except requests.RequestException as e:
        raise Exception("Failed to load the Go downloads page") from e

def append_to_bashrc(content):
    """Append content to .bashrc and update PATH."""
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, 'a') as bashrc:
        bashrc.write(content + '\n')
    os.environ["PATH"] += os.pathsep + "/usr/local/go/bin"

def install_go(go_url):
    """Install Go."""
    subprocess.run(["sudo", "apt", "-y", "install", "build-essential"], check=True)
    subprocess.run(["wget", "-O", "go.tar.gz", go_url], check=True)
    subprocess.run(["sudo", "rm", "-rf", "/usr/local/go"], check=True)
    subprocess.run(["sudo", "tar", "-C", "/usr/local", "-xzf", "go.tar.gz"], check=True)
    os.remove("go.tar.gz")
    append_to_bashrc('export PATH=$PATH:/usr/local/go/bin')

def install_mev_boost():
    """Install MEV-Boost and configure its service."""
    
    # Check if 'mevboost' user already exists
    if not user_exists('mevboost'):
        # Create 'mevboost' user if it doesn't exist
        subprocess.run(["sudo", "useradd", "--no-create-home", "--shell", "/bin/false", "mevboost"], check=True)

    # Proceed with MEV-Boost installation
    subprocess.run(['CGO_CFLAGS="-O -D__BLST_PORTABLE__" go install github.com/flashbots/mev-boost@latest'], shell=True)
    mev_boost_path = os.path.join(os.path.expanduser("~"), "go/bin/mev-boost")
    subprocess.run(["sudo", "cp", mev_boost_path, "/usr/local/bin"], check=True)
    subprocess.run(["sudo", "chown", "mevboost:mevboost", "/usr/local/bin/mev-boost"], check=True)

# Main execution mev and go
if mev_install == "yes":
    try:
        # Install Go
        go_url = get_latest_go_linux_release()
        print("Latest Go 64-bit release for Linux:", go_url)
        install_go(go_url)

        # Install MEV-Boost
        install_mev_boost()

        # Version checks
        print("\n##### Version Check #####\n")
        
        # Checking Go version
        go_version_output = subprocess.check_output(["go", "version"], text=True)
        print(go_version_output.strip())

        # Checking MEV-Boost version
        mev_boost_version_output = subprocess.check_output(["mev-boost", "--version"], text=True)
        print(mev_boost_version_output.strip())

        print("\n### Go and MEV-Boost Installation Complete ###\n")
    except Exception as e:
        print("Error:", e)

# MEV Relay Data
mainnet_relay_options = [
    {'name': 'Aestus', 'url': 'https://0xa15b52576bcbf1072f4a011c0f99f9fb6c66f3e1ff321f11f461d15e31b1cb359caa092c71bbded0bae5b5ea401aab7e@aestus.live'},
    {'name': 'Agnostic Gnosis', 'url': 'https://0xa7ab7a996c8584251c8f925da3170bdfd6ebc75d50f5ddc4050a6fdc77f2a3b5fce2cc750d0865e05d7228af97d69561@agnostic-relay.net'},
    {'name': 'Blocknative', 'url': 'https://0x9000009807ed12c1f08bf4e81c6da3ba8e3fc3d953898ce0102433094e5f22f21102ec057841fcb81978ed1ea0fa8246@builder-relay-mainnet.blocknative.com'},
    {'name': 'bloXroute Ethical', 'url': 'https://0xad0a8bb54565c2211cee576363f3a347089d2f07cf72679d16911d740262694cadb62d7fd7483f27afd714ca0f1b9118@bloxroute.ethical.blxrbdn.com'},
    {'name': 'bloXroute Max Profit', 'url': 'https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com'},
    {'name': 'bloXroute Regulated', 'url': 'https://0xb0b07cd0abef743db4260b0ed50619cf6ad4d82064cb4fbec9d3ec530f7c5e6793d9f286c4e082c0244ffb9f2658fe88@bloxroute.regulated.blxrbdn.com'},
    {'name': 'Eden Network', 'url': 'https://0xb3ee7afcf27f1f1259ac1787876318c6584ee353097a50ed84f51a1f21a323b3736f271a895c7ce918c038e4265918be@relay.edennetwork.io'},
    {'name': 'Flashbots', 'url': 'https://0xac6e77dfe25ecd6110b8e780608cce0dab71fdd5ebea22a16c0205200f2f8e2e3ad3b71d3499c54ad14d6c21b41a37ae@boost-relay.flashbots.net'},
    {'name': 'Manifold', 'url': 'https://0x98650451ba02064f7b000f5768cf0cf4d4e492317d82871bdc87ef841a0743f69f0f1eea11168503240ac35d101c9135@mainnet-relay.securerpc.com'},
    {'name': 'Ultra Sound', 'url': 'https://0xa1559ace749633b997cb3fdacffb890aeebdb0f5a3b6aaa7eeeaf1a38af0a8fe88b9e4b1f61f236d2e64d95733327a62@relay.ultrasound.money'}
]

mainnet_relay_names = [option['name'] for option in mainnet_relay_options]
mainnet_relay_names_sentence = ', '.join(mainnet_relay_names)

goerli_relay_options = [
    {'name': 'Flashbots', 'url': 'https://0xafa4c6985aa049fb79dd37010438cfebeb0f2bd42b115b89dd678dab0670c1de38da0c4e9138c9290a398ecd9a0b3110@builder-relay-goerli.flashbots.net'},
    {'name': 'bloXroute', 'url': 'https://0x821f2a65afb70e7f2e820a925a9b4c80a159620582c1766b1b09729fec178b11ea22abb3a51f07b288be815a1a2ff516@bloxroute.max-profit.builder.goerli.blxrbdn.com'},
    {'name': 'Blocknative', 'url': 'https://0x8f7b17a74569b7a57e9bdafd2e159380759f5dc3ccbd4bf600414147e8c4e1dc6ebada83c0139ac15850eb6c975e82d0@builder-relay-goerli.blocknative.com'},
    {'name': 'Eden Network', 'url': 'https://0xb1d229d9c21298a87846c7022ebeef277dfc321fe674fa45312e20b5b6c400bfde9383f801848d7837ed5fc449083a12@relay-goerli.edennetwork.io'},
    {'name': 'Manifold', 'url': 'https://0x8a72a5ec3e2909fff931c8b42c9e0e6c6e660ac48a98016777fc63a73316b3ffb5c622495106277f8dbcc17a06e92ca3@goerli-relay.securerpc.com/'},
    {'name': 'Aestus', 'url': 'https://0xab78bf8c781c58078c3beb5710c57940874dd96aef2835e7742c866b4c7c0406754376c2c8285a36c630346aa5c5f833@goerli.aestus.live'},
    {'name': 'Ultra Sound', 'url': 'https://0xb1559beef7b5ba3127485bbbb090362d9f497ba64e177ee2c8e7db74746306efad687f2cf8574e38d70067d40ef136dc@relay-stag.ultrasound.money'}
]

sepolia_relay_options = [
    {'name': 'Flashbots', 'url': 'https://0x845bd072b7cd566f02faeb0a4033ce9399e42839ced64e8b2adcfc859ed1e8e1a5a293336a49feac6d9a5edb779be53a@boost-relay-sepolia.flashbots.net'}
]

############################################################
# Checkpoint_sync
checkpoint_sync = "on"

def get_random_sync_url(sync_urls):
    selected_sync_url = random.choice(sync_urls)
    return selected_sync_url[1]

if checkpoint_sync.lower() == "on" and consensus_client_install in ['lighthouse', 'teku', 'prysm']:
    mainnet_sync_urls = [
        ("ETHSTAKER", "https://beaconstate.ethstaker.cc"),
        ("BEACONCHA.IN", "https://sync-mainnet.beaconcha.in"),
        ("ATTESTANT", "https://mainnet-checkpoint-sync.attestant.io"),
        ("SIGMA PRIME", "https://mainnet.checkpoint.sigp.io"),
    ]

    goerli_sync_urls = [
        ("ETHSTAKER", "https://goerli.beaconstate.ethstaker.cc/"),
        ("BEACONSTATE", "https://goerli.beaconstate.info/"),
        ("EF DevOps", "https://checkpoint-sync.goerli.ethpandaops.io/"),
        ("LodeStart", "https://beaconstate-goerli.chainsafe.io/"),
    ]

    sepolia_sync_urls = [
        ("Beaconstate", "https://sepolia.beaconstate.info/"),
        ("LodeStart", "https://beaconstate-sepolia.chainsafe.io/"),
    ]

    if eth_network == "mainnet":
        checkpoint_sync_url = get_random_sync_url(mainnet_sync_urls)
    elif eth_network == "goerli":
        checkpoint_sync_url = get_random_sync_url(goerli_sync_urls)
    elif eth_network == "sepolia":
        checkpoint_sync_url = get_random_sync_url(sepolia_sync_urls)
else:
    checkpoint_sync_url = None

print("Checkpoint Sync URL:", checkpoint_sync_url)

sync_url = checkpoint_sync_url

if 'sync_url' not in locals() or sync_url is None:
    sync_url = None
##############################################


##### DELETE OLD CLIENTS #####

# Removal commands for Execution clients
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

# Removal commands for Consensus clients
teku_cmds = [
    "sudo rm -rf /usr/local/bin/teku",
    "sudo rm -rf /var/lib/teku",
    "sudo rm -rf /etc/systemd/system/teku.service",
    "sudo userdel -r teku || true",
]

nimbus_cmds = [
    "sudo rm -rf /usr/local/bin/nimbus_beacon_node",
    "sudo rm -rf /var/lib/nimbus",
    "sudo rm -rf /etc/systemd/system/nimbus.service",
    "sudo userdel -r nimbus || true",
]

prysm_cmds = [
    "sudo rm -rf /usr/local/bin/beacon-chain",
    "sudo rm -rf /usr/local/bin/validator",
    "sudo rm -rf /var/lib/prysm",
    "sudo rm -rf /etc/systemd/system/prysm.service",
    "sudo userdel -r prysm || true",
]

lighthouse_cmds = [
    "sudo rm -rf /usr/local/bin/lighthouse",
    "sudo rm -rf /var/lib/lighthouse",
    "sudo rm -rf /etc/systemd/system/lighthouse.service",
    "sudo userdel -r lighthouse || true",
]


# Delete Old Execution Client
if execution_client_delete == 'geth':
    for cmd in geth_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'besu':
    for cmd in besu_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'nethermind':
    for cmd in nethermind_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif execution_client_delete == 'none':
    print("No client selected for deletion")

# Delete old Consensus Client
if consensus_client_delete == 'teku':
    for cmd in teku_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif consensus_client_delete == 'nimbus':
    for cmd in nimbus_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif consensus_client_delete == 'prysm':
    for cmd in prysm_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif consensus_client_delete == 'lighthouse':
    for cmd in lighthouse_cmds:
        print(cmd)
        subprocess.run(cmd, shell=True, check=False)

elif consensus_client_delete == 'none':
    print("No client selected for deletion")

# Install ufw
subprocess.run(['sudo', 'apt', 'install', 'ufw'])

# Set default policies
subprocess.run(['sudo', 'ufw', 'default', 'deny', 'incoming'])
subprocess.run(['sudo', 'ufw', 'default', 'allow', 'outgoing'])

# Allow specific ports
subprocess.run(['sudo', 'ufw', 'allow', '6673/tcp'])
subprocess.run(['sudo', 'ufw', 'allow', '30303'])
subprocess.run(['sudo', 'ufw', 'allow', '9000'])

# Enable and check status
subprocess.run(['sudo', 'ufw', 'enable'])
subprocess.run(['sudo', 'ufw', 'status', 'numbered'])

# Create JWT directory
subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/jwtsecret'])

# Generate random hex string and save to file
rand_hex = subprocess.run(['openssl', 'rand', '-hex', '32'], stdout=subprocess.PIPE)
subprocess.run(['sudo', 'tee', '/var/lib/jwtsecret/jwt.hex'], input=rand_hex.stdout, stdout=subprocess.DEVNULL)

# Update and upgrade packages
subprocess.run(['sudo', 'apt', '-y', 'update'])
subprocess.run(['sudo', 'apt', '-y', 'upgrade'])

# Dist-upgrade and autoremove packages
subprocess.run(['sudo', 'apt', '-y', 'dist-upgrade'])
subprocess.run(['sudo', 'apt', '-y', 'autoremove'])

# Install New Execution Client
print(f"\nInstalling Execution client: {execution_client_install.upper()}\n")
print("Creating usernames, directories, and service files...\n")

execution_client_install = execution_client_install.lower()

############ GETH INSTALL##################
if execution_client_install == 'geth':
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
if execution_client_install == 'besu':
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
if execution_client_install == 'nethermind':
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

    # chown nethermind:nethermind /usr/local/bin/nethermind/nethermind
    subprocess.run(["sudo", "chown", "nethermind:nethermind", "/usr/local/bin/nethermind/nethermind"])

    # chmod a+x /usr/local/bin/nethermind/nethermind
    subprocess.run(["sudo", "chmod", "a+x", "/usr/local/bin/nethermind/nethermind"])

    # Remove the temporary zip file
    os.remove(temp_path)

    nethermind_version = os.path.splitext(zip_filename)[0]    
 
# Install New Consensus Client
print(f"\nInstalling consensus client: {consensus_client_install.upper()}\n")
print(f"Creating usernames, directories, and service files...\n")

consensus_client_install = consensus_client_install.lower()

#### TEKU INSTALL #####
if consensus_client_install == 'teku':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'teku'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/teku'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/teku/validator_keys'])

    # Change to the home folder
    os.chdir(os.path.expanduser("~"))

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/ConsenSys/teku/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Get the latest release tag
    latest_version = response.json()['tag_name']

    # Define the download URL for the latest release
    download_url = f"https://artifacts.consensys.net/public/teku/raw/names/teku.tar.gz/versions/{latest_version}/teku-{latest_version}.tar.gz"
    teku_version = latest_version
    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to the home folder
    with open('teku.tar.gz', 'wb') as f:
        f.write(response.content)

    # Extract the binary to the home folder
    with tarfile.open('teku.tar.gz', 'r:gz') as tar:
        tar.extractall()

    # Copy the binary folder to /usr/local/bin using sudo
    os.system(f"sudo cp -r teku-{latest_version} /usr/local/bin/teku")

    # Remove the teku.tar.gz file and extracted binary folder
    os.remove('teku.tar.gz')
    shutil.rmtree(f'teku-{latest_version}')

    print("Teku binary installed successfully!")
    print(f"Download URL: {download_url}")
    
    ### IMPORT KEYSTORE ####

    # Check if temp_keystore_dir exists, then get the .json files
    json_files_in_source = [f for f in os.listdir(temp_keystore_dir)] if os.path.exists(temp_keystore_dir) else []

    json_files_in_source = [f for f in json_files_in_source if f.endswith('.json')]

    if len(json_files_in_source) > 0:  # Ensure source directory is not empty
        # Check if the teku validator_keys directory exists, otherwise create it
        validator_keys_dir = '/var/lib/teku/validator_keys'
        if not os.path.exists(validator_keys_dir):
            subprocess.run(['sudo', 'mkdir', '-p', validator_keys_dir])

        for json_file in json_files_in_source:
            source_path = os.path.join(temp_keystore_dir, json_file)
            dest_path = os.path.join(validator_keys_dir, json_file)
            
            if os.path.exists(dest_path):
                print(f"Ignoring keystore {json_file} as it already exists.")
            else:
                subprocess.run(['sudo', 'cp', source_path, dest_path])
                print(f"Successfully imported keystore {json_file}.")
        
        teku_keystore_dir = '/var/lib/teku/validator_keys'
        
        def get_and_store_password(json_file):
            txt_file_name = os.path.splitext(json_file)[0] + '.txt'
            txt_file_path = os.path.join(teku_keystore_dir, txt_file_name)
            
            # Prompt for the password and store it directly in a bytearray
            teku_pass = bytearray(getpass.getpass(prompt=f'Please enter password for {json_file}: '), 'utf-8')
            
            # Use a temporary file for writing the password.txt file
            temp_file_name = 'temp_password_file.txt'
            with open(temp_file_name, 'wb') as f:
                os.write(f.fileno(), teku_pass)
            
            # Use sudo to move the temp file to the actual desired location
            subprocess.run(['sudo', 'mv', temp_file_name, txt_file_path])
            
            # Modify permissions of the text file so it's not readable by others
            subprocess.run(['sudo', 'chmod', '600', txt_file_path])
            
            # Overwrite the password in memory with zero bytes
            for i in range(len(teku_pass)):
                teku_pass[i] = 0

        # List all files ending with .json in the teku keystore directory
        json_files = [f for f in os.listdir(teku_keystore_dir) if f.endswith('.json')]

        # For each json file, prompt for password and create a corresponding txt file
        for json_file in json_files:
            get_and_store_password(json_file)
    
    # Change ownership
    subprocess.run(['sudo', 'chown', '-R', 'teku:teku', '/var/lib/teku'])

################# PRYSM INSTALL #################
if consensus_client_install == 'prysm':
    # Create prysmbeacon user
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'prysmbeacon'])

    # Create and set ownership for /var/lib/prysm/beacon directory
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/prysm/beacon'])
    subprocess.run(['sudo', 'chown', '-R', 'prysmbeacon:prysmbeacon', '/var/lib/prysm/beacon'])

    # Create prysmvalidator user
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'prysmvalidator'])

    # Create /var/lib/prysm/validator directory
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/prysm/validator'])

    base_url = "https://api.github.com/repos/prysmaticlabs/prysm/releases/latest"
    response = requests.get(base_url)
    response_json = response.json()
    download_links = []

    for asset in response_json["assets"]:
        if re.search(r'beacon-chain-v\d+\.\d+\.\d+-linux-amd64$', asset["browser_download_url"]):
            download_links.append(asset["browser_download_url"])
        elif re.search(r'validator-v\d+\.\d+\.\d+-linux-amd64$', asset["browser_download_url"]):
            download_links.append(asset["browser_download_url"])

    if len(download_links) >= 2:
        for link in download_links[:2]:
            cmd = f"curl -LO {link}"
            os.system(cmd)

        os.system("mv beacon-chain-*-linux-amd64 beacon-chain")
        os.system("mv validator-*-linux-amd64 validator")
        os.system("chmod +x beacon-chain")
        os.system("chmod +x validator")
        os.system("sudo cp beacon-chain /usr/local/bin")
        os.system("sudo cp validator /usr/local/bin")
        os.system("rm beacon-chain && rm validator")
    else:
        print("Error: Could not find the latest release links.")

    # Check if temp_keystore_dir exists, import keys and create password .txt file
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):

        # Import validator keys
        print("Importing Validator Keystore...")
        
        subprocess.run([
            'sudo',
            '/usr/local/bin/validator',
            'accounts', 'import',
            '--keys-dir', temp_keystore_dir,
            '--wallet-dir', '/var/lib/prysm/validator',
            '--mainnet'
        ])
        
        def get_and_store_password():
            # Prompt for the password and store it directly in a bytearray
            prysm_pass = bytearray(getpass.getpass(prompt='Please enter your Prysm wallet password: '), 'utf-8')
            
            prysm_pass_temp_file = 'password_temp.txt'
            prysm_pass_path = '/var/lib/prysm/validator/password.txt'
            
            # Write the password to the temp file directly from the bytearray
            with open(prysm_pass_temp_file, 'wb') as f:
                os.write(f.fileno(), prysm_pass)

            # Use sudo to move the temp file to the actual desired location
            subprocess.run(['sudo', 'mv', prysm_pass_temp_file, prysm_pass_path])

            # Modify permissions of the text file so it's not readable by others
            subprocess.run(['sudo', 'chmod', '600', prysm_pass_path])
            
            # Overwrite the password in memory with zero bytes to erase it
            for i in range(len(prysm_pass)):
                prysm_pass[i] = 0

        get_and_store_password()
        
    # Set ownership of prysmvalidator
    subprocess.run(['sudo', 'chown', '-R', 'prysmvalidator:prysmvalidator', '/var/lib/prysm/validator'])    
    
################ NIMBUS INSTALL ##################
if consensus_client_install == 'nimbus':
    # Create /var/lib/nimbus directory
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/nimbus'])
    
    # Change Ownership
    subprocess.run(['sudo', 'chmod', '700', '/var/lib/nimbus'])
    
    # Create nimbus user
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'nimbus'])

    # Change to the home folder
    os.chdir(os.path.expanduser("~"))

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/status-im/nimbus-eth2/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Search for the asset with the name that ends in _Linux_amd64.tar.gz
    assets = response.json()['assets']
    download_url = None
    for asset in assets:
        if '_Linux_amd64' in asset['name'] and asset['name'].endswith('.tar.gz'):
            download_url = asset['browser_download_url']
            break

    if download_url is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to the home folder
    with open('nimbus.tar.gz', 'wb') as f:
        f.write(response.content)

    # Extract the binary to the home folder
    with tarfile.open('nimbus.tar.gz', 'r:gz') as tar:
        tar.extractall()

    # Find the extracted folder
    extracted_folder = None
    for item in os.listdir():
        if item.startswith("nimbus-eth2_Linux_amd64"):
            extracted_folder = item
            break

    if extracted_folder is None:
        print("Error: Could not find the extracted folder.")
        exit(1)

    # Copy the binary to /usr/local/bin using sudo
    os.system(f"sudo cp {extracted_folder}/build/nimbus_beacon_node /usr/local/bin")

    # Remove the nimbus.tar.gz file and extracted folder
    os.remove('nimbus.tar.gz')
    os.system(f"rm -r {extracted_folder}")

    print("Nimbus binary installed successfully!")
    print(f"Download URL: {download_url}")

    # Check if the temp_keystore_dir exists and is not empty
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):

        # Import Validator keystore
        subprocess.run([
            'sudo',
            '/usr/local/bin/nimbus_beacon_node',
            'deposits', 'import',
            '--data-dir=/var/lib/nimbus',
            temp_keystore_dir
        ])
            
    # Set ownership for /var/lib/nimbus directory
    subprocess.run(['sudo', 'chown', '-R', 'nimbus:nimbus', '/var/lib/nimbus'])

############ LIGHTHOUSE INSTALL ##################
if consensus_client_install == 'lighthouse':
    # Create User and directories
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'lighthousebeacon'])
    subprocess.run(['sudo', 'useradd', '--no-create-home', '--shell', '/bin/false', 'lighthousevalidator'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse/beacon'])
    subprocess.run(['sudo', 'mkdir', '-p', '/var/lib/lighthouse/validators'])
    subprocess.run(['sudo', 'chown', '-R', 'lighthousebeacon:lighthousebeacon', '/var/lib/lighthouse/beacon'])

    # Change to the home folder
    os.chdir(os.path.expanduser("~"))

    # Define the Github API endpoint to get the latest release
    url = 'https://api.github.com/repos/sigp/lighthouse/releases/latest'

    # Send a GET request to the API endpoint
    response = requests.get(url)

    # Search for the asset with the name that ends in x86_64-unknown-linux-gnu.tar.gz
    assets = response.json()['assets']
    download_url = None
    for asset in assets:
        if asset['name'].endswith('x86_64-unknown-linux-gnu.tar.gz'):
            download_url = asset['browser_download_url']
            break

    if download_url is None:
        print("Error: Could not find the download URL for the latest release.")
        exit(1)

    # Download the latest release binary
    response = requests.get(download_url)

    # Save the binary to the home folder
    with open('lighthouse.tar.gz', 'wb') as f:
        f.write(response.content)

    # Extract the binary to the home folder
    with tarfile.open('lighthouse.tar.gz', 'r:gz') as tar:
        tar.extractall()

    # Copy the binary to /usr/local/bin using sudo
    os.system("sudo cp lighthouse /usr/local/bin")

    # Remove the lighthouse.tar.gz file and extracted binary
    os.remove('lighthouse.tar.gz')
    os.remove('lighthouse')

    print("Lighthouse binary installed successfully!")
    print(f"Download URL: {download_url}")

    # Check if the temp_keystore_dir exists and is not empty, then import
    if os.path.exists(temp_keystore_dir) and os.listdir(temp_keystore_dir):

        # Lighthouse Import Keystore
        print("Importing Validator Keystore...")

        subprocess.run([
            'sudo', 
            '/usr/local/bin/lighthouse', 
            '--network', 'mainnet', 
            'account', 'validator', 'import', 
            '--directory', temp_keystore_dir, 
            '--datadir', '/var/lib/lighthouse'
        ])
    
    # Change ownership of validator directory
    subprocess.run(['sudo', 'chown', '-R', 'lighthousevalidator:lighthousevalidator', '/var/lib/lighthouse/validators'])


###### GETH SERVICE FILE #############
if execution_client_install == 'geth':
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
if execution_client_install == 'besu':
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
if execution_client_install == 'nethermind':
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
        'ExecStart=/usr/local/bin/nethermind/nethermind \\',
        f'    --config {eth_network} \\',
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

###### TEKU SERVICE FILE #######
if consensus_client_install == 'teku':
    teku_service_file_lines = [
        '[Unit]',
        'Description=Teku Consensus Client (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=teku',
        'Group=teku',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'Environment="JAVA_OPTS=-Xmx5g"',
        'Environment="TEKU_OPTS=-XX:-HeapDumpOnOutOfMemoryError"',
        'ExecStart=/usr/local/bin/teku/bin/teku \\',
        f'    --network={eth_network} \\',
        '    --data-path=/var/lib/teku \\',
        '    --validator-keys=/var/lib/teku/validator_keys:/var/lib/teku/validator_keys \\',
        '    --ee-endpoint=http://127.0.0.1:8551 \\',
        '    --ee-jwt-secret-file=/var/lib/jwtsecret/jwt.hex \\',
        *([f'    --initial-state={sync_url} \\'] if sync_url is not None else []),
        *([f'    --validators-builder-registration-default-enabled=true \\'] if mev_on_off == 'on' else []),
        *([f'    --builder-endpoint=http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        f'    --validators-proposer-default-fee-recipient={fee_address}',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    teku_service_file = '\n'.join(teku_service_file_lines)

    teku_temp_file = 'teku_temp.service'
    teku_service_file_path = '/etc/systemd/system/teku.service'

    with open(teku_temp_file, 'w') as f:
        f.write(teku_service_file)

    os.system(f'sudo cp {teku_temp_file} {teku_service_file_path}')
    os.remove(teku_temp_file)

########### NIMBUS SERVICE FILE #############
if consensus_client_install == 'nimbus':
    nimbus_service_file_lines = [
        '[Unit]',
        'Description=Nimbus Consensus Client (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=nimbus',
        'Group=nimbus',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/nimbus_beacon_node \\',
        f'    --network={eth_network} \\',
        '    --data-dir=/var/lib/nimbus \\',
        '    --web3-url=http://127.0.0.1:8551 \\',
        '    --jwt-secret=/var/lib/jwtsecret/jwt.hex \\',
        *([f'    --payload-builder=true \\'] if mev_on_off == 'on' else []),
        *([f'    --payload-builder-url=http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        f'    --suggested-fee-recipient={fee_address}',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    nimbus_service_file = '\n'.join(nimbus_service_file_lines)

    nimbus_temp_file = 'nimbus_temp.service'
    nimbus_service_file_path = '/etc/systemd/system/nimbus.service'

    with open(nimbus_temp_file, 'w') as f:
        f.write(nimbus_service_file)

    os.system(f'sudo cp {nimbus_temp_file} {nimbus_service_file_path}')
    os.remove(nimbus_temp_file)

########### PRYSM SERVICE FILE ##############
if consensus_client_install == 'prysm':
    prysm_beacon_service_file_lines = [
        '[Unit]',
        'Description=Prysm Consensus Client BN (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=prysmbeacon',
        'Group=prysmbeacon',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/beacon-chain \\',
        f'    --{eth_network} \\',
        '    --datadir=/var/lib/prysm/beacon \\',
        '    --execution-endpoint=http://127.0.0.1:8551 \\',
        '    --jwt-secret=/var/lib/jwtsecret/jwt.hex \\',
        f'    --suggested-fee-recipient={fee_address} \\',
        *([f'    --checkpoint-sync-url={sync_url} \\'] if sync_url is not None else []),
        *([f'    --genesis-beacon-api-url={sync_url} \\'] if sync_url is not None else []),
        *([f'    --http-mev-relay=http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        '    --accept-terms-of-use',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    prysm_beacon_service_file = '\n'.join(prysm_beacon_service_file_lines)

    prysm_validator_service_file_lines = [
        '[Unit]',
        'Description=Prysm Consensus Client VC (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=prysmvalidator',
        'Group=prysmvalidator',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/validator \\',
        '    --datadir=/var/lib/prysm/validator \\',
        '    --wallet-dir=/var/lib/prysm/validator \\',
        '    --wallet-password-file=/var/lib/prysm/validator/password.txt \\',
        f'    --suggested-fee-recipient={fee_address} \\',
        *([f'    --enable-builder \\'] if mev_on_off == 'on' else []),
        '    --accept-terms-of-use',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    prysm_validator_service_file = '\n'.join(prysm_validator_service_file_lines)

    prysm_beacon_temp_file = 'prysm_beacon_temp.service'
    prysm_beacon_service_file_path = '/etc/systemd/system/prysmbeacon.service'
    prysm_validator_temp_file = 'prysm_validator_temp.service'
    prysm_validator_service_file_path = '/etc/systemd/system/prysmvalidator.service'

    with open(prysm_beacon_temp_file, 'w') as f:
        f.write(prysm_beacon_service_file)

    with open(prysm_validator_temp_file, 'w') as f:
        f.write(prysm_validator_service_file)

    os.system(f'sudo cp {prysm_beacon_temp_file} {prysm_beacon_service_file_path}')
    os.remove(prysm_beacon_temp_file)
    os.system(f'sudo cp {prysm_validator_temp_file} {prysm_validator_service_file_path}')
    os.remove(prysm_validator_temp_file)

######## LIGHTHOUSE SERVICE FILES ###########
if consensus_client_install == 'lighthouse':
# Beacon Service File
    lh_beacon_service_file_lines = [
        '[Unit]',
        'Description=Lighthouse Consensus Client BN (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=lighthousebeacon',
        'Group=lighthousebeacon',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/lighthouse bn \\',
        f'    --network {eth_network} \\',
        '    --datadir /var/lib/lighthouse \\',
        '    --http \\',
        '    --execution-endpoint http://127.0.0.1:8551 \\',
        '    --execution-jwt /var/lib/jwtsecret/jwt.hex \\',
        *([f'    --checkpoint-sync-url {sync_url} \\'] if sync_url is not None else []),
        *([f'    --builder http://127.0.0.1:18550 \\'] if mev_on_off == 'on' else []),
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    lh_beacon_service_file = '\n'.join(lh_beacon_service_file_lines)

# Validator Service FIle
    lh_validator_service_file_lines = [
        '[Unit]',
        'Description=Lighthouse Consensus Client VC (Mainnet)',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=lighthousevalidator',
        'Group=lighthousevalidator',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/lighthouse vc \\',
        f'    --network {eth_network} \\',
        '    --datadir /var/lib/lighthouse \\',
        *([f'    --builder-proposals \\'] if mev_on_off == 'on' else []),
        f'    --suggested-fee-recipient {fee_address}',
        '',
        '[Install]',
        'WantedBy=multi-user.target',
    ]

    lh_validator_service_file = '\n'.join(lh_validator_service_file_lines)

# Write Service files
    lh_beacon_temp_file = 'lh_beacon_temp.service'
    lh_validator_temp_file = 'lh_validator_temp.service'
    lh_beacon_service_file_path = '/etc/systemd/system/lighthousebeacon.service'
    lh_validator_service_file_path = '/etc/systemd/system/lighthousevalidator.service'

    with open(lh_beacon_temp_file, 'w') as f:
	    f.write(lh_beacon_service_file)

    with open(lh_validator_temp_file, 'w') as f:
	    f.write(lh_validator_service_file)

    os.system(f'sudo cp {lh_beacon_temp_file} {lh_beacon_service_file_path}')
    os.system(f'sudo cp {lh_validator_temp_file} {lh_validator_service_file_path}')
    os.remove(lh_beacon_temp_file)
    os.remove(lh_validator_temp_file)

# MEV Boost Service File
if mev_install == 'yes':
    mev_boost_service_file_lines = [
        '[Unit]',
        'Description=mev-boost ethereum mainnet',
        'Wants=network-online.target',
        'After=network-online.target',
        '',
        '[Service]',
        'User=mevboost',
        'Group=mevboost',
        'Type=simple',
        'Restart=always',
        'RestartSec=5',
        'ExecStart=/usr/local/bin/mev-boost \\',
        f'    -{eth_network} \\',
        '    -min-bid 0.05 \\',
        '    -relay-check \\',
    ]

    # Add relay lines from relay_options
    
    if eth_network == 'mainnet':
        for relay in mainnet_relay_options:
            relay_line = f'    -relay {relay["url"]} \\'
            mev_boost_service_file_lines.append(relay_line)

        # Remove the trailing '\\' from the last relay line
        mev_boost_service_file_lines[-1] = mev_boost_service_file_lines[-1].rstrip(' \\')

        mev_boost_service_file_lines.extend([
            '',
            '[Install]',
            'WantedBy=multi-user.target',
    ])
    elif eth_network == 'goerli':
        for relay in goerli_relay_options:
            relay_line = f'    -relay {relay["url"]} \\'
            mev_boost_service_file_lines.append(relay_line)

        # Remove the trailing '\\' from the last relay line
        mev_boost_service_file_lines[-1] = mev_boost_service_file_lines[-1].rstrip(' \\')

        mev_boost_service_file_lines.extend([
            '',
            '[Install]',
            'WantedBy=multi-user.target',
    ])
    else:
        for relay in sepolia_relay_options:
            relay_line = f'    -relay {relay["url"]} \\'
            mev_boost_service_file_lines.append(relay_line)

        # Remove the trailing '\\' from the last relay line
        mev_boost_service_file_lines[-1] = mev_boost_service_file_lines[-1].rstrip(' \\')

        mev_boost_service_file_lines.extend([
            '',
            '[Install]',
            'WantedBy=multi-user.target',
    ])
    

    mev_boost_service_file = '\n'.join(mev_boost_service_file_lines)

    mev_boost_temp_file = 'mev_boost_temp.service'
    mev_boost_service_file_path = '/etc/systemd/system/mevboost.service'

    with open(mev_boost_temp_file, 'w') as f:
        f.write(mev_boost_service_file)

    os.system(f'sudo cp {mev_boost_temp_file} {mev_boost_service_file_path}')
    os.remove(mev_boost_temp_file)

# Reload the systemd daemon
subprocess.run(['sudo', 'systemctl', 'daemon-reload'])

# Delete temp keystore files
validator_keys_temp = os.path.join(os.environ["HOME"], 'validator_keys_temp')
subprocess.run(['sudo', 'rm', '-rf', validator_keys_temp])

# Print the final output
inbound_ports = subprocess.run(["sudo", "ufw", "status", "numbered"], stdout=subprocess.PIPE).stdout
if inbound_ports is not None:
    inbound_ports = inbound_ports.decode()
else:
    inbound_ports = ""
print(f'\nFirewall Status:\nInbound Ports: {inbound_ports}Outbound Ports: 9000, 30303, 6673/tcp\n')


print(f'Network: {eth_network.capitalize()}')

if consensus_client_install in ['lighthouse', 'teku', 'prysm', 'nimbus']:
    print(f'CheckPointSyncURL: {sync_url}')

print(f'MEV Boost: {mev_on_off.upper()}')

print(f'Validator Fee Address: {fee_address}\n')

print(f'Removed: {execution_client_delete.upper()} and {consensus_client_delete.upper()}\n')

# Installation Print
print(f'Installed: {execution_client_install.upper()} and {consensus_client_install.upper()}\n') 

# Print Geth
if execution_client_install == 'geth':
    geth_version = subprocess.run(["geth", "--version"], stdout=subprocess.PIPE).stdout
    if geth_version is not None:
        geth_version = geth_version.decode()
        geth_version = geth_version.split(" ")[-1]
    else:
        geth_version = ""
    print(f'Geth Version: v{geth_version}')

# Print Besu
if execution_client_install == 'besu':
    print(f'Besu Version: {besu_version}\n')

# Print Nethermind
if execution_client_install == 'nethermind':
    print(f'Nethermind Version: {nethermind_version}\n')

# Print Teku
if consensus_client_install == 'teku':
    print(f'Teku Version: {teku_version}\n')

# Print Nimbus
if consensus_client_install == 'nimbus':
    # Check version and capture output
    nimbus_version_output = subprocess.run(["nimbus_beacon_node", "--version"], stdout=subprocess.PIPE).stdout

    if nimbus_version_output is not None:
        # Decode output and use regex to extract the version number
        nimbus_version_output = nimbus_version_output.decode()
        match = re.search(r'v(\d+\.\d+\.\d+)', nimbus_version_output)

        if match:
            nimbus_version = match.group(1)
            print(f'Nimbus Version: {nimbus_version}\n')
        else:
            print("Error: Unable to extract Nimbus version.")
    else:
        print("Error: Command execution returned no output.")

# Print Prysm
if consensus_client_install == 'prysm':
    prysm_version = subprocess.run(["beacon-chain", "--version"], stdout=subprocess.PIPE).stdout
    if prysm_version is not None:
        prysm_version = prysm_version.decode().splitlines()[0]
        prysm_version = prysm_version.split("/")[-2]
    else:
        prysm_version = ""
    print(f'Prysm Version: {prysm_version}\n')

# Print Lighthouse
if consensus_client_install == 'lighthouse':
    lighthouse_version = subprocess.run(["lighthouse", "-V"], stdout=subprocess.PIPE).stdout
    if lighthouse_version is not None:
        lighthouse_version = lighthouse_version.decode()
    else:
        lighthouse_version = ""
    print(f'Lighthouse Version: {lighthouse_version}')

print(f"Client switch was successful! {execution_client_install.upper()} and {consensus_client_install.upper()} are ready to sync!\n")

# Final Check how many clients are installed


# List of execution and consensus clients
ethereum_clients = ["geth", "nethermind", "besu", "nimbus", "teku", "prysm", "lighthouse"]

# Path to the directory where clients are installed
base_directory = "/var/lib/"

# Count of existing directories for all clients
existing_directories = []

# Check if directories for execution and consensus clients exist
for client in ethereum_clients:
    client_directory = os.path.join(base_directory, client)
    if os.path.exists(client_directory):
        existing_directories.append(client)

# Check if more than 2 clients (execution and/or consensus) exist
if len(existing_directories) > 2:
    print("###################   WARNING   ###############\nWARNING: You currently have more than 2 Ethereum clients installed.")
    print("This may lead to issues such as slashing in a validator setup.")
    print("Installed clients:")
    for client in existing_directories:
        print(f"- {client.capitalize()}")

