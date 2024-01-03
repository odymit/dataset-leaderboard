from pathlib import Path

import yaml

PROJECT_DIR = Path(__file__).parent


def load_server_config(path=PROJECT_DIR / "sydata.secrets"):
    config = None
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def rsync_to_local():
    print("-" * 5, " syncing results to remote server ", "-" * 5)
    config = load_server_config()
    local_dir = PROJECT_DIR / "logs"
    host = config["host"]
    username = config["user"]
    remote_dir = config["remote_dir"]
    print("syncing results to remote server")
    print("server: ", host)
    print("remote dir: ", remote_dir + "/dataset_collections")

    cmd = f"rsync -avr --exclude '*.ckpt'  {username}@{host}:{remote_dir} {local_dir}"
    import pexpect

    child = pexpect.spawn(cmd)
    child.expect(".*password.*")
    child.sendline(config["passwd"])
    child.wait()
    print("-" * 5, " syncing results done! ", "-" * 5)


if __name__ == "__main__":
    rsync_to_local()
