from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from glob import iglob



def train_model(data, length_sentence):
    """
    Function to take the data from file and compare most similar sentence and return new sentence

    :param length_sentence: length of sentence in data file to compare
    :param data: data to train
    :return: new data that have same pattern
    """


    data_list = []
    if not data and not length_sentence:

        print("Data is empty.")

        return data_list

    else:

        # tagged data and set the round of training
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
        max_epochs = 10
        vec_size = 12
        alpha = 0.025

        # Training Model
        model = Doc2Vec(vector_size=vec_size,
                        alpha=alpha,
                        min_alpha=0.00025,
                        min_count=1,
                        dm=1)

        # build vocab of model
        model.build_vocab(tagged_data)

        for epoch in range(max_epochs):
            # print('iteration {0}'.format(epoch))
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha

        # save Model
        model.save("d2v.model")
        model = Doc2Vec.load("d2v.model")

        # to find most similar doc using tags
        count = 0
        array_int = []

        # get the data similar of each sentence
        for i in data:

            similar_doc = model.docvecs.most_similar(count)

            # most similar data
            for similar in similar_doc:

                int_t = int(similar[0])

                # that the new data not old file
                if int_t > length_sentence:
                    array_int.append(int_t)
                    break

            print("similar doc ", count, similar_doc)
            count = count + 1
            # get only 190 sentence
            if count > 190:
                break

        # save output file
        for index in array_int:
            data_list.append(data[index])

        # Output

        return data_list



