# school-archiver

Tool for archiving course materials (specifically lectures)

**File downloading functionality is currently not working.  It will be working soon.**

## Running the program:

- Create a virtual environment with the python packages in requirements.txt
- I recommend changing the VID_FOLDER and FILE_FOLDER variables in constants.py to the path for whatever file you would like to use
- If you want to change what video file type is used for the final lectures, feel free to change FINISHED_VIDEO_TYPE in constants.py
- Make sure you have a webdriver downloaded for the browser you want to use - see https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#4-hard-coded-location
- Change WEBDRIVER_LOCATION in constants.py to the path to the directory that contains the Chrome webdriver
- I used Chrome and have not tested this code with other browsers
- If you want to use a different browser, which is not recommended, change line 136 of courseLinks.py to use whatever browser you wish
- Run main.py
- If this is your first time running the program or you have new lectures, answer yes to the prompt asking you if you want to fetch all course video links again
- Same for course files
- Input your bruinlearn username and password
- Do your duo authentication and after that it should run without your input
- Notably, Selenium does not function unless the chrome window is the active one, so leave the window up on your screen until it closes itself

## Other Info:

- This process takes a while
- It is much quicker to just download course files, usually taking around a minute total, including getting the links
- Try and have a minimum of several hours to run all the code at once
- As long as the Chrome window is open, the program is still compiling its list of links to videos
- The Chrome window should not be open for more than a few (5-10) minutes
- Once the window closes, you can use your computer for other things
- The longest part of the process is concatenating the video files into one
- The code should work after a partially completed or prior run of the program, however this has not been exhaustively tested

## How it works

- We use selenium-wire so that we can listen to requests
- We compile all the urls of the videos to download into a dictionary which is then saved to a local text file, allowing it to be reused
- Bruinlearn sends the lecture videos to the browser in small, couple second clips
- We iterate through all those clips and download them
- We concatenate all those clips into one video file and then delete them
- The video files are saved in folders as mp4 files, formatted as follows:
- classname/dateoflecture/videofilename.mp4
