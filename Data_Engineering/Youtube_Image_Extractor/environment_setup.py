import os
import os.path as osp
import sys
import subprocess

# implement pip as a subprocess:

def setup_environment(config):
    video_path = config["video_path"]
    image_path = config["image_path"]

    print("Setting up folders")
    if not osp.exists(video_path):
        os.makedirs(video_path)
        print("Created video folder")
    if not osp.exists(image_path):
        os.makedirs(image_path)
        print("Created image folder")
    print("Folder structure is ready")

    print("downloading requirements")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r','requirements.txt'])

if __name__=="__main__":
    from config import load_config
    config = load_config()
    setup_environment(config)