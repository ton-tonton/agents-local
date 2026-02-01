import yaml
import os
import subprocess
import sys

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def sync_skills():
    # scripts/ is usually one level deep from root
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(workspace_root, 'skills.yaml')

    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

    try:
        config = load_config(config_path)
    except ImportError:
        print("Error: PyYAML is not installed. Run 'pip install pyyaml'")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    upstream_config = config.get('upstream_path')
    skills = config.get('skills', [])

    # normalizing upstream_path to a list
    upstream_paths = []
    if upstream_config:
        if isinstance(upstream_config, list):
            upstream_paths = upstream_config
        else:
            # Assume string
            upstream_paths = [upstream_config]

    # Validate global paths
    valid_paths = []
    for path in upstream_paths:
        if os.path.isdir(path):
            valid_paths.append(path)
        else:
            print(f"Warning: Global upstream path does not exist: {path}")

    skills_dir = os.path.join(workspace_root, 'skills')
    if not os.path.exists(skills_dir):
        os.makedirs(skills_dir)

    # Flatten skills list handling groups
    skills_to_sync = []

    for entry in skills:
        if isinstance(entry, str):
            skills_to_sync.append({"name": entry, "path": None})
        elif isinstance(entry, dict):
            names = entry.get('name')
            path = entry.get('path')

            if isinstance(names, list):
                for name in names:
                    skills_to_sync.append({"name": name, "path": path})
            elif isinstance(names, str):
                skills_to_sync.append({"name": names, "path": path})
            else:
                print(f"Warning: Invalid 'name' in skill entry: {entry}")

    print(f"Syncing {len(skills_to_sync)} skills...")

    for item in skills_to_sync:
        skill_name = item['name']
        skill_path = item['path']

        source = None

        # 1. Try explicit path if provided
        if skill_path:
            # If path ends with skill_name, assume it's the full path to the skill folder
            # If not, assume it's the parent folder (similar to upstream_path behavior)
            candidate = os.path.join(skill_path, skill_name)
            if os.path.isdir(candidate):
                source = candidate
            else:
                # Check if the user meant the direct path to the skill folder
                if os.path.isdir(skill_path) and os.path.basename(skill_path) == skill_name:
                     source = skill_path
                else:
                    print(f"Warning: Explicit path for '{skill_name}' does not contain skill: {candidate}")

        # 2. Fallback to global valid paths
        if not source and valid_paths:
            for path in valid_paths:
                candidate = os.path.join(path, skill_name)
                if os.path.isdir(candidate):
                    source = candidate
                    break

        dest = os.path.join(skills_dir, skill_name)

        if not source:
            print(f"Warning: Source skill '{skill_name}' not found (explicit path: {skill_path})")
            continue

        # Create destination directory if it doesn't exist
        if not os.path.exists(dest):
            os.makedirs(dest)

        # rsync command
        # -a: archive mode
        # -v: verbose
        # --delete: delete extraneous files from dest dirs
        # Ensure trailing slash on source to copy contents into dest
        source_cmd = source if source.endswith('/') else source + '/'

        cmd = ['rsync', '-av', '--delete', source_cmd, dest]

        try:
            # Running rsync
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            print(f"✓ {skill_name}")
            # print(result.stdout) # Uncomment for verbose output
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to sync {skill_name}: {e.stderr}")

if __name__ == "__main__":
    sync_skills()
