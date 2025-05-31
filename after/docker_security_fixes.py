import json
import os
import yaml

# Update daemon.json
def harden_daemon_json():
    daemon_config = {
        "userns-remap": "default",
        "no-new-privileges": True,
        "icc": False,
        "log-driver": "json-file",
        "log-opts": {"max-size": "10m", "max-file": "3"}
    }
    daemon_path = "C:\\ProgramData\\Docker\\config\\daemon.json"
    try:
        with open(daemon_path, "w") as f:
            json.dump(daemon_config, f, indent=4)
        print(f"Updated {daemon_path} with hardening flags")
    except PermissionError:
        print(f"Error: Need admin privileges to write to {daemon_path}")

# Inject security settings into Dockerfile
def harden_dockerfile():
    dockerfile_path = "after/Dockerfile"
    healthcheck = "HEALTHCHECK --interval=30s --timeout=3s CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1"
    user_line = "USER appuser"

    with open(dockerfile_path, "r") as f:
        lines = f.readlines()

    # Check if USER and HEALTHCHECK already exist
    has_user = any("USER appuser" in line for line in lines)
    has_healthcheck = any("HEALTHCHECK" in line for line in lines)

    if not has_user or not has_healthcheck:
        with open(dockerfile_path, "w") as f:
            for line in lines:
                f.write(line)
                if "COPY app.py ." in line and not has_user:
                    f.write(f"{user_line}\n")
                if "CMD [\""python\"", \""app.py\""]" in line and not has_healthcheck:
                    f.write(f"{healthcheck}\n")
        print("Injected USER and HEALTHCHECK into Dockerfile")
    else:
        print("Dockerfile already hardened")

# Inject security settings into docker-compose.yml
def harden_docker_compose():
    compose_path = "after/docker-compose.yml"
    with open(compose_path, "r") as f:
        config = yaml.safe_load(f)

    # Add security settings to web service
    web = config["services"]["web"]
    web["read_only"] = True
    web["security_opt"] = ["no-new-privileges:true"]
    web["mem_limit"] = "256m"
    web["pids_limit"] = 100
    web["volumes"] = ["./.env:/app/.env:ro"]

    # Add security settings to db service
    db = config["services"]["db"]
    db["read_only"] = True
    db["mem_limit"] = "256m"
    db["pids_limit"] = 100

    # Make networks internal
    config["networks"]["frontend"]["internal"] = True
    config["networks"]["backend"]["internal"] = True

    with open(compose_path, "w") as f:
        yaml.safe_dump(config, f, default_flow_style=False)
    print("Injected security settings into docker-compose.yml")

if __name__ == "__main__":
    harden_daemon_json()
    harden_dockerfile()
    harden_docker_compose()
