import argparse
import getpass
import configparser
from ldap3 import Server, Connection, ALL

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract values from the configuration file
try:
    server_name = config['DEFAULT']['server']
    user_dn = config['DEFAULT']['user_dn']
    base_dn = config['DEFAULT']['base_dn']
except KeyError as e:
    print(f"Missing configuration key: {e}")
    exit(1)

# Print configuration values for debugging
print(f"Server: {server_name}")
print(f"User DN: {user_dn}")
print(f"Base DN: {base_dn}")

# Define the server and connection
server = Server(server_name, get_info=ALL)


# Function to get the OU of a computer account
def get_computer_ou(computer_name, password):
    conn = Connection(server, user_dn, password, auto_bind=True)
    search_filter = f"(sAMAccountName={computer_name}$)"
    conn.search(base_dn, search_filter, attributes=['distinguishedName'])
    
    if conn.entries:
        dn = conn.entries[0].distinguishedName.value
        ou = ",".join(dn.split(",")[1:])
        return ou
    else:
        return None

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Get the OU of a computer account in Active Directory.')
    parser.add_argument('computer_name', type=str, help='Computer name in Active Directory')
    args = parser.parse_args()

    # Prompt for password without echoing
    password = getpass.getpass(prompt='Enter password: ')

    computer_ou = get_computer_ou(args.computer_name, password)
    
    if computer_ou:
        print(f"The OU of the computer account {args.computer_name} is: {computer_ou}")
    else:
        print(f"Computer account {args.computer_name} not found.")

if __name__ == "__main__":
    main()