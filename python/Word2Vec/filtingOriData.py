from nltk.corpus import stopwords


# get the file data
def getTheOriginData(path):
    with open(path) as file_object:
        contents = file_object.read()

    ##split the data by line
    lines = contents.split('\n')
    ##the labels
    labels = []
    ##the pairslist which is store the pairs
    pairslist = []
    ##get the pairs and the labels
    for line in lines:
        pairs = []
        strs = line.split('\t')
        labels.append(strs[0])
        strs[3] = filtting(strs[3])
        strs[4] = filtting(strs[4])
        print(strs[3])
        pairs.append(strs[3])
        pairs.append(strs[4])
        pairslist.append(pairs)

    return labels, pairslist

def filtting(wordlist):
    filtered_words = [word for word in wordlist if word not in stopwords.words('english')]
    return filtered_words
#get the data
##get the train data
trainPath = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_train.txt'
train_labels, train_pairslist = getTheOriginData(trainPath)

##get the test data
testPath = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_test.txt'
test_labels, test_pairslist = getTheOriginData(testPath)

