# -*- coding: utf-8 -*-# 

# -------------------------------------------------------------------------------
# Name:         generatefeedvector
# Description:  
# Author:       fushp
# Date:         2018/12/29
# -------------------------------------------------------------------------------

import sys
import  feedparser
import  re

# 解析rss数据源 的标题 和单词统计情况的 字典
apcount = {}
wordcounts = {}
feedlist = [line for line in file('feedlist.txt')]
wordlist = []


def getwordcounts(url):
    d = feedparser.parse(url)
    wc = {}
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description
         # 提取单词列表
        words = getwords(e.title + '' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    return d.feed.title, wc


def getwords(html):
  # Remove all the HTML tags
    txt=re.compile(r'<[^>]+>').sub('',html)

  # Split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

  # Convert to lowercase
    return [word.lower() for word in words if word != '']


#统计所有链接 单词统计
def countTotalContent():
    for feedurl in feedlist:
        try:
            title, wc = getwordcounts(feedurl)
            wordcounts[title] = wc
            for word, count in wc.items():
                apcount.setdefault(word, 0)
                if count > 1:
                    apcount[word] += 1
        except:
            print 'Failed to parse feed %s' % feedurl

    #只选择介乎百分比的单词 --->这个算法感觉奇奇怪怪的 我没看懂它再讲什么?????
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if frac > 0.1 and frac < 0.5:
            wordlist.append(w)
    print wordlist

#将数据进行存储到文件中
def savewordcountsToFile():
    out = file('blogdata.txt', 'w')
    out.write('Blog')
    for word in wordlist:
        out.write('\t%s' % word)
    out.write('\n')
    for blog, wc in wordcounts.items():
        print blog
        out.write(blog)
        for word in wordlist:
            if word in wc:
                out.write('\t%d' % wc[word])
            else:
                out.write('\t0')
        out.write('\n')


if __name__ == '__main__':
    # countTotalContent()
    # print wordcounts
    # print apcount
    # savewordcountsToFile()

