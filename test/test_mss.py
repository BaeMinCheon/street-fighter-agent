import mss
import datetime as DT

def main():
    time_start = DT.datetime.now()

    sct = mss.mss()
    
    # monitor = {"left" : 5, "top" : 115, "width" : 775, "height" : 585}
    # output = "D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_total.png".format(**monitor)
    # sct_img = sct.grab(monitor)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    # monitor = {"left" : 100, "top" : 150, "width" : 275, "height" : 35}
    # output = "D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_1p_hp.png".format(**monitor)
    # sct_img = sct.grab(monitor)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    # monitor = {"left" : 410, "top" : 150, "width" : 275, "height" : 35}
    # output = "D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_2p_hp.png".format(**monitor)
    # sct_img = sct.grab(monitor)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    # monitor = {"left" : 315, "top" : 285, "width" : 155, "height" : 55}
    # output = "D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_fight.png".format(**monitor)
    # sct_img = sct.grab(monitor)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    # monitor = {"left" : 285, "top" : 265, "width" : 210, "height" : 50}
    # output = "D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_you_win.png".format(**monitor)
    # sct_img = sct.grab(monitor)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    # monitor = {"left" : 285, "top" : 265, "width" : 210, "height" : 50}
    # output = "D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_you_lose.png".format(**monitor)
    # sct_img = sct.grab(monitor)
    # mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    time_end = DT.datetime.now()
    interval = (time_end - time_start).total_seconds() * 1000
    print("{} ms".format(interval))

if __name__ == "__main__":
    main()