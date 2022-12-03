from courseLinks import getAllCourseVideoLinks
from downloader import downloadAllCourseVids
from videoMaker import concatAllCourseVids
from get_progress import get_progress
from constants import *
import getpass, os


MY_FOLDER = os.path.join("E:", "SchoolArchiving", "vid_folders")


def main():
    get_new_dict = input(
        "Fetch all course video links again?  This process is unnecessary if there are no new lectures from last time the program was run (Y/N)"
    )
    while get_new_dict.upper() != "Y" and get_new_dict.upper() != "N":
        get_new_dict = input("Please enter Y (for yes) or N (for no)")
    if get_new_dict.upper() == "Y":
        username = input("Username: ")
        password = getpass.getpass()
        all_courses_dict = getAllCourseVideoLinks(username, password)
        with open(COURSE_DICT_LOCATION, "w") as coursefile:
            coursefile.write(str(all_courses_dict))
    # We save the links in a text file in case we want to stop here and resume later
    with open(COURSE_DICT_LOCATION, "r") as dictfile:
        test_dict = eval(dictfile.read())
        test_dict = get_progress(test_dict, MY_FOLDER)
        downloadAllCourseVids(test_dict, MY_FOLDER)
        concatAllCourseVids(test_dict, MY_FOLDER)


if __name__ == "__main__":
    main()
