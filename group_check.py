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
    return conn.entries[0].memberOf

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Get group memberships for an AD user.')
    parser.add_argument('username', type=str, help='Active Directory username')
    args = parser.parse_args()

    # Prompt for password without echoing
    password = getpass.getpass(prompt='Enter password: ')

    groups = get_user_groups(args.username, password)
    print(f"Groups for {args.username}:")
    
    # Extract and process group names
    group_names = []
    for group in groups:
        group_name = group.split(',')[0].split('=')[1]
        group_name = group_name.replace("\\#", "#")
        group_names.append(group_name)
    
    # Sort the group names
    group_names.sort()
    
    # Print sorted group names
    for group_name in group_names:
        print(group_name)

if __name__ == "__main__":
    main()

    