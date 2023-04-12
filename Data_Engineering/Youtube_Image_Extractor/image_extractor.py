import os.path as osp
import pandas as pd
import cv2
import traceback

def extract_imgs(config):
    image_path = config["image_path"]
    image_data_file=osp.join(image_path, "image_list.csv")
    video_path = config["video_path"]
    video_data_file = osp.join(video_path, "video_list.csv")

    try:
        img_data = pd.read_csv(image_data_file)
    except FileNotFoundError:
        print("Image data csv not found")
        img_data = pd.DataFrame(columns=['image_id', 'video_id', 'frame', 'height', 'width'])
        img_data.to_csv(image_data_file, index=False)
        print("New empty csv file created instead")

    vid_data = pd.read_csv(video_data_file)
    vid_data.video_id=vid_data.video_id.astype(str)

    screenshot_rate=config["screenshot_rate"]

    print("Processing Videos")
    try:
        for index in vid_data.index:
            if vid_data["processed"][index]:
                continue

            vid_id=int(vid_data["video_id"][index])
            video_file=osp.join(video_path, str(vid_id)+".mp4")

            cap = cv2.VideoCapture(video_file)
            vid_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            count_img=0

            for frame_id in range(0,vid_length,screenshot_rate):
                if len(img_data.loc[(img_data['video_id'] == vid_id) & (img_data['frame'] == frame_id)])>0:
                    continue
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id - 1)
                ret, frame = cap.read()
                image_id = len(img_data.index)
                cv2.imwrite(osp.join(image_path,f"{image_id}.png"), frame)
                img_data.loc[image_id] = [image_id,
                                          vid_id,
                                          frame_id,
                                          frame.shape[0],
                                          frame.shape[1]
                                          ]

                count_img+=1

            cap.release()
            vid_data.at[index,"processed"]=True
            print(f"Generated {count_img} images from video {vid_id}")
            #cv2.destroyAllWindows()

        img_data.to_csv(image_data_file, index=False)
        vid_data.to_csv(video_data_file, index=False)
        print("Image data saved")

    except (Exception, KeyboardInterrupt):
        print("Exit due to unexpected error")
        img_data.to_csv(image_data_file, index=False)
        vid_data.to_csv(video_data_file, index=False)
        print("Image data saved")
        traceback_info = traceback.format_exc()
        print(traceback_info)

if __name__ == '__main__':
    from config import load_config
    config = load_config()
    extract_imgs(config)
