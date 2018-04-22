#计算欧几里德距离：
def euclidean(p,q):
    #如果两数据集数目不同，计算两者之间都对应有的数
    same = 0
    for i in p:
        if i in q:
            same +=1

    #计算欧几里德距离,并将其标准化
    e = 0
    for i in range(same):
        e = e + (p[i]-q[i])*(p[i]-q[i])
    return 1/(1+e**.5)

# 计算jaccard系数
def jaccard(p,q):
    c = list(set(q).intersection(set(p)))
    return float(len(c))/(len(p)+len(q)-len(c))



p = ['shirt','shoes','pants','socks']
q = ['shirt','shoes']
print(euclidean(p,q))