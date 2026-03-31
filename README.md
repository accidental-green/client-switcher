# Ethereum Client Switcher

Ethereum client switcher allows validators to easily switch their execution client (Geth, Besu, Nethermind) with a single click.

The code is open source and available for both CLI (terminal) and GUI to accommodate various setups and preferences.

## Instructions:

To begin installation, paste the following commands into the terminal:

**Install updates and packages:**

`sudo apt-get update && sudo apt-get install git curl python3-pip python3-tk -y && sudo pip install requests customtkinter`

**Clone the client-switcher repo:**

`git clone https://github.com/agco-1/client-switcher.git && cd client-switcher`

### Run Client Switcher:

**Note**: Choose either GUI (popup window) or CLI (in terminal)

**GUI — Execution clients only:**

`python3 client_switcher_gui.py`

**GUI — Execution + Consensus clients, MEV Boost, Validator settings:**

`python3 client_switcher_max.py`

**CLI:**

`python3 client_switcher_cli.py`

### Installation Screen:
Select the Ethereum network, client to delete, client to install, then click "Install".

The script will delete all old client data, install the new client, and create service files, usernames, directories etc

Once installation has finished, you can start the new client and begin syncing.

This project has not been audited yet, but working to make that happen soon.

**Other Ethereum related repos:**

[Validator Install](https://github.com/agco-1/validator-install): Fresh Ubuntu to syncing validator in minutes

[Validator Updater](https://github.com/agco-1/validator-updater): Instantly update clients (Execution, Consensus, and Mevboost)

[Validator Controller](https://github.com/agco-1/validator-controller): Easily control the validator with a single click (start, stop, journals, service files)
