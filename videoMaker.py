import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

VIDEO_PATH = "E:/SchoolArchiving/vid_folders/class1/10/10/2022/cs35l-1-20221010-25834"
# INPUT: Path to folder full of .ts video files, filename for the finished video file, number of files to concatenate at once
# Assumes the folder is full of .ts video files with numeric, sequential names, starting at 0.ts
# Makes a video file out of all the .ts files
def concatenate_files(path, name, num_concat=40, cleanup=True):
    num_vid_files = len(os.listdir(path))
    # Iterating through the video files
    # all_vids = []
    tempfile_path = os.path.join(path, "tempfiles")
    os.makedirs(tempfile_path)
    for i in range(0, num_vid_files, num_concat):
        num_vids_to_concat = min(num_concat, (num_vid_files - i))
        vids = []
        for vid_num in range(i, i + num_vids_to_concat):
            print(f"Loading video number {vid_num}")
            vid_path = os.path.join(path, str(vid_num) + ".ts")
            vids.append(VideoFileClip(vid_path))
        vid_segment = concatenate_videoclips(vids)
        vid_segment.write_videofile(
            os.path.join(tempfile_path, (str(int(i / num_concat)) + ".mp4"))
        )
        print(f"Successfully concatenated videos {i} to {i + num_vids_to_concat}")
    temp_files = []
    num_temp_files = len(os.listdir(tempfile_path))
    for i in range(num_temp_files):
        vid_path = os.path.join(tempfile_path, str(i) + ".mp4")
        temp_files.append(VideoFileClip(vid_path))
        print(f"Loaded file {i}.mp4")
    final_vid = concatenate_videoclips(temp_files)
    print("Final video file made, writing to memory")
    final_vid.write_videofile(os.path.join(path, name))
    if cleanup:
        print("Cleaning up .ts files")
        files = os.listdir(path)
        for file in files:
            if file.endswith(".ts"):
                try:
                    os.remove(os.path.join(path, file))
                except PermissionError:
                    print(f"Couldn't remove file {file}")
        for file in os.listdir(tempfile_path):
            if file.endswith(".mp4"):
                try:
                    os.remove(os.path.join(tempfile_path, file))
                except PermissionError:
                    print(f"Couldn't remove file {file}")
    print("Done")


if __name__ == "__main__":
    concatenate_files(VIDEO_PATH, "testvid.mp4")
