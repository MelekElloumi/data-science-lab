import pytube.exceptions
from pytube import YouTube
import pandas as pd
from time import time
import os
import traceback
import os.path as osp

def register_vids(config):
    url = ""
    while url.upper() != 'N':
        url = input("Insert a youtube url or 'N' if you want to quit:")
        if url.upper() != 'N':
            if url.startswith("https://youtu.be/"):
                video_path = config["video_path"]
                video_urls_file = osp.join(video_path, "video_urls.txt")
                with open(video_urls_file, 'a') as f:
                    f.write(url + "\n")
            else:
                print("Wrong url format")
        else:
            print("Exiting urls input")
def download_vids(config):
    video_path = config["video_path"]
    video_data_file = osp.join(video_path, "video_list.csv")
    video_urls_file = osp.join(video_path, "video_urls.txt")
    resolution=config["resolution"]

    try:
        vid_df = pd.read_csv(video_data_file)
    except FileNotFoundError:
        print("Video data csv not found")
        vid_df = pd.DataFrame(columns=['video_id', 'url', 'title', 'resolution', 'length', 'size', 'processed'])
        vid_df.to_csv(video_data_file, index=False)
        print("New empty csv file created instead")

    with open(video_urls_file, 'r') as f:
        try:
            print("Processing Url file")
            for url in f:
                url = url.rstrip("\n")
                if any(vid_df['url'].str.contains(url, regex=False)) or not url:
                    continue

                down_time=time()
                video_id=len(vid_df.index)
                filename=f"{video_id}.mp4"

                for i in range(100):
                    try:
                        yt=YouTube(url)
                        title=yt.title
                    except pytube.exceptions.PytubeError:
                        continue
                    else:
                        break
                print("Downloading: "+title)
                try:
                    yt.streams.filter(file_extension='mp4', res=resolution, only_video=config["only_video"],
                                      only_audio=config["only_audio"]).first().download(
                                                        output_path=video_path, filename=filename)
                    vid_df.loc[video_id] = [video_id,
                                            url,
                                            title,
                                            resolution,
                                            round(yt.length / 60, 2),
                                            round(os.stat(video_path + "\\" + filename).st_size / 1024 ** 2, 2),
                                            False]
                except AttributeError:
                    print(resolution+" resolution was not found. Downloading in 720p instead")
                    yt.streams.filter(file_extension='mp4', res="720p").first().download(
                        output_path=video_path, filename=filename)
                    vid_df.loc[video_id] = [video_id,
                                            url,
                                            title,
                                            "720p",
                                            round(yt.length / 60, 2),
                                            round(os.stat(video_path + "\\" + filename).st_size / 1024 ** 2, 2),
                                            False]

                print("Finished downloading "+title+" in "+str(time()-down_time))

            vid_df.to_csv(video_data_file, index=False)
            print("Video data saved")

        except (Exception, KeyboardInterrupt):
            print("Exit due to unexpected error")
            vid_df.to_csv(video_data_file, index=False)
            print("Video data saved")
            traceback_info = traceback.format_exc()
            print(traceback_info)

if __name__=="__main__":
    from config import load_config
    config = load_config()
    register_vids(config)
    download_vids(config)