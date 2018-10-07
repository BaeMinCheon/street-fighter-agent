import mss as MSS
import datetime as DT
import PIL.Image as IMG

def main():
    sct = MSS.mss()
    monitor = {"left" : 5, "top" : 115, "width" : 775, "height" : 585}
    box_p1_hp = (99, 65, 99 + 264, 65 + 1)
    box_p2_hp = (411, 65, 411 + 264, 65 + 1)

    time_start = DT.datetime.now()
    
    sct_img = sct.grab(monitor)
    capture = IMG.frombytes("RGB", sct_img.size, sct_img.rgb, "raw")
    img_p1_hp = capture.crop(box_p1_hp)
    img_p2_hp = capture.crop(box_p2_hp)

    time_end = DT.datetime.now()
    interval = (time_end - time_start).total_seconds() * 1000
    print("{} ms".format(interval))

    list_p1_hp = list(img_p1_hp.getdata())
    list_p2_hp = list(img_p2_hp.getdata())
    
    score_p1 = 0
    for i in range(len(list_p1_hp)):
        if list_p1_hp[i] == (247, 219, 0):
            score_p1 += 1
    print("score_p1 : {}".format(score_p1))

    score_p2 = 0
    for i in range(len(list_p2_hp)):
        if list_p2_hp[i] == (247, 219, 0):
            score_p2 += 1
    print("score_p2 : {}".format(score_p2))

if __name__ == "__main__":
    main()