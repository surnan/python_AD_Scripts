# only working locally.  Not getting that list off remote computers.

import argparse
import win32com.client
import getpass

def get_local_admins(computer=None, username=None, password=None):
    if computer:
        computer = f"\\\\{computer}"
    else:
        computer = "."

    try:
        group_name = "Administrators"
        if username and password:
            locator = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            print(f"Connecting to {computer} with username {username}")
            connection = locator.ConnectServer(computer, "root\\cimv2", username, password)
            connection.Security_.ImpersonationLevel = 3
            group = connection.ExecQuery(f"SELECT * FROM Win32_Group WHERE Name='{group_name}'")
            members = []
            for g in group:
                for member in g.Associators_("Win32_GroupUser"):
                    members.append(member.Name)
        else:
            obj_group = win32com.client.Dispatch("AdsNameSpaces").GetObject("", f"WinNT://{computer}/{group_name},group")
            members = [member.Name for member in obj_group.Members()]
        
        return members
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(description='List users in the local admin group.')
    parser.add_argument('computer', nargs='?', default=None, help='Computer name to check. If not provided, checks the local computer.')
    parser.add_argument('--username', type=str, help='Username for remote computer.')
    args = parser.parse_args()

    password = None
    if args.username:
        password = getpass.getpass(prompt='Enter password: ')

    admins = get_local_admins(args.computer, args.username, password)
    if isinstance(admins, list):
        print("Local Administrators:")
        for admin in admins:
            print(admin)
    else:
        print(admins)

if __name__ == "__main__":
    main()