import cv2, pafy

def get_video(url):
    video = pafy.new(url)
    best = video.getbest(preftype='mp4')
    vf = cv2.VideoCapture(best.url)

    return vf 