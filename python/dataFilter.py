import string
import re
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

#get the tfidf data
def getTheTfIdfData(path):
    with open(path) as file_object:
        contents = file_object.read()
    ##split the data by line
    lines = contents.split('\n')
    ##the dictionary about (word,tfidf)
    dictionary = {}
    ##get the word and tfidf
    for line in lines:
        strs = line.split('\t')
        dictionary[strs[0]] = strs[1]

    return dictionary


#filter the sentence more short by get the more import word from two nearist words
def filterNear(pairslist, tfidf):

    fil_src_sentences = []
    fil_susp_sentences = []

    #filter the all sentences of pairslist
    ##Traversal the pairslist
    for pairs in pairslist:
        pairs[0] = re.sub(r'\'s', "", pairs[0])
        pairs[1] = re.sub(r'\'s', "", pairs[1])
        pairs[0] = re.sub("[^a-zA-Záéñí]", " ", pairs[0])
        pairs[1] = re.sub("[^a-zA-Záéñí]", " ", pairs[1])
        for i in range(100):
            pairs[0] = re.sub("  ", " ", pairs[0])
            pairs[1] = re.sub("  ", " ", pairs[1])

        print(pairs[0])
        ##the origin src sentence
        Ori_src_words = str.lower(pairs[0]).split()
        ##the orgin susp sentence
        Ori_susp_words = str.lower(pairs[1]).split()

        ##the filtered src sentence
        fil_src_words = []
        ##the filtered susp sentence
        fil_susp_words = []

        i = 0
        while(i < len(Ori_src_words)):
            if (len(Ori_src_words[i]) < 3):
                print(Ori_src_words[i])
                Ori_src_words.remove(Ori_src_words[i])
                i = i - 1
            i = i + 1


        i = 0
        while(i < len(Ori_susp_words)):
            if (len(Ori_susp_words[i]) < 3):
                print(Ori_susp_words[i])
                Ori_susp_words.remove(Ori_susp_words[i])
                i = i - 1
            i = i + 1



        ##the filter process for src
        ###set iter number
        i = 1
        ###read the all words
        while(i < len(Ori_src_words)):
            ### if the sencond word tfidf bigger than the first word, hold the sencond word
            if(tfidf[Ori_src_words[i]] > tfidf[Ori_src_words[i-1]]):
                fil_src_words.append(Ori_src_words[i])
            else:
                fil_src_words.append(Ori_src_words[i-1])


            if( (i+1) < len(Ori_src_words) and (i+2) == len(Ori_src_words) ):
                fil_src_words.append(Ori_src_words[i+1])
            ###let the index i to next next
            i = i + 2

        ##the filter process for susp
        ###set iter number
        i = 1
        while(i < len(Ori_susp_words)):

            ### if the sencond word tfidf bigger than the first word, hold the sencond word
            if(tfidf[Ori_susp_words[i]] > tfidf[Ori_susp_words[i-1]]):
                fil_susp_words.append(Ori_susp_words[i])
            else:
                fil_susp_words.append(Ori_susp_words[i-1])
            if( (i+1) < len(Ori_src_words) and (i+2) == len(Ori_src_words) ):
                fil_src_words.append(Ori_src_words[i+1])
            i = i + 2
            ###let the index i to next next
            i = i + 2



        ##add the filtered sentence to the list
        ###src
        fil_src_sentences.append(fil_src_words)
        ###susp
        fil_susp_sentences.append(fil_susp_words)

    return fil_src_sentences, fil_susp_sentences

#filter the sentence more short by get the more import word from two nearist words
def filterMax(pairslist, tfidf):

    fil_src_sentences = []
    fil_susp_sentences = []

    #filter the all sentences of pairslist
    ##Traversal the pairslist
    for pairs in pairslist:
        print(pairs[0])
        pairs[0] = re.sub(r'\'s', "", pairs[0])
        pairs[1] = re.sub(r'\'s', "", pairs[1])
        pairs[0] = re.sub("[^a-zA-Záéí]", " ", pairs[0])
        pairs[1] = re.sub("[^a-zA-Záéí]", " ", pairs[1])
        for i in range(100):
            pairs[0] = re.sub("  ", " ", pairs[0])
            pairs[1] = re.sub("  ", " ", pairs[1])


        ##the origin src sentence
        Ori_src_words = str.lower(pairs[0]).split()
        ##the orgin susp sentence
        Ori_susp_words = str.lower(pairs[1]).split()

        ##the filtered src sentence
        fil_src_words = []
        ##the filtered susp sentence
        fil_susp_words = []



        ##add the filtered sentence to the list
        ###src
        fil_src_sentences.append(fil_src_words)
        ###susp
        fil_susp_sentences.append(fil_susp_words)

    return fil_src_sentences, fil_susp_sentences



#get the data
##get the train data
trainPath = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_train.txt'
train_labels, train_pairslist = getTheOriginData(trainPath)
##get the test data
testPath = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_test.txt'
test_labels, test_pairslist = getTheOriginData(testPath)

#get the tfidf
##get the train tfidf
train_tfidfPath = '/home/cks/PycharmProjects/MyProject/data/Train-tfidf.txt'
train_tfidf = getTheTfIdfData(train_tfidfPath)
##get the test tfidf
test_tfidfPath = '/home/cks/PycharmProjects/MyProject/data/Test-tfidf.txt'
test_tfidf = getTheTfIdfData(test_tfidfPath)

#get the filtered sentences
##get the train filtered sentences
train_fil_src_sentences, train_fil_susp_sentences = filterNear(train_pairslist, train_tfidf)
##get the test filtered sentences
test_fil_src_sentences, test_fil_susp_sentences = filterNear(test_pairslist, test_tfidf)


#fitter the sentences' size  to 2^n(which size is most near the origin sentences' size)
#########this operation would not do now################3

#write the data to the new file
##write the all (label + '\t' + src + '\t' + susp + '\n') to the train file
with open('/home/cks/PycharmProjects/MyProject/data/Train-filtered.txt', 'w') as f:
    for i in range(len(train_labels)):
        label = train_labels[i]
        src = train_fil_src_sentences[i]
        susp = train_fil_susp_sentences[i]
        f.write(str(label) + '\t' + ' '.join(src) + '\t' + ' '.join(susp) + '\n')

##write the all (label + '\t' + src + '\t' + susp + '\n') to the test file
with open('/home/cks/PycharmProjects/MyProject/data/Test-filtered.txt', 'w') as f:
    for i in range(len(test_labels)):
        label = test_labels[i]
        src = test_fil_src_sentences[i]
        susp = test_fil_susp_sentences[i]
        f.write(str(label) + '\t' + ' '.join(src) + '\t' + ' '.join(susp) + '\n')