"""
Very basic helper script to automate the process of installing Valour

CONTRIBUTORS:
https://github.com/aut-mn
"""
import os, subprocess, json, platform

# Check if running as sudo, can't run as sudo on macOS due to brew
if os.geteuid() == 0 and platform.system() == "Darwin":
    print("Please run this script as a normal user.")
    exit(1)
elif os.geteuid() != 0 and platform.system() != "Darwin":
    print("Please run this script with escalated privileges.")
    exit(1)

def check_command(command):
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return True
    except subprocess.CalledProcessError: return False

package_managers = ["apt", "yum", "dnf", "zypper", "pacman", "brew", "port", "choco", "winget"]
packageManager = None
for manager in package_managers:
    if check_command(f"{manager} --version"): packageManager = manager

def install_package(package: str):
    """Installs a package"""
    try:
        print(f"Now installing {package}...")
        if packageManager == "pacman": subprocess.check_output(f"sudo pacman -S {package}", stderr=subprocess.STDOUT, shell=True)
        elif packageManager == "brew": subprocess.check_output(f"brew install {package}", stderr=subprocess.STDOUT, shell=True)
        elif packageManager is not None: subprocess.check_output(f"sudo {packageManager} install {package}", stderr=subprocess.STDOUT, shell=True)
        else: 
            print(f"Failed to install {package}. Error: No package manager detected.")
            return False
        print(f"{package} installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {str(e)}")
        return False


print("ValourBuild - Automated Valour Installation Helper")
initialPath = str(input("Input your desired path for Valour: "))
if not initialPath: initialPath = os.path.expanduser("~")
if not os.path.exists(initialPath): os.makedirs(initialPath)

for dependency in ["git", "dotnet", "redis-server"]:
    if not check_command(f"{dependency} --version"):
        if packageManager == "brew" and dependency == "redis-server": dependency = "redis"
        if not (install_package(dependency)): exit(1)


subprocess.run(["git", "clone", "https://github.com/Valour-Software/Valour"], cwd=initialPath)
path = os.path.join(initialPath, ("Valour" if packageManager != "winget" else "Valour"))
subprocess.run(["cp", "appsettings.helper.json", "appsettings.json"], cwd=path + ("/Valour/Server/" if packageManager != "winget" else "\\Valour\\Server\\"))

try:
    subprocess.run(["sudo", "dotnet", "workload", "restore", "--yes", "Valour.sln"], cwd=path)
    response = str(input("Would you like a guided configuration setup? (y/n): "))
    if response.lower() == "n":
        print("Skipping guided configuration setup.")
    elif response.lower() == "y":
        with open(path + ("/Valour/Server/appsettings.json" if packageManager != "winget" else "\\Valour\\Server\\appsettings.json"), "r") as f:
            # This will NOT work until https://github.com/Valour-Software/Valour/pull/1202 is merged!
            data = json.load(f)
            print("--- CDN ---")
            data["CDN"]["Key"] = str(input("Enter your CDN key: "))
            data["CDN"]["DbAddress"] = str(input("Enter your CDN Database Address: "))
            data["CDN"]["DbUser"] = str(input("Enter your CDN Database Username: "))
            data["CDN"]["DbPassword"] = str(input("Enter your CDN Database Password: "))
            data["CDN"]["DbName"] = str(input("Enter your CDN Database Name: "))
            print("--- S3 ---")
            data["CDN"]["S3Access"] = str(input("Enter your S3 Access Key: "))
            data["CDN"]["S3Secret"] = str(input("Enter your S3 Secret Key: "))
            data["CDN"]["S3Endpoint"] = str(input("Enter your S3 Endpoint: "))
            data["CDN"]["PublicS3Access"] = str(input("Enter your PUBLIC S3 Access Key: "))
            data["CDN"]["PublicS3Secret"] = str(input("Enter your PUBLIC S3 Secret Key: "))
            data["CDN"]["PublicS3Endpoint"] = str(input("Enter your PUBLIC S3 Endpoint: "))
            print("--- Database ---")
            data["Database"]["Host"] = str(input("Enter your Database Host: "))
            data["Database"]["Username"] = str(input("Enter your Database Username: "))
            data["Database"]["Password"] = str(input("Enter your Database Password: "))
            print("--- Redis ---")
            data["Redis"]["ConnectionString"] = str(input("Enter your Redis Connection String: "))
            print("--- Email ---")
            data["Email"]["ApiKey"] = str(input("Enter your Email API Key (Optional): "))
            if not data["Email"]["ApiKey"]: data["Email"]["ApiKey"] = "fake-value"
            json.dump(data, f)
except Exception as e:
    print(f"Failed to install Valour: {e}. Cleaning up workspace...")
    parent_dir = os.path.dirname(path)
    if packageManager != "winget": subprocess.run(["rm", "-rf", os.path.join(parent_dir, "Valour")])
    else: subprocess.run(["rmdir", "/s", "/q", os.path.join(parent_dir, "Valour")])
    exit(1)

print("Valour installed successfully! In the project folder, ensure redis-server and PostgreSQL are running, then run 'dotnet run' to start the server.")
