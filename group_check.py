import argparse
import getpass
from ldap3 import Server, Connection, ALL

# Define the server and connection
server = Server('ADSWCDCPDC12', get_info=ALL)

# Function to get group memberships
def get_user_groups(username, password):
    conn = Connection(server, 'CN=nandls01,OU=NYULMC Users,DC=nyumc,DC=org', password, auto_bind=True)
    search_filter = f'(sAMAccountName={username})'
    conn.search('DC=nyumc,DC=org', search_filter, attributes=['memberOf'])
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
    for group in groups:
        print(group)

if __name__ == "__main__":
    main()