#!/usr/bin/python3
import os
import sys
import math

import array

import statistics




class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            (n, _nlinks) = (0, 0)
            t=f.readlines()
            for i in range(len(t[0])):
                if t[0][i]==' ':
                    n=int(t[0][0:i])
                    _nlinks=int(t[0][i+1:])

            self.n=n
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            l=0
            for i in range(1,len(t)):
                if (ord(t[i][0])>=65 and ord(t[i][0])<=90) or (ord(t[i][0])>=1040 and ord(t[i][0])<=1071):
                    self._titles.append(t[i])
                    self._sizes[l] = list(map(int, t[i+1].split()))[0]
                    self._offset[l] = list(map(int, t[i+1].split()))[2]
                    self._redirect[l] = list(map(int, t[i+1].split()))[1]
                    l+=1
                if (ord(t[i][0])<=65 and ord(t[i][0])>=90) or (ord(t[i][0])<=1040 and ord(t[i][0])>=1071) and (ord(t[i-1][0])<=65 and ord(t[i-1][0])>=90) or (ord(t[i-1][0])<=1040 and ord(t[i-1][0])>=1071):
                    self._links[l-1].append(t[i])

            # TODO: прочитать граф из файла

        print('Граф загружен')

    def get_number_of_links_from(self, _id):
        return self._offset[_id]

    def get_links_from(self, _id):
        return self._links[_id]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if self._titles[i]==title+'\n':
                return i
    def shlak(self):
        return self._titles

    def get_number_of_pages(self):
        return self.n

    def is_redirect(self, _id):
        if self._redirect[_id]!=0:
            return True
        else:
            return False

    def get_title(self, _id):
        return self._titles[_id][0:(len(self._titles[_id])-1)]

    def get_page_size(self, _id):
        return self._sizes[_id]

def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()

if __name__ == '__main__':
        wg = WikiGraph()
        wg.load_from_file('wiki_small.txt')
        k1=0
        k2=0
        k3=0
        mn=wg._offset[0]
        mx=wg._offset[0]
        mx_id=None
        num_ssil=0
        for i in range(wg.get_number_of_pages()):
            if wg.is_redirect(i)==True:
                k1+=1
            if wg._offset[i]<mn:
                mn=wg._offset[i]
            if wg._offset[i]>mx:
                mx=wg._offset[i]
            num_ssil+=wg.get_number_of_links_from(i)
        for i in range(wg.get_number_of_pages()):
            if wg._offset[i]==mn:
                k2+=1
            if wg._offset[i]==mx:
                k3+=1
                mx_id=i
        print(wg.get_number_of_pages())
        print('Количество статей с перенаправлением',k1,' ',(k1*100/wg.get_number_of_pages()),'%')
        print('Минимальное количество ссылок из статьи',mn)
        print('Количество статей с минимальным количеством ссылок',k2)
        print('Максимальное количество ссылок из статьи',mx)
        print('Количество статей с максимальным количеством ссылок',k3)
        print('Статья с наибольшим количеством ссылок',wg.get_title(mx_id))
        print('Среднее количество ссылок в статье',num_ssil/wg.get_number_of_pages())
