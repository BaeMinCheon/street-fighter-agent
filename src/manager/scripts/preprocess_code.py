feature['P1.Position.X'] = data['P1.Position.X']
feature['P1.Position.Y'] = 192 - data['P1.Position.Y.Raw']
feature['P1.HP.Current'] = data['P1.HP.Current']
if data['P1.IsAttacking.Raw'] >= 256:
    feature['P1.IsAttacking'] = 1
else:
    feature['P1.IsAttacking'] = 0
if data['P1.IsHitting.Raw'] >= 256:
    feature['P1.IsHitting'] = 1
else:
    feature['P1.IsHitting'] = 0
if (feature['P1.IsAttacking'] + feature['P1.IsHitting']) == 0:
    feature['P1.CanControl'] = 1
else:
    feature['P1.CanControl'] = 0
feature['P2.Position.X'] = data['P2.Position.X']
feature['P2.Position.Y'] = 192 - data['P2.Position.Y.Raw']
feature['P2.HP.Current'] = data['P2.HP.Current']
if feature['P1.Position.X'] > feature['P2.Position.X']:
    feature['P1.IsLeft'] = 1
else:
    feature['P1.IsLeft'] = 0
feature['Gap.X'] = abs(feature['P1.Position.X'] - feature['P2.Position.X'])
feature['Gap.Y'] = abs(feature['P1.Position.Y'] - feature['P2.Position.Y'])
feature['Gap.HP.P1'] = feature['P1.HP.Current'] - feature['P2.HP.Current']
if feature['P1.CanControl'] > 0:
    feature['P1.CanAction'] = 1
    if feature['P1.Position.Y'] == 0:
        feature['P1.CanMove'] = 1
    else:
        feature['P1.CanMove'] = 0
else:
    feature['P1.CanAction'] = 0
    feature['P1.CanMove'] = 0
feature['RoundTimer'] = data['RoundTimer']
if data['Winner.Player.Raw'] > 0:
    feature['Winner.Player'] = 1
else:
    feature['Winner.Player'] = 0
feature['Reward'] = feature['Gap.HP.P1']