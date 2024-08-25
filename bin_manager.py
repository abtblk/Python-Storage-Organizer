import json
import os
import platform

# Define the file to store bin data
DATA_FILE = "bins_data.json"

# Ensure the file exists; create it if it does not
def ensure_file_exists():
    if not os.path.isfile(DATA_FILE):
        try:
            with open(DATA_FILE, "w") as file:
                json.dump({}, file)  # Create an empty JSON object
            print(f"File '{DATA_FILE}' created successfully.")
        except IOError as e:
            print(f"Error creating file: {e}")

# Load bins data from file, if it exists
def load_bins():
    ensure_file_exists()
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data from file: {e}")
        return {}

# Save bins data to file
def save_bins(bins):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(bins, file)
    except IOError as e:
        print(f"Error saving data to file: {e}")

# Dictionary to store bins and items
bins = load_bins()

def add_item(bin_name, items):
    if bin_name not in bins:
        bins[bin_name] = {}
    items_list = [item.strip() for item in items.split(',') if item.strip()]
    for item in items_list:
        if item:
            # Parse item and quantity
            if ' #' in item:
                item_name, quantity = item.rsplit(' #', 1)
                quantity = int(quantity)
            else:
                item_name, quantity = item, 1
            
            # Add or update item in the bin
            if item_name in bins[bin_name]:
                bins[bin_name][item_name] += quantity
            else:
                bins[bin_name][item_name] = quantity
            
            print(f"Added {quantity} of item '{item_name}' to bin '{bin_name}'.")
    save_bins(bins)

def transfer_item(from_bin, to_bin, item):
    if ' #' in item:
        item_name, quantity = item.rsplit(' #', 1)
        quantity = int(quantity)
    else:
        item_name, quantity = item, 1

    if from_bin in bins and item_name in bins[from_bin]:
        if bins[from_bin][item_name] >= quantity:
            bins[from_bin][item_name] -= quantity
            if bins[from_bin][item_name] == 0:
                del bins[from_bin][item_name]
            add_item(to_bin, f"{item_name} #{quantity}")
            print(f"Transferred {quantity} of item '{item_name}' from '{from_bin}' to '{to_bin}'.")
        else:
            print(f"Not enough quantity of '{item_name}' in bin '{from_bin}' to transfer.")
    else:
        print(f"Item '{item_name}' not found in bin '{from_bin}'.")

def find_item(item):
    if ' #' in item:
        item_name, _ = item.rsplit(' #', 1)
    else:
        item_name = item

    for bin_name, items in bins.items():
        if item_name in items:
            print(f"Item '{item_name}' found in bin '{bin_name}' with quantity {items[item_name]}.")
            return
    print(f"Item '{item_name}' not found in any bin.")

def remove_item(item, bin_name):
    if ' #' in item:
        item_name, quantity = item.rsplit(' #', 1)
        quantity = int(quantity)
    else:
        item_name, quantity = item, 1

    if bin_name in bins and item_name in bins[bin_name]:
        if bins[bin_name][item_name] > quantity:
            bins[bin_name][item_name] -= quantity
            print(f"Removed {quantity} of item '{item_name}' from bin '{bin_name}'.")
        elif bins[bin_name][item_name] == quantity:
            del bins[bin_name][item_name]
            print(f"Removed all of item '{item_name}' from bin '{bin_name}'.")
        else:
            print(f"Not enough quantity of '{item_name}' in bin '{bin_name}' to remove.")
        save_bins(bins)
    else:
        print(f"Item '{item_name}' not found in bin '{bin_name}'.")

def list_items():
    if not bins:
        print("No bins found.")
    else:
        for bin_name, items in bins.items():
            print(f"Bin '{bin_name}':")
            for item, quantity in items.items():
                print(f"  - {item}: {quantity}")

def list_available_items():
    item_set = set()
    for items in bins.values():
        item_set.update(items.keys())
    if not item_set:
        print("No items available.")
    else:
        print("Available items:")
        for item in item_set:
            print(f"  - {item}")

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_help():
    print("Available commands (with aliases):")
    print("  -a, --add BIN ITEM1 #QTY, ITEM2 #QTY,... : Add ITEM1, ITEM2,... with quantity QTY to BIN")
    print("  -t, --trans, --transfer FROM_BIN TO_BIN ITEM : Transfer ITEM from FROM_BIN to TO_BIN")
    print("  -f, --find ITEM                           : Find ITEM")
    print("  -r, --rm, --remove ITEM BIN               : Remove ITEM from BIN")
    print("  -l, --list                                : List all items in all bins")
    print("  --list-available                          : List all available items")
    print("  -c, --clear                               : Clear the screen")
    print("  -h, --help                                : Show this help message")
    print("  -q, --quit, --exit                        : Quit the application")

def parse_command(command):
    if command.startswith('-'):
        # Split the command into action and arguments
        parts = command.split(maxsplit=1)
        action = parts[0]
        remaining_args = parts[1] if len(parts) > 1 else ''
        
        if action in ['-a', '--add']:
            # Extract bin name and items; handle multi-word items with quantities
            if ' ' in remaining_args:
                bin_name, items = remaining_args.split(' ', 1)
                add_item(bin_name.strip(), items.strip())
            else:
                print("Invalid arguments for add command.")
                
        elif action in ['-t', '--trans', '--transfer']:
            # Extract from_bin, to_bin, and item; handle multi-word items
            if ' ' in remaining_args:
                parts = remaining_args.split(' ', 2)
                if len(parts) == 3:
                    from_bin, to_bin, item = parts
                    transfer_item(from_bin.strip(), to_bin.strip(), item.strip())
                else:
                    print("Invalid arguments for transfer command.")
            else:
                print("Invalid arguments for transfer command.")
                
        elif action in ['-f', '--find']:
            find_item(remaining_args.strip())
        
        elif action in ['-r', '--rm', '--remove']:
            # Extract item and bin_name; handle multi-word items
            if ' ' in remaining_args:
                parts = remaining_args.rsplit(' ', 1)
                if len(parts) == 2:
                    item, bin_name = parts
                    remove_item(item.strip(), bin_name.strip())
                else:
                    print("Invalid arguments for remove command.")
            else:
                print("Invalid arguments for remove command.")
                
        elif action in ['-l', '--list']:
            list_items()
        
        elif action in ['--list-available']:
            list_available_items()
        
        elif action in ['-c', '--clear']:
            clear_screen()
            show_help()  # Show help after clearing the screen
        
        elif action in ['-h', '--help']:
            show_help()
        
        elif action in ['-q', '--quit', '--exit']:
            print("Exiting Bin Manager. Goodbye!")
            return False
        
        else:
            print("Invalid command.")
    else:
        print("Commands should start with '-' or '--'.")
    return True

def main():
    print("Welcome to the Interactive Bin Manager!")
    show_help()  # Show help on startup

    while True:
        try:
            command = input("\nEnter command: ").strip()
            if not parse_command(command):
                break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()