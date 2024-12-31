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

# Define the server
server = Server(server_name, get_info=ALL)

# Function to get users in a group
def get_group_members(server, user_dn, base_dn, group_name, password):
    print("Establishing connection...")
    conn = Connection(server, user_dn, password, auto_bind=True)
    print("Connection established.")
    search_filter = f'(cn={group_name})'
    conn.search(base_dn, search_filter, attributes=['member'])
    members = []
    for entry in conn.entries[0].member:
        user_dn = entry
        conn.search(user_dn, '(objectClass=person)', attributes=['sAMAccountName', 'displayName'])
        if conn.entries:
            user_info = conn.entries[0]
            username = user_info.sAMAccountName.value
            display_name = user_info.displayName.value
            members.append((username, display_name))
    
    # Sort members by display name
    members.sort(key=lambda x: (x[1] is None, x[1]))
    return members

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='List all users in an Active Directory group.')
    parser.add_argument('group', type=str, help='Active Directory group name')
    args = parser.parse_args()

    # Prompt for password without echoing
    password = getpass.getpass(prompt='Enter password: ')

    members = get_group_members(server, user_dn, base_dn, args.group, password)
    print(f"Members of group {args.group}:")
    for username, display_name in members:
        print(f"Username: {username}, Display Name: {display_name}")

if __name__ == "__main__":
    main()
