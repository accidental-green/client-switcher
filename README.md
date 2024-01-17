# Ethereum Client Switcher

Ethereum client switcher allows validators to instantly switch their execution client (Geth, Besu, Nethermind).

The switcher assumes a "standard" installation based on [Somer Esat's Guides](https://github.com/SomerEsat/ethereum-staking-guides). but can be modified to fit any installation.

<br>
 

**CLIENT SWITCHER (GUI):**
<br>

![Screenshot from 2024-01-10 23-40-18](https://github.com/accidental-green/client-switcher/assets/72235883/ef1368a4-b164-4f21-b9c0-3accea0bcc5c)

## Client-Switcher Instructions:

Copy/paste the following commands into the terminal:

**Install updates and packages:**

`sudo apt-get update && sudo apt-get install git curl python3-pip python3-tk -y && sudo pip install requests`

**Clone the client-switcher repo:**

`git clone https://github.com/accidental-green/client-switcher.git`

**Run Client Switcher:**

`python3 client-switcher/client-switcher-gui.py`



<br>

**CLIENT SWITCHER:**
<br>

![Screenshot from 2024-01-10 23-40-18](https://github.com/accidental-green/client-switcher/assets/72235883/ef1368a4-b164-4f21-b9c0-3accea0bcc5c)

Once you make your selections and click "INSTALL", the script will delete the old client info (username, database, etc) and install the new client with the necessary usernames, directories, permissions, and service files.

**Sucessful Install Screen:**

![image](https://github.com/accidental-green/client-switcher/assets/72235883/3dc25341-56f4-4e9e-8d39-b56d72a1cdf2)


**NOTE**: This does NOT affect anything with validator keys or Concensus Client (Lighthouse, Prysm, Teku, Nimbus).

Once installation is complete, you can start the new execution client and begin syncing. Depending on hardware/internet, it can take 24-48 hours for a full validator to sync from scratch. You can check progress in the journals

Suggestions and feedback welcome. Still in testing, use with caution.

Feel free to check out my other Ethereum related repos:

[Validator Install](https://github.com/accidental-green/validator-install): Fresh Ubunutu to syncing validator in 52 seconds

[Validator Updater](https://github.com/accidental-green/validator-updater): Instantly update clients (Execution, Consensus, and Mevboost)

[Validator Controller](https://github.com/accidental-green/validator-controller)
: Easily control the validator with a single click (start, stop, journals, service files)
