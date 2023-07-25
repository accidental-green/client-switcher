# Ethereum Client Switcher

Open source Ethereum client switcher to help people instantly switch their execution client (Geth, Besu, Nethermind)

To run the program, use the following commands:

`sudo apt-get update && sudo apt-get install git curl -y && sudo pip install requests`

`git clone https://github.com/accidental-green/client-switcher.git`

`python3 client-switcher/client-switcher.py`


The program will ask a few simple questions:

![Screenshot from 2023-07-24 19-58-15](https://github.com/accidental-green/client-switcher/assets/72235883/14d2f92d-7cde-4382-8d4e-100f6a6f0d87)


That's it! The script will delete the old client info (username, database, etc) and install the new client with the necessary usernames, directories, permissions, and service files.

Sucessful Install:

![Screenshot from 2023-07-24 19-59-56](https://github.com/accidental-green/client-switcher/assets/72235883/48fdeb1a-fbcc-4750-8045-50088f94f6d5)

NOTE: This does NOT affect anything with validator keys or Concensus Client (Lighthouse, Prysm, Teku, Nimbus).

Once everything is installed, you can start the new Execution client and begin syncing. Depending on hardware/internet, it can take 24-48 hours for a full validator to sync from scratch. You can check progress in the journals.

Once everything is synced, the validator should start attesting again.

This can also be used if you have a corrupted database (ex remove/reinstall BESU).

If you're starting from scratch on Ubuntu, you can use my other project [Instant Validators](https://github.com/accidental-green/validator-install) to do a full install in minutes.

Suggestions and feedback always welcome. Still in testing, not for mainnet (yet).
