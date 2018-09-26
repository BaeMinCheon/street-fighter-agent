import pyscreenshot as PS
import datetime as DT

if __name__ == "__main__":
    time_start = DT.datetime.now()

    # img_fight = PS.grab(bbox=(300, 280, 470, 350))
    # img_fight.save("D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_fight.png")

    # img_you_win_lose = PS.grab(bbox=(280, 250, 500, 320))
    # img_you_win_lose.save("D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_you_win_lose.png")

    # img_1p_hp = PS.grab(bbox=(90, 150, 370, 190))
    # img_1p_hp.save("D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_1p_hp.png")

    # img_2p_hp = PS.grab(bbox=(400, 150, 680, 190))
    # img_2p_hp.save("D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_2p_hp.png")

    img_total = PS.grab(bbox=(0, 110, 770, 700))
    img_total.save("D:\\Study\\7.VHPC\\reinforcement_leraning\\StreetFighter2WW\\code\\test\\resource\\img_total.png")

    time_end = DT.datetime.now()
    interval = (time_end - time_start).total_seconds() * 1000
    print("{} ms".format(interval))