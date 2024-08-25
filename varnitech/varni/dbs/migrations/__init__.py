import os
import shutil

def copy_bootstrap(destination_path):
    """Copy the Alembic bootstrap files to the destination directory."""
    bootstrap_dir = os.path.join(os.path.dirname(__file__), 'bootstrap')
    
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    for item in os.listdir(bootstrap_dir):
        s = os.path.join(bootstrap_dir, item)
        d = os.path.join(destination_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    
    print(f"Bootstrap files copied to {destination_path}")
