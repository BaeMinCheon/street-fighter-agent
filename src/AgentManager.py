import ImageManager as IM

class AgentManager:

    def __init__(self):
        self.IM = IM.ImageManager()

    def PreProcess(self):
        self.IM.Capture()
        self.IM.ReadRoundState()
        self.IM.PrintRoundState()
        self.IM.ReadHP()
        self.IM.PrintHP()
        # separator
        print()
    
    def Train(self):
        pass