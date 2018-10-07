import mss as MSS
import PIL.Image as IMG

class ImageManager:
    
    def __init__(self):
        # mss instance
        self.screenshot = MSS.mss()
        # variables for checking round state
        self.monitor = {"left" : 5, "top" : 115, "width" : 775, "height" : 585}
        self.fight_masking_black = IMG.open("D:\\Git\\street-fighter-agent\\resource\\fight_masking_black.png")
        self.fight_masking_color = IMG.open("D:\\Git\\street-fighter-agent\\resource\\fight_masking_color.png").convert("RGB")
        self.fight_masking_color_hash = hash(self.fight_masking_color.tobytes())
        self.win_masking_black = IMG.open("D:\\Git\\street-fighter-agent\\resource\\win_masking_black.png")
        self.win_masking_color = IMG.open("D:\\Git\\street-fighter-agent\\resource\\win_masking_color.png").convert("RGB")
        self.win_masking_color_hash = hash(self.win_masking_color.tobytes())
        self.lose_masking_black = IMG.open("D:\\Git\\street-fighter-agent\\resource\\lose_masking_black.png")
        self.lose_masking_color = IMG.open("D:\\Git\\street-fighter-agent\\resource\\lose_masking_color.png").convert("RGB")
        self.lose_masking_color_hash = hash(self.lose_masking_color.tobytes())
        self.background = IMG.new("RGB", (775, 585), color="white")
        self.round_state = 0
        self.round_state_dict = {0:"Not Matched", 1:"Starts, Fight", 2:"Ends, You Win", 3:"Ends, You Lose"}
        # variables for checking hp value
        self.box_p1_hp = (99, 65, 99 + 264, 65 + 1)
        self.p1_hp = -1
        self.box_p2_hp = (411, 65, 411 + 264, 65 + 1)
        self.p2_hp = -1

    def Capture(self):
        # capture the section & save it
        self.capture = self.screenshot.grab(self.monitor)
        self.capture = IMG.frombytes("RGB", self.capture.size, self.capture.rgb, "raw")

    def ReadRoundState(self):
        # making masked image & its hash value
        fight_masked_image = IMG.composite(self.capture, self.background, self.fight_masking_black)
        fight_masked_image_hash = hash(fight_masked_image.tobytes())
        win_masked_image = IMG.composite(self.capture, self.background, self.win_masking_black)
        win_masked_image_hash = hash(win_masked_image.tobytes())
        lose_masked_image = IMG.composite(self.capture, self.background, self.lose_masking_black)
        lose_masked_image_hash = hash(lose_masked_image.tobytes())
        # checking which state it is
        if fight_masked_image_hash == self.fight_masking_color_hash:
            self.round_state = 1
        elif win_masked_image_hash == self.win_masking_color_hash:
            self.round_state = 2
        elif lose_masked_image_hash == self.lose_masking_color_hash:
            self.round_state = 3
        else:
            self.round_state = 0

    def PrintRoundState(self):
        print("Round State : {}".format(self.round_state_dict[self.round_state]))

    def ReadHP(self):
        # read player #1's HP
        img_p1_hp = self.capture.crop(self.box_p1_hp)
        list_p1_hp = list(img_p1_hp.getdata())
        self.p1_hp = 0
        for i in range(len(list_p1_hp)):
            if list_p1_hp[i] == (247, 219, 0):
                self.p1_hp += 1
        # read player #2's HP
        img_p2_hp = self.capture.crop(self.box_p2_hp)
        list_p2_hp = list(img_p2_hp.getdata())
        self.p2_hp = 0
        for i in range(len(list_p2_hp)):
            if list_p2_hp[i] == (247, 219, 0):
                self.p2_hp += 1

    def PrintHP(self):
        print("Player #1 HP : {}".format(self.p1_hp))
        print("Player #2 HP : {}".format(self.p2_hp))