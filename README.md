Python Storage Organizer
Welcome to the Python Storage Organizer! This script allows you to manage items within virtual bins through a command-line interface. It supports adding, transferring, finding, and removing items with specific quantities, and it saves your data persistently in a JSON file.

Features
Add Items with Quantities: Add items to a bin, specifying quantities.
Transfer Items: Move items from one bin to another.
Remove Items: Remove items by quantity from a specific bin.
Find Items: Locate items across all bins.
List All Items: Display all items in all bins.
Persistent Storage: Data is saved in a bins_data.json file, so your changes are preserved across sessions.
Clear Screen: Clear the console and display the help message.
Help Command: Display the list of available commands.
Getting Started
Prerequisites
Python 3.x
Installation
Clone this repository:

git clone https://github.com/abtblk/Python-Storage-Organizer.git
cd Python-Storage-Organizer
Run the script:

python bin_manager.py
Usage
Once the script is running, you can use the following commands:

Add Items: -a BIN ITEM1 #QTY, ITEM2 #QTY,...

Example: -a bin1 apple #3, banana #2
Transfer Items: -t FROM_BIN TO_BIN ITEM #QTY

Example: -t bin1 bin2 apple #2
Remove Items: -r ITEM #QTY BIN

Example: -r apple #1 bin2
Find Items: -f ITEM

Example: -f apple
List All Items: -l

Example: -l
List Available Items: --list-available

Example: --list-available
Clear Screen: -c

Example: -c
Help Command: -h

Example: -h
Exit Application: -q or --quit

Example: -q
Example Commands
Adding items: -a bin1 "red apple #4, green banana #2"
Transferring items: -t bin1 bin2 "red apple #2"
Removing items: -r "red apple #1" bin2
Finding an item: -f "red apple"
File Structure
bin_manager.py: The main script for managing bins and items.
bins_data.json: Automatically created data file to store your bins and items persistently.
Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request with your changes.

License
This project is open source and available under the MIT License.

Acknowledgments
Thanks to ChatGPT for the assistance in developing this script. Boy oh boy debugging was fun!
