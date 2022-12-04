from courseLinks import getAllInfo
from downloader import downloadAllCourseVids, downloadCourseFiles
from videoMaker import concatAllCourseVids
from get_progress import get_progress
from constants import *
import getpass, os


def main():
    get_new_vids = input(
        "Fetch all course video links again?  This process is unnecessary if there are no new lectures from last time the program was run (Y/N)"
    ).upper()
    while get_new_vids != "Y" and get_new_vids != "N":
        get_new_vids = input("Please enter Y (for yes) or N (for no)").upper()
    get_new_files = input(
        "Fetch all course file links again?  This process is unnecessary if there are no new files from last time the program was run (Y/N)"
    ).upper()
    while get_new_files != "Y" and get_new_files != "N":
        get_new_files = input("Please enter Y (for yes) or N (for no)").upper()
    if get_new_vids == "Y" or get_new_files == "Y":
        get_new_vids = get_new_vids == "Y"
        get_new_files = get_new_files == "Y"
        username = input("Username: ")
        password = getpass.getpass()
        vid_dict, file_dict = getAllInfo(
            username, password, get_new_vids, get_new_files
        )
        if get_new_vids:
            with open(VIDEO_DICT_LOCATION, "w") as course_file:
                course_file.write(str(vid_dict))
        if get_new_files:
            with open(FILE_DICT_LOCATION, "w") as course_file:
                course_file.write(str(file_dict))
    # We save the links in a text file in case we want to stop here and resume later
    with open(VIDEO_DICT_LOCATION, "r") as dict_file:
        test_dict = eval(dict_file.read())
        test_dict = get_progress(test_dict, VID_FOLDER)
        downloadAllCourseVids(test_dict, VID_FOLDER)
        concatAllCourseVids(test_dict, VID_FOLDER)
    with open(FILE_DICT_LOCATION, "r") as dict_file:
        test_dict = eval(dict_file.read())
        downloadCourseFiles(test_dict, FILE_FOLDER)


if __name__ == "__main__":
    main()
