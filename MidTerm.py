import os
import json
from collections import defaultdict

def load_users(file_path): # Defines the function 'load_users' which takes 'file_path' as a parameter.
    try:
        with open(file_path, 'r', encoding='utf-8') as f: # opens a file then automaticaly closses it when the code block runs.
            return json.load(f)  # Assumes data is stored as a list of dictionaries
    except FileNotFoundError: # exception handling.
        print("Error: User data file not found.")
        return []
    except json.JSONDecodeError: # exception handling.
        print("Error: Invalid JSON format.")
        return []

def count_permissions(users):
    permission_count = defaultdict(int)
    for user in users:
        for permission in user.get("permissions", []):
            permission_count[permission] += 1 # this code block finds the amount of times a permishion is shown across all users.
    
    print("\nPermission Counts:")
    for perm, count in permission_count.items():
        print(f"{count} users have '{perm}' permission.") # I belive this code block finds how many users have permissions and displays them.
    
    return permission_count

def find_users_by_permission(users, permission): #function for finding users based on permissions.
    matching_users = [] #start of a list for matching users variable.
    for user in users:
        if permission in user.get("permissions", []):
            matching_users.append(user["name"]) 
    
    if matching_users: #will run code below if variable is met.
        print(f"\nUsers with '{permission}' permission:")
        for user in matching_users: # for each user in matching users print (f" - {user})
            print(f"  - {user}")
    else: #if matching_users is not met with true print what is blow.
        print(f"No users found with '{permission}' permission.")
    
    return matching_users

def find_user_roles(users, username): #this code block prints the roles and permisions of a specific user.
    for user in users:
        if user["name"].lower() == username.lower(): # ensures users input matches with the username found in the jason file.
            print(f"\nUser: {user['name']}") #asignes the user name to the user found in the list.
            print(f"Roles: {', '.join(user.get('roles', [])) or 'No roles'}") #applies the roles of the users to the users in the current list.
            print(f"Permissions: {', '.join(user.get('permissions', [])) or 'No permissions'}") #does the same as last but with permissions instead of roles.
            return user
    print(f"User '{username}' not found.")
    return None

def get_valid_file(): # has user input file path for jason file and tells them their path is invalid if no file is found (does not do the exception handling however.)
    while True:
        file_path = input("Enter the user data JSON file path: ") #jason file path input.
        if os.path.isfile(file_path) and file_path.endswith('.json'): #ensures the file exists and that it is a .json file type.
            return file_path #if so teturn the file_path variable and use it as needed.
        print("Invalid file. Please provide a valid JSON file.")

def find_most_common_permission(users):
    # Dictionary to store the count of each permission
    permission_count = defaultdict(int)

    # Iterate through all users and count each permission
    for user in users:
        for permission in user.get("permissions", []):
            permission_count[permission] += 1

    # If there are no permissions, exit early
    if not permission_count:
        print("No permissions found in user data.")
        return None

    # Find the maximum count value
    max_count = max(permission_count.values())

    # Find all permissions that match the maximum count
    most_common_permissions = [perm for perm, count in permission_count.items() if count == max_count]

    # Display results
    print("\nMost Common Permission(s):")
    for perm in most_common_permissions:
        print(f"  - '{perm}' with {max_count} occurrences.")

    return most_common_permissions

def find_last_assigned_role(users):
    last_roles = []  # List to store the last assigned role for each user

    # Iterate through all users
    for user in users:
        roles = user.get("roles", [])
        if roles:  # If the user has roles, take the last one
            last_roles.append(roles[-1])

    # If no roles exist, exit early
    if not last_roles:
        print("No roles found in user data.")
        return None

    # Count occurrences of each last role
    role_count = defaultdict(int)
    for role in last_roles:
        role_count[role] += 1

    # Find the most common last assigned role(s)
    max_count = max(role_count.values())
    most_common_last_roles = [role for role, count in role_count.items() if count == max_count]

    # Display results
    print("\nMost Common Last Assigned Role(s):")
    for role in most_common_last_roles:
        print(f"  - '{role}' assigned {max_count} times.")

    return most_common_last_roles

def main():  #this is the start of main
    file_path = get_valid_file()
    users = load_users(file_path)
    
    if not users: #displays the print () if no specified user is found.
        print("No user data found. Exiting.")
        return
    
    count_permissions(users)
    
    while True: #the code here and down handles getting the users first input to determine what they want to do.
        print("\nOptions:")
        print("1. Find users by permission")
        print("2. Find roles and permissions of a user")
        print("3. Find the most common permission")
        print("4. Find the last assigned role")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            perm = input("Enter permission to search for: ")
            find_users_by_permission(users, perm)
        elif choice == '2':
            username = input("Enter username: ")
            find_user_roles(users, username)
        elif choice == '3':
            find_most_common_permission(users) 
        elif choice == '4':
            find_last_assigned_role(users)
        elif choice == '5':
            print("Exiting.")
            break
        else: #ensures user inputs a valid choise by looping if input is not 1-5.
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
