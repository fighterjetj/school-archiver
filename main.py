from course_links import getAllInfo
from video_functions import downloadAllCourseVids, downloadCourseFiles
from videoMaker import concatAllCourseVids
from get_progress import get_progress
from constants import *
import getpass, os


def main():
    download_vids = input("Do you want to download course videos? (Y/N)\n").upper()
    while download_vids != "Y" and download_vids != "N":
        download_vids = input("Please enter Y (for yes) or N (for no)\n").upper()
    download_vids = download_vids == "Y"
    download_files = input(
        "Do you want to download course files? (Y/N) (NOTE - THIS FUNCTIONALITY IS CURRENTLY NOT PROPERLY UNIMPLEMENTED.  THIS WILL NOT WORK\n"
    ).upper()
    while download_files != "Y" and download_files != "N":
        download_files = input("Please enter Y (for yes) or N (for no)\n").upper()
    download_files = download_files == "Y"
    get_new_vids = input(
        "Fetch all course video links again?  This process is unnecessary if there are no new lectures from last time the program was run (Y/N)\n"
    ).upper()
    while get_new_vids != "Y" and get_new_vids != "N":
        get_new_vids = input("Please enter Y (for yes) or N (for no)\n").upper()
    get_new_vids = get_new_vids == "Y"
    get_new_files = input(
        "Fetch all course file links again?  This process is unnecessary if there are no new files from last time the program was run (Y/N)\n"
    ).upper()
    while get_new_files != "Y" and get_new_files != "N":
        get_new_files = input("Please enter Y (for yes) or N (for no)\n").upper()
    get_new_files = get_new_files == "Y"
    if get_new_vids or get_new_files:
        username = input("Username: ")
        password = getpass.getpass()
        vid_dict, file_dict = getAllInfo(
            username, password, get_new_vids, get_new_files
        )
        # We save the links in a text file in case we want to stop here and resume later
        if get_new_vids:
            with open(VIDEO_DICT_LOCATION, "w") as course_file:
                course_file.write(str(vid_dict))
        if get_new_files:
            with open(FILE_DICT_LOCATION, "w") as course_file:
                course_file.write(str(file_dict))
    if download_vids:
        with open(VIDEO_DICT_LOCATION, "r") as dict_file:
            test_dict = eval(dict_file.read())
            test_dict = get_progress(test_dict, VID_FOLDER)
            downloadAllCourseVids(test_dict, VID_FOLDER)
            concatAllCourseVids(test_dict, VID_FOLDER)

    if download_files:
        with open(FILE_DICT_LOCATION, "r") as dict_file:
            test_dict = eval(dict_file.read())
            downloadCourseFiles(test_dict, FILE_FOLDER)


if __name__ == "__main__":
    main()
