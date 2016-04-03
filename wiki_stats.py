#!/usr/bin/python3

import os
import sys
import math

import array

import statistics

from matplotlib import rc
"""
rc('font', family='Droid Sans', weight='normal', size=14)
"""
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:

            (n, _nlinks) = (map(int, f.readline().split()))
            self._titles = []
            steps = 2854434 / 6  
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            n_lks = 0 # current number of links
            for i in range(n):
                self._titles.append(f.readline().rstrip())
                (size, redirect, lks) = (map(int, f.readline().split()))
                self._sizes[i] = size
                self._redirect[i] = redirect
                for j in range(n_lks, n_lks + lks):
                    self._links[j] = int(str(f.readline()))
                n_lks += lks
                self._offset[i+1] = self._offset[i] + lks
                if i % steps == 0:
                    print ('*', end = ' ')
            print('Done!')
        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return len(self._links[self._offset[_id]:self._offset[_id+1]])

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if self._titles[i] == title:
                return(i)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes(_id)

def analyse_links_from_page(G):
    numlinks_from = list(map(G.get_number_of_links_from, range(G.get_number_of_pages())))
    _max = max(numlinks_from)
    _min = min(numlinks_from)
    mxn = sum(x == _max for x in numlinks_from)
    mnn = sum(x == _min for x in numlinks_from)
    print("Minimal number of links from page:", _min)
    print("Pages with minimal number of links:", mnn)
    print("Maximal number of links from page:", _max)
    print("Pages with maximal number of links:", mxn)
    for i in range(G.get_number_of_pages()):
        if G.get_number_of_links_from(i) == _max:
            break
    print("Page with maximal number of links:",  G.get_title(i))
    print("Mean number of links: %0.2f  (st. dev. : %0.2f)" %(statistics.mean(numlinks_from), statistics.stdev(numlinks_from)))
    hist("lfrom", numlinks_from, 300, 200, "aa", "bb", "zz")
    
def analyse_links_to_page(G):
    numlinks_to = [0 for i in range(G.get_number_of_pages())]
    for i in range(G.get_number_of_pages()):
        for x in G.get_links_from(i):
            numlinks_to[x] += 1
            if G.is_redirect(i) == 1:
                numlinks_to[x] -= 1
    _max = max(numlinks_to)
    _min = min(numlinks_to)
    mxn = sum(x == _max for x in numlinks_to)
    mnn = sum(x == _min for x in numlinks_to)
    print("Minimal number of links to page:", _min)
    print("Pages with minimal number of to-links:", mnn)
    print("Maximal number of links to page:", _max)
    print("Pages with maximal number of to-links:", mxn)
    for i in range(G.get_number_of_pages()):
        if numlinks_to[i] == _max:
            break
    print("Page with maximal number of to-links:",  G.get_title(i))
    print("Mean number of to-links: %0.2f  (st. dev. : %0.2f)" %(statistics.mean(numlinks_to), statistics.stdev(numlinks_to)))
    
    hist("linksto", numlinks_to, 300, 150, "aa", "bb", "zz")
def analyse_redirects(G):
    redirects_to = [0 for i in range(G.get_number_of_pages())]
    for i in range(G.get_number_of_pages()):
        for x in G.get_links_from(i):
            if G.is_redirect(i) == 1:
                redirects_to[x] += 1
    _max = max(redirects_to)
    _min = min(redirects_to)
    mxn = sum(x == _max for x in redirects_to)
    mnn = sum(x == _min for x in redirects_to)
    print("Minimal number of redirects to page:", _min)
    print("Pages with minimal number of redirects:", mnn)
    print("Maximal number of redirects to page:", _max)
    print("Pages with maximal number of redirects:", mxn)
    for i in range(G.get_number_of_pages()):
        if redirects_to[i] == _max:
            break
    print("Page with maximal number of redirects:",  G.get_title(i))
    print("Mean number of redirects: %0.2f  (st. dev. : %0.2f)" %(statistics.mean(redirects_to), statistics.stdev(redirects_to)))
    number_of_redirects_to = [0 for i in range(_max+2)]
    print(_max)
    hist("redir", redirects_to, 100, 50, "aa", "bb", "zz")
    
def bfs(G, start, target):
    path = []
    queue = [start]
    while queue:
        v = queue.pop(0)
        if v not in path:
            path.append(v)
            queue = queue + list(G.get_links_from(v))
            if v == target:
                break
    return path



def hist(fname, data, bins, range,  xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    plt.yscale("log")
    n, bins, patches = plt.hist(data, bins, (0, range), facecolor='green', alpha=0.5)
    plt.savefig(fname, format="pdf")

def hist_log(fname, data, bins, range,  xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    plt.xscale("log")
    n, bins, patches = plt.hist(data, bins, (0, range), facecolor='green', alpha=0.5)
    plt.savefig(fname, format="eps")
    


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

    print("Number of pages with redirect:", sum(wg._redirect))
    analyse_links_from_page(wg)
    analyse_links_to_page(wg)
    analyse_redirects(wg)
    A = bfs(wg, wg.get_id("Python"), wg.get_id("Список_файловых_систем"))
    for i in range(len(A)):
        A[i] = wg.get_title(A[i])
    hist("size", wg._sizes, 100, 40000, "aa", "bb", "zz")
    print("Done!")
