from video_downloader import download_vids
from image_extractor import extract_imgs
from environment_setup import setup_environment
import os.path as osp

def datagen_pipeline(config):
    setup_environment(config)
    download_vids(config)
    extract_imgs(config)

if __name__=="__main__":
    from config import load_config
    config = load_config()
    datagen_pipeline(config)