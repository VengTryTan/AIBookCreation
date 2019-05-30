from TrainingModel.trainModel import train_model
from Cleansing.split import split_sentence
from glob import iglob
import os


def load_from_file(files_pattern):
    """ read and merge files which matches given file pattern, prepare for parsing and return it.

        :param: files_pattern: 'name_file_as_txt'
        :return: text in string
    """

    # read text
    text = ""
    for path in iglob(files_pattern):
        with open(path, 'r') as f:
            text += f.read().strip()

    return text

# file path
path_file = "Data/little_prince.txt"
path_allNovel = "Data/allNovel.txt"

try:
    # check of it is a file
    check_file = open(path_file, 'r', encoding='utf-8')
    check_file_allNovel = open(path_allNovel, 'r', encoding='utf-8')

    # check file of text file
    file = os.path.splitext(path_file)[-1].lower()
    file_allNovel = os.path.splitext(path_allNovel)[-1].lower()

    if file == '.txt' and file_allNovel == ".txt":

        # read file and make it to string
        text_file = load_from_file(path_file)
        text_allNovel = load_from_file(path_allNovel)

        # split sentence in file and make the list of sentence
        text_file_sentence = split_sentence(text_file)
        file_sentence = text_file_sentence.split("\n")
        text_allNovel_sentence = split_sentence(text_allNovel)
        allNovel_sentence = text_allNovel_sentence.split("\n")

        # check the data
        if allNovel_sentence is None and file_sentence is None:

            print ("No data in file.")

        else:

            # get length of data and sum all data to train
            length_data_file = len(file_sentence)
            data = file_sentence + allNovel_sentence

            # train the data to get sentence from allNovel
            result = train_model(data, length_data_file)

            if not result:

                print ("data is empty.")

            else:

                # print sentence and write data to file
                f = open('epoch(text).txt', 'w+')
                for sentence in result:

                    f.write(sentence)
                    print (sentence)

    else:

        print("File is not text file.")
except FileNotFoundError:

    print("File path not found")
