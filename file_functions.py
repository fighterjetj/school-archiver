from course_links import duoMobileLogin, makeDriver
from constants import *
import requests, os, datetime, getpass, time


def downloadCourseFile(file_url, path, requests_session, download_chunks=1024 * 1024):
    file = requests_session.get(file_url)
    with open(path, "wb") as file_to_write:
        for chunk in file.iter_content(chunk_size=download_chunks):
            file_to_write.write(chunk)


# INPUT: A dictionary that represents a filetree, with download links for the files and subdictionaries for the subdirectories, and a file path
# Downloads all the course files in a corresponding tree at the location passed
def downloadCourseFiles(
    file_dict,
    path,
    download_chunks=1024 * 1024,
):
    # If no files, do nothing
    if len(file_dict) == 0:
        return
    try:
        os.makedirs(path)
    except FileExistsError:
        print(f"Folder at path {path} already exists")
    print(f"Downloading content to f{path}")
    files = file_dict.keys()
    for file in files:
        # Getting rid of any slashes
        fileName = file.replace("/", "-")
        fileName = fileName.replace("\\", "-")
        file_path = os.path.join(path, fileName)
        file_info = file_dict[file]
        if type(file_info) == dict:
            downloadCourseFiles(file_dict[file], file_path)
        # If the file already exists but it isn't a directory, we don't redownload it
        elif not os.path.exists(file_path):
            full_file = requests.get(file_info, stream=True)
            with open(file_path, "wb") as file_to_write:
                for chunk in full_file.iter_content(chunk_size=download_chunks):
                    if chunk:
                        file_to_write.write(chunk)
        else:
            print(f"Already downloaded {file_path}")
    print(f"Finished downloading content to {path}")


def flattenFileDict(file_dict):
    to_return = []
    for file in file_dict:
        if type(file_dict[file]) == dict:
            to_return += flattenFileDict(file_dict[file])
        else:
            to_return.append(file_dict[file])
    return to_return


"""
def downloadCourseFilesUsingSelenium(file_dict, path):
    if len(file_dict) == 0:
        return
    try:
        os.makedirs(path)
    except FileExistsError:
        print(f"Folder at path {path} already exists")
    flat_file_dict = flattenFileDict(file_dict)
    # print(flat_file_dict)
    password = getpass.getpass()
    driver = makeDriver()
    duoMobileLogin("", password, driver, SITE)
    time.sleep(5)
    print("Getting!")
    for url in flat_file_dict:
        driver.get(url)
        time.sleep(1)
"""
