import configparser
import os
import winreg
import win32com.client as win32

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract values from the configuration file
try:
    server_name = config['DEFAULT']['server']
    user_dn = config['DEFAULT']['user_dn']
    base_dn = config['DEFAULT']['base_dn']
    email = config['DEFAULT']['email']
except KeyError as e:
    print(f"Missing configuration key: {e}")
    exit(1)

# Print configuration values for debugging
print(f"Server: {server_name}")
print(f"User DN: {user_dn}")
print(f"Base DN: {base_dn}")
print(f"Email: {email}")

def list_installed_apps():
    # List to store the names of installed applications
    installed_apps = []

    # Registry paths to check for installed applications
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    # Iterate over both registry paths
    for reg_path in reg_paths:
        try:
            # Open the registry key
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            
            # Iterate over the subkeys (installed applications)
            for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                subkey_name = winreg.EnumKey(reg_key, i)
                subkey = winreg.OpenKey(reg_key, subkey_name)
                
                try:
                    # Get the application name
                    app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    installed_apps.append(app_name)
                except FileNotFoundError:
                    # If the DisplayName value is not found, skip this application
                    continue
                
                # Close the subkey
                winreg.CloseKey(subkey)
            
            # Close the registry key
            winreg.CloseKey(reg_key)
        except FileNotFoundError:
            # If the registry path is not found, skip it
            continue

    return installed_apps

# Get the list of installed applications
installed_apps = list_installed_apps()

# Print the list of installed applications
for app in installed_apps:
    print(app)

# Write the list of installed applications to a file
file_path = os.path.abspath('installed_apps.txt')
with open(file_path, 'w') as f:
    for app in installed_apps:
        f.write(app + '\n')

# Ensure the file exists before attempting to send the email
if not os.path.exists(file_path):
    print(f"Error: The file {file_path} does not exist.")
else:
    # Function to send an email with the file attached
    def send_email_with_attachment(subject, body, to, attachment_path):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = subject
        mail.Body = body
        mail.To = to
        mail.Attachments.Add(attachment_path)
        mail.Send()

    # Send the email
    send_email_with_attachment(
        subject='List of Installed Applications',
        body='Please find attached the list of installed applications.',
        to=email,
        attachment_path=file_path
    )

    print(f"Email sent successfully with attachment: {file_path}")