#get the file data

# 计算jaccard系数
def getJaccard(p,q):
    c = list(set(q).intersection(set(p)))
    return float(len(c))/(len(p)+len(q)-len(c))


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
        pairs.append(strs[1])
        pairs.append(strs[2])
        pairslist.append(pairs)

    return labels, pairslist


def Caculate(pairslist):
    sim = []
    for i in range(len(pairslist)):
        src = pairslist[i][0]
        susp = pairslist[i][1]

        jaccard = getJaccard(src, susp)
        sim.append(jaccard)
    return sim


#get the data
##get the train data
trainPath = '/home/cks/PycharmProjects/MyProject/data/Train-filtered.txt'
train_labels, train_pairslist = getTheOriginData(trainPath)
##get the test data
testPath = '/home/cks/PycharmProjects/MyProject/data/Test-filtered.txt'
test_labels, test_pairslist = getTheOriginData(testPath)

trainPath2 = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_train.txt'
train_labels2, train_pairslist2 = getTheOriginData(trainPath2)
##get the test data
testPath2 = '/home/cks/PycharmProjects/MyProject/data/msr_paraphrase_test.txt'
test_labels2, test_pairslist2 = getTheOriginData(trainPath2)

#caculate the similarity
##caculate the similarity of train data
train_sim1 = Caculate(train_pairslist)
##caculate the similarity of test data
test_sim1 = Caculate(test_pairslist)
##caculate the similarity of train data
train_sim2 = Caculate(train_pairslist2)
##caculate the similarity of test data
test_sim2 = Caculate(test_pairslist2)


with open('/home/cks/PycharmProjects/MyProject/data/Train_sim.txt', 'w') as f:
    for i in range(len(train_sim1)):
        label = train_labels[i]
        sim1 = train_sim1[i]
        sim2 = train_sim2[i]
        f.write(str(label) + '\t' + str(sim1) + '\t' + str(sim2) + '\n')

with open('/home/cks/PycharmProjects/MyProject/data/Test_sim.txt', 'w') as f:
    for i in range(len(test_sim1)):
        label = test_labels[i]
        sim1 = test_sim1[i]
        sim2 = test_sim2[i]
        f.write(str(label) + '\t' + str(sim1) + '\t' + str(sim2) + '\n')
