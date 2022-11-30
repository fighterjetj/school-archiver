import requests, os, re, datetime

# Bruinlearn media is stored sequentially, with 0.ts being the first couple seconds of the video
URL = "https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20221109-27311.mp4/media_w1066734084_tkd293emF0b2tlbmVuZHRpbWU9MTY2ODY4MDcyOSZ3b3d6YXRva2VuaGFzaD12RnNXaUNQbTNYejRyaldHcXhzT3hDLXI5OXh1RGxiOUJUcjYyalY4V1RrPQ==_0.ts"
link = "https://bclive.oid.ucla.edu/2022f-v/mp4:cs35l-1-20221109-27311.mp4/media_w1066734084_tkd293emF0b2tlbmVuZHRpbWU9MTY2ODY4MDcyOSZ3b3d6YXRva2VuaGFzaD12RnNXaUNQbTNYejRyaldHcXhzT3hDLXI5OXh1RGxiOUJUcjYyalY4V1RrPQ==_"


def get_videos(
    start_link,
    source_url="https://bclive.oid.ucla.edu/",
    file_type=".ts",
    video_name=None,
    download_chunks=1024 * 1024,
    parent_dir="vid_folders/",
    update_interval=50,
):
    # Checking the link comes from bclive.oid.ucla.edu
    if start_link[: len(source_url)] != source_url:
        raise Exception("Passed link does not match the intended source")
    # Checking it is a link to a .ts file
    if start_link[-len(file_type) :] != file_type:
        raise Exception(f"Not a {file_type} file url")
    base_link = start_link[: -len(file_type)]
    # Stripping the filenumber off the end of the link
    while base_link[-1].isnumeric():
        base_link = base_link[:-1]
    # Getting the overall video .mp4 name
    if not video_name:
        video_name = str(datetime.datetime.now()).replace(" ", "")
        # video_name = re.findall("mp4:.*.mp4", URL)[0][4:-4]
    """
    video_ver = 0
    directoryNameTaken = False
    """
    vid_path = os.path.join(parent_dir, video_name)
    # Making a directory to store the video files
    try:
        os.makedirs(vid_path)
        print("Made folder for videos")
    except FileExistsError:
        raise Exception("Already have a file for that video")
        """
        if directoryNameTaken:
            video_ver += 1
            video_name = video_name[:-len(str(video_ver-1))] + str(video_ver)
        else:
            directoryNameTaken = True
            video_name = video_name + "v1"
        """
    curr_vid = 0
    video_file = requests.get(base_link + str(curr_vid) + ".ts", stream=True)
    # As long as the video file exists, we want to download
    while video_file.status_code == 200:
        with open(f"{parent_dir}/{video_name}/{curr_vid}.ts", "wb") as vid:
            for chunk in video_file.iter_content(chunk_size=download_chunks):
                if chunk:
                    vid.write(chunk)
        if curr_vid % update_interval == 0:
            print(f"Finished downloading video file #{curr_vid}")
        curr_vid += 1
        video_file = requests.get(base_link + str(curr_vid) + ".ts", stream=True)
    print("All videos downloaded!")


if __name__ == "__main__":
    get_videos(URL)
