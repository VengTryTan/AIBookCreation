# coding=utf8
from glob import iglob
import MeCab



def load_from_file_list(files_pattern):
    """ read and get text in line of file which store as a list and return

        :param files_pattern: 'name_file_as_txt'
        :return: the line list in sentence
    """

    line_list = list()

    with open(files_pattern, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            line_list.append(line)

        return line_list



def split_sentence(text):
    """ split text to sentences by newline, and split sentence to words by space.

        :param text: string of text to split
        :return: text of sentence by line
    """

    # separate words using mecab
    mecab = MeCab.Tagger()
    tagger = MeCab.Tagger("-Owakati")

    # split_text as string of all sentence
    split_text = str()

    if not text:

        print("String is empty.")

        return split_text

    else:

        # make text parse by mecab
        text_parse = tagger.parse(text)

        # identify the word character is quote in sentence
        check_char = 0

        # these chars might break markovify
        # https://github.com/jsvine/markovify/issues/84
        breaking_chars = [
            '(',
            ')',
            '[',
            ']',
            '"',
            "'", ]

        # character end of the sentence
        end_chars = [
            '。',
            '！',
            '？'
        ]

        # split whole text to sentences by newline, and split sentence to words by space.
        # 　nodeには単語、surfaceには品詞などの特徴が入っている
        for line in text_parse.split():

            # get word in line using mecab
            mp = mecab.parseToNode(line)

            # each word in line
            while mp:

                # try if unicodeDecodeError
                try:

                    # check if the word is not breaking_character
                    if mp.surface not in breaking_chars:  # skip if node is markovify breaking char　単語に品詞を与える

                        # if the word is not in quote
                        if check_char == 0:

                            # if word is end of sentence
                            if mp.surface in end_chars:

                                split_text += mp.surface + '\n'  # represent sentence by newline　読点が来たら次の行

                            # if word is start quote is identify the next word in quote
                            elif mp.surface == "「":

                                check_char = 1
                                split_text += mp.surface

                            # if the word is 、 add it with not space
                            elif mp.surface == "、":

                                split_text += mp.surface

                            # if the word is end quote not add to the text
                            elif mp.surface == "」":

                                pass
                            else:

                                split_text += mp.surface + ' '  # split words by space　句点が来たら一つ空ける

                        # if the word in quote
                        elif check_char == 1:

                            if mp.surface in end_chars:

                                split_text += mp.surface + '」\n「'  # represent sentence by newline　読点が来たら次の行
                            elif mp.surface == "」":

                                check_char = 0
                                split_text = split_text[:-1]
                            elif mp.surface == "、":

                                split_text += mp.surface
                            else:
                                split_text += mp.surface + ' '  # split words by space　句点が来たら一つ空ける
                    else:
                        pass

                except UnicodeDecodeError:

                    # sometimes error occurs
                    # 　エラーが起こった時は次に行く
                    pass
                finally:

                    # get the next word in line
                    mp = mp.next

        return split_text


