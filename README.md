# Ethereum Client Switcher

Easily switch your Ethereum Validator client in a single click! This tool allows node operators to easily switch from Geth to Besu in a single click (more clients coming soon)

The script will delete the old Geth data (username, database, etc) and install Besu with the necessary usernames, directories, permissions, and service files.

To run the program, use the following commands:

`sudo apt-get update && sudo apt-get install git curl -y && sudo pip install requests`

`git clone https://github.com/accidental-green/client-switcher.git`

`python3 client-switcher/client_switcher.py`


The program will ask a few simple questions:

1) Execution Client to DELETE? (Geth, Besu, Nethermind, Reth, None)

2) Execution Client to INSTALL? (Geth, Besu, Nethermind, Reth, None)

3) Select an Ethereum Network? (Mainnet, Goerli, Sepolia)

That's it! Just 3 simple answers and 

NOTE: This does NOT affect anything with validator keys or Concensus Client (Lighthouse, Prysm, Teku, Nimbus).

Once everything is installed, the script will restart all service files and everything should begin syncying. Depending on hardware/internet, it can take ~24 hours for a full validator to sync from scratch. You can check progress in the journals.

Once everything is synced, the validator should start attesting again. Same Same, but with a new Execution Client.

This can also be used if you have a corrupted database (ex delete/reinstall GETH).

If you're starting from scratch on Ubuntu, you can use my other project Instant Validator to do a full install in minutes.

These are mostly "weekend projects", but I'd like to dedicate more time to these things if people find them useful. 

Any testing or feedback is greatly appreciated.

Cheers and Happy Staking!
