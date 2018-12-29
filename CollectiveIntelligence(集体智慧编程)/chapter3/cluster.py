# -*- coding: utf-8 -*-# 

# -------------------------------------------------------------------------------
# Name:         cluster
# Description:   分级聚类 ：将距离最近的两个群组 组合成一个新的群组
# 可视化方式: 树状图 这块有点复杂 没理解? 先放弃
# Author:       fushp
# Date:         2018/12/29
# -------------------------------------------------------------------------------

import sys


# 读取文件内容
def readfile(filename):
    lines = [line  for line in file(filename)]
    #读取列数据
    colname = lines[0].strip().split('\t')[1:]
    # print colname
    # exit()
    #读取行数据
    rowname = []
    data = []
    for  row in lines[1:]:
        p = row.strip().split('\t')
        # 每行的第一列是行名称
        rowname.append(p[0])
        #剩余就是改行对应的数据了
        data.append([float(x) for x in p[1:]])

    return rowname, colname, data




# 聚类 层级树
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

#皮尔逊算法
def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return 1.0 - num / den


def hcluster(rows, distance=pearson):
  distances = {}
  currentclustid = -1

  # Clusters are initially just the rows
  clust = [bicluster(rows[i],id=i) for i in range(len(rows))]

  while len(clust)>1:
    lowestpair = (0, 1)
    closest = distance(clust[0].vec, clust[1].vec)

    # loop through every pair looking for the smallest distance
    for i in range(len(clust)):
      for j in range(i+1, len(clust)):
        # distances is the cache of distance calculations
        if (clust[i].id, clust[j].id) not in distances:
          distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec, clust[j].vec)

        d = distances[(clust[i].id, clust[j].id)]

        if d<closest:
          closest = d
          lowestpair = (i, j)

    # calculate the average of the two clusters
    mergevec = [
    (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
    for i in range(len(clust[0].vec))]

    # create the new cluster
    newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest,
                         id=currentclustid)

    # cluster ids that weren't in the original set are negative
    currentclustid -= 1
    del clust[lowestpair[1]]
    del clust[lowestpair[0]]
    clust.append(newcluster)
  return clust[0]


# 打印聚类树
def printclust(clust, labels=None, n=0):
  # indent to make a hierarchy layout 利用缩进来建立层级布局
    for i in range(n):
        print ' ',
    if clust.id < 0:
        # negative id means that this is branch 负数标记代表这是一个分支
        print '-'
    else:
        # positive id means that this is an endpoint 正数标记代表这是一个分支
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]

  # now print the right and left branches
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n+1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n+1)


if __name__ == '__main__':
   print readfile('blogdata.txt')
