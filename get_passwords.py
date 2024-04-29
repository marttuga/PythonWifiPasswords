import subprocess  # for running system commands
import re  # for regular expressions

# Run the command netsh wlan show profiles, capture the output and decode it
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True).stdout

# Use regular expression to look for entries that say "All User Profile: <profile_name>"
profile_names = re.findall(r"All User Profile\s+:\s(.*)", command_output)

# Create a list to store Wi-Fi profiles
wifi_list = []

# Iterate through profile names
for name in profile_names:
    wifi_profile = {}

    # Run netsh wlan show profile <profile_name> command to get profile information
    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True, text=True).stdout

    # Check if "Security key" is present in profile information
    if "Security key           : Absent" in profile_info:
        continue  # Skip profiles without security key
    else:
        # Store SSID (Wi-Fi network name)
        wifi_profile["ssid"] = name
        
        # Run netsh wlan show profile <profile_name> key=clear command to get password
        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True, text=True).stdout
        
        # Use regular expression to extract password
        password_match = re.search(r"Key Content\s+:\s(.*)", profile_info_pass)
        
        # Check if password was found
        if password_match:
            wifi_profile["password"] = password_match.group(1)
        else:
            wifi_profile["password"] = None  # No password found
        
        
        # Add Wi-Fi profile to the list
        wifi_list.append(wifi_profile)

# Print Wi-Fi profiles and passwords
for wifi_profile in wifi_list:
    print(wifi_profile)
