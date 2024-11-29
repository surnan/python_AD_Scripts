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
    return [entry.split(',')[0].split('=')[1] for entry in conn.entries[0].memberOf]

# Function to find common groups
def find_common_groups(user1, user2, password):
    groups_user1 = set(get_user_groups(user1, password))
    groups_user2 = set(get_user_groups(user2, password))
    common_groups = groups_user1.intersection(groups_user2)
    return common_groups

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description='Find common group memberships for two AD users.')
    parser.add_argument('user1', type=str, help='First Active Directory username')
    parser.add_argument('user2', type=str, help='Second Active Directory username')
    args = parser.parse_args()

    # Prompt for password without echoing
    password = getpass.getpass(prompt='Enter password: ')

    common_groups = find_common_groups(args.user1, args.user2, password)
    print(f"Common groups for {args.user1} and {args.user2}:")
    for group in common_groups:
        print(group)

if __name__ == "__main__":
    main()