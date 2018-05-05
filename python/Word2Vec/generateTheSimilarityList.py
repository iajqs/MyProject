import math

# read the word2vec list
def read_Word2Vec(path):
    with open(path) as file_object:
        contents = file_object.read()
    ##split the data by line
    lines = contents.split('\n')
    ## the List of word2Vec
    Word2VecList = {}
    for i in range(len(lines)-1):
        line = lines[i]
        words = line.split()
        ### the target word
        target = words[0]
        ### the list of the linked words of target word
        linkedList = {}
        ### set the target word as the first in the linkList
        linkedList[target] = 1
        ### add the all sim word to the linked list
        for j in range(len(words)):
            if j == 0:
                continue
            word = words[j]
            linkedList[word] = j+1
        Word2VecList[target] = linkedList
    return Word2VecList

# get the sim from two words(a to b)
## In this function, the words' sim is relate with the words' order
## for example, the sim(a, b) is not must the same with sim(b, a)
def getWordPairSim(word1, word2, Word2VecList):
    ## if the word1 same with word2, return 1
    if(word1 == word2):
        return 1
    ## set the default value of the words' pair
    sim = 1/(1+math.log(len(Word2VecList)+1))
    # print(sim)
    ## if the word1 in the
    if word1 in Word2VecList:
        linkedList = Word2VecList[word1]
        if word2 in linkedList:
            index = linkedList[word2]
            # print(index)
            sim = 1/(1+math.log(index))
    return sim

# get the sim from two sentences
def getSentencePairSim(sen1, sen2, Word2VecList):
    words1 = sen1.split()
    words2 = sen2.split()
    length = len(words1) + len(words2)
    sim = 0
    for word1 in words1:
        wordSim = 0
        for word2 in words2:
            if(wordSim < getWordPairSim(word1, word2, Word2VecList)):
                wordSim = getWordPairSim(word1, word2, Word2VecList)
        sim += wordSim

    for word2 in words2:
        wordSim = 0
        for word1 in words1:
            if(wordSim < getWordPairSim(word2, word1, Word2VecList)):
                wordSim = getWordPairSim(word2, word1, Word2VecList)
        sim += wordSim
    sim = sim/length
    return sim

# get the sim from sen1 to sen2
def getSen1ToSen2Sim( sen1, sen2, Word2VecList ):
    words1 = sen1.split()
    words2 = sen2.split()
    length = len(words1)
    sim = 0
    for word1 in words1:
        wordSim = 0
        for word2 in words2:
            if(wordSim < getWordPairSim(word1, word2, Word2VecList)):
                wordSim = getWordPairSim(word1, word2, Word2VecList)
        sim += wordSim

    sim = sim/length
    return sim

# caculate the all sentences' pairs' sim
def getSim_allSentencePairs(pairslist, labels, Word2VecList):
    simList = []

    for i in range(len(pairslist)):
        pairsSim = []
        pairs = pairslist[i]
        src = pairs[0]
        susp = pairs[1]
        # sim = getSentencePairSim(src, susp, Word2VecList)
        sim1_2 = getSen1ToSen2Sim(src, susp, Word2VecList)
        sim2_1 = getSen1ToSen2Sim(susp, src, Word2VecList)
        pairsSim.append(sim1_2)
        pairsSim.append(sim2_1)
        simList.append(pairsSim)
        # print(str(sim) + "\t" +labels[i])
    return simList

#get the file data
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
        pairs.append(strs[3])
        pairs.append(strs[4])
        pairslist.append(pairs)


    return labels, pairslist


#get the word2Vec
## file path
word2vecPath = '/home/cks/PycharmProjects/MyProject/python/Word2Vec/data/Word2Vec.txt'
## get the List of word2Vec
Word2VecList = read_Word2Vec(word2vecPath)

#get the data
##get the train data
trainPath = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_train.txt'
train_labels, train_pairslist = getTheOriginData(trainPath)
## get the train_sim
train_sim = getSim_allSentencePairs(train_pairslist, train_labels, Word2VecList)

##get the test data
testPath = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_test.txt'
test_labels, test_pairslist = getTheOriginData(testPath)
## get the test sim
test_sim = getSim_allSentencePairs(test_pairslist, test_labels, Word2VecList)

# write
with open('/home/cks/PycharmProjects/MyProject/python/Word2Vec/data/train_sim.txt', 'w') as f:
    for i in range(len(train_labels)):
        label = train_labels[i]
        pairsSim = train_sim[i]
        sim1_2 = pairsSim[0]
        sim2_1 = pairsSim[1]
        f.write(str(label) + '\t' + str(sim1_2) + "\t"+ str(sim2_1) + '\n')

with open('/home/cks/PycharmProjects/MyProject/python/Word2Vec/data/test_sim.txt', 'w') as f:
    for i in range(len(test_labels)):
        label = test_labels[i]
        pairsSim = test_sim[i]
        sim1_2 = pairsSim[0]
        sim2_1 = pairsSim[1]
        f.write(str(label) + '\t' + str(sim1_2) + "\t"+ str(sim2_1) + '\n')