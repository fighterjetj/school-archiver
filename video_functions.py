from course_links import duoMobileLogin, makeDriver
from constants import *
import requests, os, datetime, getpass, time

# Bruinlearn media is stored sequentially, with 0.ts being the first couple seconds of the video
URL = "https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20221109-27311.mp4/media_w1066734084_tkd293emF0b2tlbmVuZHRpbWU9MTY2ODY4MDcyOSZ3b3d6YXRva2VuaGFzaD12RnNXaUNQbTNYejRyaldHcXhzT3hDLXI5OXh1RGxiOUJUcjYyalY4V1RrPQ==_0.ts"
link = "https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20221109-27311.mp4/media_w1066734084_tkd293emF0b2tlbmVuZHRpbWU9MTY2ODY4MDcyOSZ3b3d6YXRva2VuaGFzaD12RnNXaUNQbTNYejRyaldHcXhzT3hDLXI5OXh1RGxiOUJUcjYyalY4V1RrPQ==_"

# INPUT: A link to any video clip from a lecture, the source url that the video comes from, the filetype of these videos, the name of the video,
# the byte size for writing the video clips, the parent directory to store all the videos in, and after how many videos you want to get an update
# Downloads all the video clips for a given lecture and saves them in a file
def get_videos(
    start_link,
    source_url="https://bclive.oid.ucla.edu/",
    file_type=CLIP_VIDEO_TYPE,
    video_name=None,
    download_chunks=1024 * 1024,
    parent_dir="vid_folders/",
    update_interval=50,
):
    # Checking the link comes from the source url
    if start_link[: len(source_url)] != source_url:
        raise Exception("Passed link does not match the intended source")
    # Checking it is a link to a file of the passed type
    if start_link[-len(file_type) :] != file_type:
        raise Exception(f"Not a {file_type} file url")
    base_link = start_link[: -len(file_type)]
    # Stripping the video number off the end of the link to get a base link to use
    while base_link[-1].isnumeric():
        base_link = base_link[:-1]
    # If no video name was passed, we download the files in the parent directory
    if video_name:
        vid_path = os.path.join(parent_dir, video_name)
    else:
        vid_path = parent_dir
    # Making a directory to store the video files
    curr_vid = 0
    try:
        os.makedirs(vid_path)
        print("Made folder for videos")
    except FileExistsError:
        # If the directory already exists, we want to continue where the downloader left off
        num_clips = 0
        for file in os.listdir(vid_path):
            if file.endswith(CLIP_VIDEO_TYPE):
                num_clips += 1
        print(f"Already {num_clips} existing clips in {vid_path}")
        curr_vid = num_clips
    video_file = requests.get(base_link + str(curr_vid) + CLIP_VIDEO_TYPE, stream=True)
    # As long as the video file exists, we want to download it
    # If the status code is 200, the download was a success
    while video_file.status_code == 200:
        with open(os.path.join(vid_path, str(curr_vid) + CLIP_VIDEO_TYPE), "wb") as vid:
            for chunk in video_file.iter_content(chunk_size=download_chunks):
                if chunk:
                    vid.write(chunk)
        # Updating on progress based on the passed parameter
        if curr_vid % update_interval == 0:
            print(f"Finished downloading video file #{curr_vid}")
        curr_vid += 1
        video_file = requests.get(
            base_link + str(curr_vid) + CLIP_VIDEO_TYPE, stream=True
        )
    print("All videos downloaded!")


# INPUT: A dictionary formatted as {date1: (video1name, video1link), date2: (video2name, video2link)}, course name, and path for course videos
# Downloads all lecture videos and stores them in the directory passed under a folder with the course name
# The folder with the course name has a folder for every date with the downloaded videos inside of it
def downloadCourseVids(course_dict, course, folder_path):
    dates = course_dict.keys()
    course_folder_path = os.path.join(folder_path, course)
    for date in dates:
        print(f"Downloading lecture from {date} for the course {course}")
        vid_folder_path = os.path.join(course_folder_path, date)
        # If this folder already exists, we probably already downloaded that lecture
        get_videos(
            start_link=course_dict[date][1] + CLIP_VIDEO_TYPE,
            parent_dir=vid_folder_path,
        )


# INPUT: A dictionary of dictionaries formatted as {classname: {date1: (video1name, video1link), date2: (video2name, video2link)}}
# Downloads all the course videos in the dictionary
def downloadAllCourseVids(all_courses_dict, folder_path=VID_FOLDER):
    courses = all_courses_dict.keys()
    for course in courses:
        downloadCourseVids(
            course_dict=all_courses_dict[course], course=course, folder_path=folder_path
        )


if __name__ == "__main__":
    pass
