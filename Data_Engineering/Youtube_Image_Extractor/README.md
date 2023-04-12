# Youtube Image Extractor

- This is a script that downloads youtube videos and extract images for it to be used in a computer vision dataset.
- It uses pytube to download videos and opencv to navigate the videos.
- First you need to put the video directory and output image directory in config.json.
- `setup_environment` downloads the needed requirements and create the output directories if needed.
- `video_downloader` asks for urls to download videos from. The urls are saved in a text file.
- `image_extractor` loops through all unseen videos and take screenshots with a fixed rate defined in config.json.
- `pipeline` will execute everything in order with a single python file execution.