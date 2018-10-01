import ImageManager as IM
import datetime as DT

def main():
    im = IM.ImageManager()

    while True:
        time_start = DT.datetime.now()

        im.Capture()
        im.Masking()
        im.RoundState()

        time_end = DT.datetime.now()
        interval = (time_end - time_start).total_seconds() * 1000
        print("{} ms \n".format(interval))

if __name__ == "__main__":
    main()
    print("\n\t DONE")

    