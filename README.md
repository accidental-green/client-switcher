# Ethereum Client Switcher

Open source Ethereum client switcher to help people instantly switch their execution client (Geth, Besu, Nethermind)

To run the program, use the following commands:

`sudo apt-get update && sudo apt-get install git curl -y && sudo pip install requests`

`git clone https://github.com/accidental-green/client-switcher.git`

`python3 client-switcher/client-switcher.py`


The program will ask a few simple questions:

1) Select Execution Client to REMOVE? (Geth, Besu, Nethermind, None)

2) Select Execution Client to INSTALL? (Geth, Besu, Nethermind, None)

3) Select an Ethereum Network? (Mainnet, Goerli, Sepolia)

That's it! The script will delete the old client info (username, database, etc) and install the new client with the necessary usernames, directories, permissions, and service files.

NOTE: This does NOT affect anything with validator keys or Concensus Client (Lighthouse, Prysm, Teku, Nimbus).

Once everything is installed, you can start the new Execution client and begin syncing. Depending on hardware/internet, it can take ~36 hours for a full validator to sync from scratch. You can check progress in the journals.

Once everything is synced, the validator should start attesting again.

This can also be used if you have a corrupted database (ex delete/reinstall GETH).

If you're starting from scratch on Ubuntu, you can use my other project Instant Validators to do a full install in minutes.

Suggestions and feedback always welcome. Still in testing, not for mainnet.
