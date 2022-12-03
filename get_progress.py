from constants import *
import os, copy

# INPUT: A dictionary of dictionaries formatted as {classname: {date1: (video1name, video1link), date2: (video2name, video2link)}}, a path to a folder
# OUTPUT: A dictionary with a course dictionary (formatted like the one passed) for the downloads that need to be completed and the concatenations that need to be completed
def get_progress(all_courses_dict, folder_path=DEFAULT_FOLDER):
    to_return = copy.deepcopy(all_courses_dict)
    # Iterating through the course_dict to check if any folders don't exist
    for className in all_courses_dict.keys():
        course_dict = all_courses_dict[className]
        for date in course_dict.keys():
            # If the folder hasn't been made, it both needs to be downloaded as well as concatenated
            vid_folder = os.path.join(folder_path, className, date)
            if os.path.exists(vid_folder):
                # Checking if the completed video file exists
                completed_file = os.path.join(vid_folder, course_dict[date][0])
                if os.path.exists(completed_file):
                    to_return[className].pop(date)
    # Because the download function will only download new clips, if all the clips are downloaded in the folder, it will do nothing
    return to_return
