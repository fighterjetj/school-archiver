import os, shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips
from constants import *

VIDEO_PATH = "E:/SchoolArchiving/vid_folders/class1/10/10/2022/cs35l-1-20221010-25834"
# INPUT: Path to folder full of .ts video files, filename for the finished video file, number of files to concatenate at once
# Input (cont'd): whether we want to delete the video clips after, and the filetype to be concatenating
# Assumes the folder is full of video files with numeric, sequential names, starting at 0.ts (or whatever the filetype is)
# Makes a video file out of all the files
def concatenate_files(
    path, name, num_concat=40, cleanup=True, filetype=CLIP_VIDEO_TYPE
):
    num_vid_files = 0
    for file in os.listdir(path):
        if file.endswith(filetype):
            num_vid_files += 1
    tempfile_path = os.path.join(path, "tempfiles")
    # If the folder already exists, aborts to avoid causing problems
    try:
        os.makedirs(tempfile_path)
    except FileExistsError:
        # Removes the prior tempfile and just starts over
        shutil.rmtree(tempfile_path)
        os.makedirs(tempfile_path)
    # Iterating through the video files in the folder
    for i in range(0, num_vid_files, num_concat):
        num_vids_to_concat = min(num_concat, (num_vid_files - i))
        vids = []
        # We use for loops through ranges like this because the files should be numbered sequentially
        # And by default the os.listdir() orders alphabetically so 12.ts comes before 2.ts
        for vid_num in range(i, i + num_vids_to_concat):
            print(f"Loading video number {vid_num}")
            vid_path = os.path.join(path, str(vid_num) + filetype)
            vids.append(VideoFileClip(vid_path))
        # We save videos incrementally instead of making one big video file so that if the program fails some progress is saved
        vid_segment = concatenate_videoclips(vids)
        vid_segment.write_videofile(
            os.path.join(
                tempfile_path, (str(int(i / num_concat)) + FINISHED_VIDEO_TYPE)
            )
        )
        print(f"Successfully concatenated videos {i} to {i + num_vids_to_concat}")
    temp_files = []
    num_temp_files = 0
    for file in os.listdir(tempfile_path):
        if file.endswith(FINISHED_VIDEO_TYPE):
            num_temp_files += 1
    # Loading all the temp files that we just made
    for i in range(num_temp_files):
        vid_path = os.path.join(tempfile_path, str(i) + FINISHED_VIDEO_TYPE)
        temp_files.append(VideoFileClip(vid_path))
        print(f"Loaded file {i}{FINISHED_VIDEO_TYPE}")
    final_vid = concatenate_videoclips(temp_files)
    print("Final video file made, writing to memory")
    final_vid.write_videofile(os.path.join(path, name))
    if cleanup:
        print(f"Cleaning up {filetype} files")
        files = os.listdir(path)
        for file in files:
            if file.endswith(filetype):
                try:
                    os.remove(os.path.join(path, file))
                    # Sometimes we run into permission errors saying that the file is still in use, presumably by our process
                    # I assume this is a bug on the part of moviepy, but to get around it we just don't delete it
                    # These files are rare, so it is trivial to manually delete them afterwards
                except PermissionError:
                    print(f"Couldn't remove file {file}")
        for file in os.listdir(tempfile_path):
            if file.endswith(FINISHED_VIDEO_TYPE):
                try:
                    os.remove(os.path.join(tempfile_path, file))
                except PermissionError:
                    print(f"Couldn't remove file {file}")
        try:
            os.path.remove(os.path.join(tempfile_path))
        except PermissionError:
            print(f"Couldn't remove {tempfile_path}")
    print("Done")


# INPUT: A dictionary formatted as {date1: (video1name, video1link), date2: (video2name, video2link)}, course name, and path for course videos
# Assumes that downloadCourseVids has been called previously with the same inputs
def concatCourseVids(course_dict, course, folder_path):
    dates = course_dict.keys()
    for date in dates:
        # Making the appropriate path for the file
        vid_folder_path = os.path.join(folder_path, course, date)
        concatenate_files(vid_folder_path, course_dict[date][0])


# INPUT: A dictionary of dictionaries formatted as {classname: {date1: (video1name, video1link), date2: (video2name, video2link)}}
# Concatenates all of the video clips into one video file
# This process takes a while
def concatAllCourseVids(all_courses_dict, folder_path=DEFAULT_FOLDER):
    courses = all_courses_dict.keys()
    for course in courses:
        concatCourseVids(
            course_dict=all_courses_dict[course], course=course, folder_path=folder_path
        )


if __name__ == "__main__":
    pass
    # concatenate_files(VIDEO_PATH, "testvid.mp4")
