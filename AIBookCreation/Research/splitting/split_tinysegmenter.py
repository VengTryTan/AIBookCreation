# coding=utf8
from rakutenma import RakutenMA
import tinysegmenter
from nltk import *
import nltk
import re

#segmenter = tinysegmenter.TinySegmenter()
result = tinysegmenter.tokenize(
    "米中間選挙は6日に午後6時（日本時間7日午前8時）に一部の投票所が締め切られ、開票が始まった。米連邦議会の多数党がどちらになるかによって、ドナルド・トランプ米大統領の政策の行方が決まる。特に下院でどれだけ、民主党が共和党現職の議席を奪うかが注目されている。")
print('Segmenter: ')
print(result)

# Initialize a RakutenMA instance with an empty model
# the default ja feature set is set already
rma = RakutenMA()

# Let's analyze a sample sentence (from http://tatoeba.org/jpn/sentences/show/103809)
# With a disastrous result, since the model is empty!
print('Result')
print(rma.tokenize(result))
print('Original')
print(rma.tokenize("米中間選挙は6日に午後6時（日本時間7日午前8時）に一部の投票所が締め切られ、開票が始まった。"))
print('------------------')
# print(rma.tokenize("子どものみなさん、ゆるしてください。ぼくはこの本をひとりのおとなのひとにささげます。でもちゃんとしたわけがあるのです。"))
# print(rma.tokenizetwo("彼は新しい仕事できっと成功するだろう。"))
# print(rma.tokenize("彼は新しい仕事できっと成功するだろう。"))

# Feed the model with ten sample sentences from tatoeba.com
# "tatoeba.json" is available at https://github.com/rakuten-nlp/rakutenma

import json

tatoeba = json.load(open("tatoeba.json", encoding='utf-8'))
j = 0
while (j < 10):
    j += 1
    for i in tatoeba:
        rma.train_one(i)

        # Now what does the result look like?
        # First trained, maybe?
        print('After first trained')
        print('segment')
        print(rma.tokenize(result))
        print('rma')
        print(rma.tokenize(
            "米中間選挙は6日に午後6時（日本時間7日午前8時）に一部の投票所が締め切られ、開票が始まった。米連邦議会の多数党がどちらになるかによって、ドナルド・トランプ米大統領の政策の行方が決まる。特に下院でどれだけ、民主党が共和党現職の議席を奪うかが注目されている。"))

# Initialize a RakutenMA instance with a pre-trained model
rma = RakutenMA(phi=1024, c=0.007812)  # Specify hyperparameter for SCW (for demonstration purpose)
rma.load("model_ja.json")

# Set the feature hash function (15bit)
rma.hash_func = rma.create_hash_func(15)

# Tokenize one sample sentence
print('Tokenize simple sentence')
print(rma.tokenize("うらにわにはにわにわとりがいる"));

# Re-train the model feeding the right answer (pairs of [token, PoS tag])
res = rma.train_one(
    [["うらにわ", "N-nc"],
     ["に", "P-k"],
     ["は", "P-rj"],
     ["にわ", "N-n"],
     ["にわとり", "N-nc"],
     ["が", "P-k"],
     ["いる", "V-c"]])
# The result of train_one contains:
#   sys: the system output (using the current model)
#   ans: answer fed by the user
#   update: whether the model was updated
print('After changes')
print(res)

# Now what does the result look like?
print('Result')
print(rma.tokenize("子どものみなさん、ゆるしてください。ぼくはこの本をひとりのおとなのひとにささげます。でもちゃんとしたわけがあるのです。"))

print('Frequency of Words')
fdist1 = FreqDist(result)
print(fdist1.most_common(50))

print('Entity of Words')
results = (tinysegmenter.tokenize("レオン・ウェルトに子どものみなさん、ゆるしてください。ぼくはこの本をひとりのおとなのひとにささげます。でもちゃんとしたわけがあるのです。そのおとなのひとは、ぼくのせかいでいちばんの友だちなんです。それにそのひとはなんでもわかるひとで、子どもの本もわかります。しかも、そのひとはいまフランスにいて、さむいなか、おなかをへらしてくるしんでいます。心のささえがいるのです。まだいいわけがほしいのなら、このひともまえは子どもだったので、ぼくはその子どもにこの本をささげることにします。おとなはだれでも、もとは子どもですよね。（みんな、そのことをわすれますけど。）じゃあ、ささげるひとをこう書きなおしましょう。"))
print(results)
entities = nltk.ne_chunk(results)
print(entities)
