# Ethereum Client Switcher

Client switcher is an open source tool that allows validators to instantly switch their entire setup (ec, cc, mev, keystore) in a single click.

#### Important Note:
This code has NOT been audited and could potentially do system wide irreparable damage. The script is programed to delete important data including validator keystores and blockchain databases. This cannot be undone.

If you choose to import a keystore, it's possible an error in this code causes your validator to get slashed.

Still in testing, please ensure you have all validator_keystore backups before running this **experimental** open source software.

## Client Switcher Features:

- **Execution, Consensus, and MEV Clients**: Supports Geth, Besu, Nethermind, Teku, Nimbus, Lighthouse, Prysm, and Mevboost.
- **Import Validator Keystores**: Seamlessly import existing keystores to jump-start your validator setup.
- **Standard Configuration**: Get the same results as manually following Somer's guides (service files, users, directories, etc.)
- **GUI & CLI Versions**: Choose the version that suits your comfort level and setup.


### CLIENT SWITCHER:
![Screenshot from 2024-01-21 22-57-32](https://github.com/accidental-green/client-switcher/assets/72235883/b379586c-942a-4189-8b0d-e15e50393369)

## Instructions:

**Note**: If you choose to DELETE a client, you will lose all data associated with those directories including validator keystores and blockchain databases. Please be sure you have the appropriate backups before running this script.



To begin installation, paste the following commands into the terminal:

**Install updates and packages:**

`sudo apt-get update && sudo apt-get install git curl python3-pip python3-tk -y && sudo pip install requests`

**Clone the client-switcher repo:**

`git clone https://github.com/accidental-green/client-switcher.git`

**Run Client Switcher:**

Upon running this command, a pop-up window will open:


`python3 client-switcher/client_switcher_gui.py`


### Installation Screen:
Select the Ethereum network, clients to delete, clients to install, MEV settings, and Ethereum tip address.

![Screenshot from 2024-01-21 21-15-20](https://github.com/accidental-green/client-switcher/assets/72235883/3384bcad-6337-440d-ae54-9301145e4c8d)


### Validator Keystore (optional)

If you'd like to import a validator keystore, click "Import Keystore".

**Note**: The import window will open to USB by default, but you can navigate to any directory.

Locate the keystore, click open, and the button will update to indicate keystore was successfully imported.


**Install:** Once everything is ready, click "Install" and return to the original terminal window. If importing a validator keystore, you'll eventually be asked to enter the password.

### Sucessful Install Screen:

![Screenshot from 2024-01-21 21-52-32](https://github.com/accidental-green/client-switcher/assets/72235883/d23d2ff9-5c98-48a9-944d-e77e2cb361ee)


**NOTE:** To avoid slashing, be sure the old validator client has been completely deleted and cannot be started.

Once installation has finished, you can start the new clients and begin syncing. You can follow progress in the journals, but a fresh validator sync can take 24-48 hours depending on internet and hardware.

### Other Notes:

This project is still in testing, so use with caution.

The command line version (client_switcher_cli.py) is only able to switch Execution Clients.

Feel free to check out my other Ethereum related repos:

[Validator Install](https://github.com/accidental-green/validator-install): Fresh Ubunutu to syncing validator in minutes

[Validator Updater](https://github.com/accidental-green/validator-updater): Instantly update clients (Execution, Consensus, and Mevboost)

[Validator Controller](https://github.com/accidental-green/validator-controller)
: Easily control the validator with a single click (start, stop, journals, service files)
