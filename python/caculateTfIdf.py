from sklearn.feature_extraction.text import CountVectorizer
import re
#get the file data
with open('/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_test.txt') as file_object:
    contents = file_object.read()
##split the data by line
lines = contents.split('\n')
##the labels
labels = []
##the pairslist which is store the pairs
pairslist = []
##the data for caculate the tf-idf
sentences = []
##get the pairs and the labels
for line in lines:
    pairs = []
    strs = line.split('\t')
    labels.append(strs[0])
    strs[3] = re.sub("[0-9]", " ", strs[3])
    strs[4] = re.sub("[0-9]", " ", strs[4])
    pairs.append(strs[3])
    pairs.append(strs[4])
    pairslist.append(pairs)
    sentences.append(strs[3])
    sentences.append(strs[4])


#get the tf-idf table
def getTheTFIDFTable(sentences):

    #
    vectorizer = CountVectorizer()
    ##caculate the tf of the word
    X = vectorizer.fit_transform(sentences)
    ##get the all word
    word = vectorizer.get_feature_names()

    from sklearn.feature_extraction.text import TfidfTransformer

    #
    transformer = TfidfTransformer()
    ##get the tfidf martix of the word of every sentence
    tfidf = transformer.fit_transform(X)

    weight = tfidf.toarray()

    ##generate a dictionary about (word,tfidf)
    dictionary = {}
    for i in range(len(weight)):
        for j in range(len(word)):
            if(weight[i][j]!=0):
                dictionary[word[j]] = weight[i][j]
                # print(dictionary.get(word[j]))

    return dictionary


#get the dictionnary about (word, tfidf) from sentences
dictionary = getTheTFIDFTable(sentences)
#write the all (word + '\t' + tfidf) to the file
with open('/home/cks/PycharmProjects/MyProject/data/Test-tfidf.txt', 'w') as f:
    for word in dictionary:
        print(word)
        tfidf = dictionary.get(word)
        f.write(word +'\t'+ str(tfidf) + '\n')


