import argparse
import getpass
import configparser
from ldap3 import Server, Connection, ALL

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract values from the configuration file
server_name = config['DEFAULT']['server']
user_dn = config['DEFAULT']['user_dn']
base_dn = config['DEFAULT']['base_dn']

# Define the server and connection
server = Server(server_name, get_info=ALL)

# Function to get group memberships
def get_user_groups(username, password):
    conn = Connection(server, user_dn, password, auto_bind=True)
    search_filter = f'(sAMAccountName={username})'
    conn.search(base_dn, search_filter, attributes=['memberOf'])
    if conn.entries and 'memberOf' in conn.entries[0]:
        return [entry.split(',')[0].split('=')[1] for entry in conn.entries[0].memberOf]
    else:
        return []

# Function to find unique groups
def find_unique_groups(user1, user2, password):
    groups_user1 = set(get_user_groups(user1, password))
    groups_user2 = set(get_user_groups(user2, password))
    
    unique_to_user1 = groups_user1 - groups_user2
    unique_to_user2 = groups_user2 - groups_user1
    
    return unique_to_user1, unique_to_user2

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Find unique group memberships for two AD users.')
    parser.add_argument('user1', type=str, help='First Active Directory username')
    parser.add_argument('user2', type=str, help='Second Active Directory username')
    args = parser.parse_args()

    # Prompt for password without echoing
    password = getpass.getpass(prompt='Enter password: ')

    unique_to_user1, unique_to_user2 = find_unique_groups(args.user1, args.user2, password)
    
    print(f"Groups unique to {args.user1}:")
    for group in unique_to_user1:
        print(f"{group} ({args.user1})")
    
    print(f"\nGroups unique to {args.user2}:")
    for group in unique_to_user2:
        print(f"{group} ({args.user2})")

if __name__ == "__main__":
    main()