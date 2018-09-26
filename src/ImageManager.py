import mss as MSS
import PIL.Image as IMG

class ImageManager:
    
    def __init__(self):
        self.screenshot = MSS.mss()
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
    
    def Capture(self):
        self.capture = self.screenshot.grab(self.monitor)
        self.capture = IMG.frombytes("RGB", self.capture.size, self.capture.rgb, "raw")

    def Masking(self):
        self.fight_masked_image = IMG.composite(self.capture, self.background, self.fight_masking_black)
        self.fight_masked_image_hash = hash(self.fight_masked_image.tobytes())
        self.win_masked_image = IMG.composite(self.capture, self.background, self.win_masking_black)
        self.win_masked_image_hash = hash(self.win_masked_image.tobytes())
        self.lose_masked_image = IMG.composite(self.capture, self.background, self.lose_masking_black)
        self.lose_masked_image_hash = hash(self.lose_masked_image.tobytes())

    def RoundState(self):
        if self.fight_masked_image_hash == self.fight_masking_color_hash:
            print("round starts : fight")
        elif self.win_masked_image_hash == self.win_masking_color_hash:
            print("round ends : win")
        elif self.lose_masked_image_hash == self.lose_masking_color_hash:
            print("round ends : lose")
        else:
            print("not matched")
