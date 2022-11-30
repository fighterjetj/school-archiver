from courseLinks import getAllCourseVideoLinks
from downloader import downloadAllCourseVids
from videoMaker import concatAllCourseVids
import getpass


def main():
    username = input("Username: ")
    password = getpass.getpass()
    all_courses_dict = getAllCourseVideoLinks(username, password)
    with open("Course_dict.txt", "w") as coursefile:
        coursefile.write(str(all_courses_dict))
    # We save the links in a text file in case we want to stop here and resume later
    with open("course_dict.txt", "r") as dictfile:
        testdict = eval(dictfile.read())
        downloadAllCourseVids(testdict)
        concatAllCourseVids(testdict)


if __name__ == "__main__":
    main()
