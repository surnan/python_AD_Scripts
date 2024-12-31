import winreg

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