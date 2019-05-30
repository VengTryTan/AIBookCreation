# -*- coding: utf-8 -*-
# from mlask import MLAsk
# emotion_analyzer = MLAsk()
# sentiment= emotion_analyzer.analyze('彼のことは嫌いではない！(;´Д`)')
# print(sentiment)

# -*- coding: utf-8 -*-
from mlask import MLAsk


emotion_analyzer = MLAsk()

print(emotion_analyzer.analyze('彼のことは嫌いではない！(;´Д`)'))