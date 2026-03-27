import os
import subprocess
from dotenv import load_dotenv

def start_tunnel():
    load_dotenv()

    # Configuration from .env
    ssh_ip = os.getenv("SSH_SERVER_IP")
    ssh_user = os.getenv("SSH_USER")
    key_path = os.getenv("SSH_PRIVATE_KEY_PATH")
    local_port = os.getenv("LOCAL_DB_PORT", "3307")
    remote_host = os.getenv("REMOTE_DB_HOST", "localhost")
    remote_port = os.getenv("REMOTE_DB_PORT", "3306")

    if not all([ssh_ip, ssh_user, key_path]):
        print("❌ Error: Missing SSH_SERVER_IP, SSH_USER, or SSH_PRIVATE_KEY_PATH in .env")
        return

    # Expand '~' to the full home directory path
    # Type guard: Ensure key_path is a string before passing to expanduser
    if key_path is None:
        print("❌ Error: SSH_PRIVATE_KEY_PATH is not set in your .env file.")
        return

    expanded_key_path = os.path.expanduser(key_path)

    # SSH Command Breakdown:
    # -i: Specifies the private key file
    # -L: Local port forwarding
    # -N: Do not execute a remote command (just forward ports)
    # -o StrictHostKeyChecking=accept-new: Automatically adds the server to known_hosts
    cmd = [
        "ssh",
        "-i", expanded_key_path,
        "-L", f"{local_port}:{remote_host}:{remote_port}",
        "-N",
        "-o", "StrictHostKeyChecking=accept-new",
        f"{ssh_user}@{ssh_ip}"
    ]

    print(f"🚀 Establishing secure tunnel via {expanded_key_path}...")
    print(f"🔗 Localhost:{local_port} -> {ssh_ip}:{remote_port}")

    try:
        # Using subprocess.run will keep the tunnel open until you hit Ctrl+C
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Tunnel closed by user.")
    except subprocess.CalledProcessError as e:
        print("\n❌ SSH Error: Ensure your public key is on the server and the path is correct.")

if __name__ == "__main__":
    start_tunnel()
