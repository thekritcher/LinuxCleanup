import subprocess
import sys

def run_command(command):
    """ Run shell command and return the output """
    try:
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_distribution():
    """ Determine the Linux distribution """
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
            for line in lines:
                if "ID_LIKE" in line or "ID" in line:
                    distro = line.strip().split("=")[1].replace('"', '')
                    return distro
    except FileNotFoundError:
        print("Could not determine the operating system.")
        sys.exit(1)
    return ""

def manage_packages(distro):
    """ Manage packages based on the distribution """
    if "arch" in distro:
        # Arch Linux specific commands
        orphan_command = "pacman -Qdtq"
        remove_command = "sudo pacman -Rns"
        mirror_command = "sudo reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist"
    elif "debian" in distro or "ubuntu" in distro:
        # Debian/Ubuntu specific commands
        orphan_command = "apt list --installed | grep -v automatic"
        remove_command = "sudo apt autoremove"
        mirror_command = "sudo apt-get update"
    elif "fedora" in distro or "rhel" in distro:
        # Fedora/RHEL specific commands
        orphan_command = "dnf repoquery --unneeded"
        remove_command = "sudo dnf autoremove"
        mirror_command = "sudo dnf update --refresh"
    else:
        print(f"Distribution '{distro}' is not supported by this script.")
        sys.exit(1)

    orphans = run_command(orphan_command)
    if orphans:
        print("Orphaned packages found:")
        print(orphans)
        remove = input("Would you like to remove these packages? (y/n): ")
        if remove.lower() == 'y':
            run_command(f"{remove_command} {orphans}")
            print("Orphaned packages have been removed.")
        else:
            print("No packages were removed.")
    else:
        print("No orphaned packages found.")

    optimize = input("Would you like to optimize your mirror list now? (y/n): ")
    if optimize.lower() == 'y':
        run_command(mirror_command)
        print("Mirror list has been optimized.")
    else:
        print("Mirror list optimization skipped.")

def main():
    distro = get_distribution()
    manage_packages(distro)

if __name__ == "__main__":
    main()
