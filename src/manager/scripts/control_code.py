if feature['Winner.Player'] == 0:
	if feature['P1.CanControl'] == 1:
		pass
	else:
		control = [0, 0, 0]
else:
	if self.count_frame >= 60:
		self.count_frame = 0
		control = [0, 0, 2]
	else:
		control = [0, 0, 0]

feature['Reward'] = feature['Gap.HP.P1.Diff'] - feature['Gap.X.Diff']