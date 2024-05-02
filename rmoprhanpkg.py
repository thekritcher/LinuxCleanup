import subprocess
import sys

def run_command(command):
    """ Run shell command and return the output """
    try:
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.stdout
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def list_orphaned_packages():
    """ List all orphaned packages """
    command = "pacman -Qdtq"
    orphans = run_command(command)
    if orphans:
        return orphans.strip().split('\n')
    else:
        return []

def remove_packages(packages):
    """ Remove specified packages """
    command = f"sudo pacman -Rns {' '.join(packages)}"
    print("Removing the following orphaned packages:")
    print('\n'.join(packages))
    return run_command(command)

def optimize_mirror_list():
    """ Optimize the mirror list using reflector """
    command = "sudo reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist"
    print("Optimizing the mirror list...")
    return run_command(command)

def main():
    print("Checking for orphaned packages...")
    orphans = list_orphaned_packages()
    if orphans:
        print("Orphaned packages found:")
        print('\n'.join(orphans))
        remove = input("Would you like to remove these packages? (y/n): ")
        if remove.lower() == 'y':
            remove_packages(orphans)
        else:
            print("No packages were removed.")
    else:
        print("No orphaned packages found.")
    
    optimize = input("Would you like to optimize your mirror list now? (y/n): ")
    if optimize.lower() == 'y':
        optimize_mirror_list()
        print("Mirror list has been optimized.")
    else:
        print("Mirror list optimization skipped.")

if __name__ == "__main__":
    main()
