import mss as MSS
import datetime as DT
import PIL.Image as IMG

def main():
    sct = MSS.mss()
    monitor = {"left" : 5, "top" : 115, "width" : 775, "height" : 585}
    
    fight_mask_black = IMG.open("D:\\Git\\street-fighter-agent\\resource\\fight_masking_black.png")
    fight_mask = IMG.open("D:\\Git\\street-fighter-agent\\resource\\fight_masking_color.png")
    fight_mask = fight_mask.convert("RGB")
    fight_mask_hash_value = hash(fight_mask.tobytes())

    you_lose_mask_black = IMG.open("D:\\Git\\street-fighter-agent\\resource\\win_masking_black.png")
    you_lose_mask = IMG.open("D:\\Git\\street-fighter-agent\\resource\\win_masking_color.png")
    you_lose_mask = you_lose_mask.convert("RGB")
    you_lose_mask_hash_value = hash(you_lose_mask.tobytes())

    you_win_mask_black = IMG.open("D:\\Git\\street-fighter-agent\\resource\\lose_masking_black.png")
    you_win_mask = IMG.open("D:\\Git\\street-fighter-agent\\resource\\lose_masking_color.png")
    you_win_mask = you_win_mask.convert("RGB")
    you_win_mask_hash_value = hash(you_win_mask.tobytes())

    background = IMG.new("RGB", (775, 585), color="white")

    time_start = DT.datetime.now()
    
    sct_img = sct.grab(monitor)
    capture = IMG.frombytes("RGB", sct_img.size, sct_img.rgb, "raw")
    image = IMG.composite(capture, background, fight_mask_black)
    # image = IMG.composite(capture, background, you_lose_mask_black)
    # image = IMG.composite(capture, background, you_win_mask_black)

    image_bytes = image.tobytes()
    hash_value = hash(image_bytes)

    if hash_value == fight_mask_hash_value:
        print("round starts : fight")
    elif hash_value == you_win_mask_hash_value:
        print("round ends : win")
    elif hash_value == you_lose_mask_hash_value:
        print("round ends : lose")
    else:
        print("not matched")

    time_end = DT.datetime.now()
    interval = (time_end - time_start).total_seconds() * 1000
    print("{} ms".format(interval))

if __name__ == "__main__":
    main()