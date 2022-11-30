# school-archiver
Tool for archiving course materials (specifically lectures)
RUNNING THE CODE:
Create a virtual environment with the python packages in requirements.txt
Make sure you have a webdriver downloaded for the browser you want to use
- I used Chrome and have not tested this code with other browsers
- Chrome is the only one confirmed to work
Run main.py
Input your bruinlearn username and password
Do your duo authentication and after that it should run without your input

IMPORTANT TO KNOW:
This process takes a while
Try and have a minimum of several hours to run all the code
The longest part of the process is concatenating the video files into one
Currently the code is not designed to work with a partially completed run, you'll have to start over
If you want, you can just run the uncompleted steps by not calling the already completed functions
This currently requires manually editing the code
For best results, delete any already created files by the program that are incomplete
Ex: If failing during video concatenation, delete any tempfiles

ABOUT:
We use selenium-wire so that we can listen to requests
We compile all the urls of the videos to download
Bruinlearn sends the lecture videos to the browser in small, couple second clips
We iterate through all those clips and download them
We concatenate all those clips into one video file and then delete them
The video files are saved in folders as mp4 files, formatted as follows:
- classname/month/date/year/videofilename/videofilename.mp4

FUTURE PLANS:
Seamlessly resume from partially complete runs of the program
Greater control over folder structure
Downloading of other bruinlearn processes
