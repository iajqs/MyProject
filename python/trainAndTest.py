import tensorflow as tf
import numpy as np

sess = tf.InteractiveSession()

def getTheData(path):
    with open(path) as file_object:
        contents = file_object.read()
    ##split the data by line
    lines = contents.split('\n')
    ##the labels
    labels = []
    ##the pairslist which is store the pairs
    sims = []
    ##get the pairs and the labels
    for line in lines:
        pairs = []
        strs = line.split('\t')
        if(strs[0] == '0'):
            labels.append([1, 0])
        else:
            labels.append([0, 1])
        sims.append([strs[1], strs[2]])

    return labels, sims

def get_random_block_from_data(data, labels, batch_size):
    start_index = np.random.randint(0, len(data) - batch_size)
    return data[start_index:(start_index+batch_size)], labels[start_index:(start_index+batch_size)]


#load the MINST
##get the train data
trainPath = '/home/cks/PycharmProjects/MyProject/python/Word2Vec/data/train_sim.txt'
train_labels, train_sims = getTheData(trainPath)
##get the test data
testPath = '/home/cks/PycharmProjects/MyProject/python/Word2Vec/data/test_sim.txt'
test_labels, test_sims = getTheData(testPath)

#register a session as the eviroment for caculate
sess = tf.InteractiveSession()
#x is the trainData
##placeholder as the place for data input
x = tf.placeholder(tf.float32, [None, 2])
#set the weight, the feature's number is 784, the label's number is 10
w = tf.Variable(tf.zeros([2, 2]))
#set the bia, the label's number is 10, so set 10 bias too.
b = tf.Variable(tf.zeros([2]))

# #run hidden layer
# ##get the hidden input data
# h1 = tf.nn.softmax(tf.matmul(x, w1) + b1)
# ##get the weight2
# w2 = tf.Variable(tf.zeros([10, 2]))
# ##get the bias2
# b2 = tf.Variable(tf.zeros([2]))

#the train model
##y is the trainResult
##y = softmax(Wx+b) in TensorFlow the y as the result of this formula
y = tf.nn.softmax(tf.matmul(x, w) + b)
#cross-entropy in TensorFlow
##y_ is the real label
y_ = tf.placeholder(tf.float32, [None, 2])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
#once train
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
#initialize the global variables
tf.global_variables_initializer().run()


#train
for i in range(1000):
        batch_x, batch_y = get_random_block_from_data(train_sims, train_labels, 128)
        # print(batch_y)
        ##this x is for the upper x
        ##this y_ is for the upper y_
        _,cross = sess.run([train_step, cross_entropy],feed_dict={x:batch_x, y_:batch_y})
        print(cross)




#this y is come from upper y, and the upper y is come from the train_step.run, is the python is caculate from the last to first line?
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
#caculate the accuracy
## the tf.cast is translate the bool to float32
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#print the test result
##this x is the x first time input the system
##the y_ too
print(accuracy.eval(feed_dict={x:train_sims, y_:train_labels}))

