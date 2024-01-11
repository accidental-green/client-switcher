# Ethereum Client Switcher

Open source Ethereum client switcher to help people instantly switch their execution client (Geth, Besu, Nethermind). The switcher assumes a "standard" installation based on [Somer Esat's Guides](https://github.com/SomerEsat/ethereum-staking-guides)
.

**To switch execution clients, use the following commands:**

`sudo apt-get update && sudo apt-get install git curl python3-pip python3-tk -y && sudo pip install requests`

`git clone https://github.com/accidental-green/client-switcher.git`

`python3 client-switcher/client-switcher-gui.py`

<br>

**CLIENT SWITCHER:**
<br>

![Screenshot from 2024-01-10 23-40-18](https://github.com/accidental-green/client-switcher/assets/72235883/ef1368a4-b164-4f21-b9c0-3accea0bcc5c)

Once you make your selections and click "INSTALL", the script will delete the old client info (username, database, etc) and install the new client with the necessary usernames, directories, permissions, and service files.

**Sucessful Install Screen:**

![image](https://github.com/accidental-green/client-switcher/assets/72235883/3dc25341-56f4-4e9e-8d39-b56d72a1cdf2)


NOTE: This does NOT affect anything with validator keys or Concensus Client (Lighthouse, Prysm, Teku, Nimbus).

Once installed complete, you can start the new Execution client and begin syncing. Depending on hardware/internet, it can take 24-48 hours for a full validator to sync from scratch. You can check progress in the journals.

Once everything has synced, the validator should start attesting again.

This can also be used if you have a corrupted database (ex remove/reinstall GETH).

If you're starting from scratch on Ubuntu and want to do a full validator install, you can use [Instant Validators](https://github.com/accidental-green/validator-install) to do a full install in minutes.

Suggestions and feedback always welcome. Still in testing, use with caution.
