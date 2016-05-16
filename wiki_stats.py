#!/usr/bin/python3

import os
import sys
import math
import array

import statistics

from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import matplotlib.pyplot as plt


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            (n, _nlinks) = tuple(int(i) for i in f.readline()[:-1].split())
            self._n, self._nlinks = n, _nlinks
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))

            number  = 0

            for line in range(n):
                self._titles.append(f.readline()[:-1])
                size, flag, links = tuple(int(i) for i in f.readline()[:-1].split())
                self._sizes[line] = size
                self._offset[line] = number

                if flag == 1:
                    self._redirect[line] = True
                else:
                    self._redirect[line] = False


                for one in range(links):
                    self._links[number + one] = int(f.readline()[:-1])
                number += links

        print('Граф загружен')
        f.close()

    def get_number_of_links_from(self, _id):
        return len(self._links[self._offset[_id]:self._offset[_id + 1]])

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        return self._titles.index(title)

    def get_number_of_pages(self):
        return self._n

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]

    def get_all_links(self):
        return self._nlinks




def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.hist(x=data, bins=bins, facecolor=facecolor, alpha=alpha, **kwargs)
    plt.savefig(fname, transparent=transparent)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
        maxlinks = max(wg.get_links_from(i) for i in range(wg.get_number_of_pages()))
        print('Maximum number of links  = ', len(maxlinks))
        minlinks = min(wg.get_links_from(i) for i in range(wg.get_number_of_pages()))
        print('Minimum number of links = ', len(minlinks))
        redirlinks = sum(1 for i in range(wg.get_number_of_pages()) if wg.is_redirect(i))
        print('The number of links with redirection = ', redirlinks)
        pageminlink = sum(1 for i in range(wg.get_number_of_pages()) if len(wg.get_links_from(i)) == len(minlinks))
        print('The number of articles with minlinks = ', pageminlink)
        pageminlink = sum(1 for i in range(wg.get_number_of_pages()) if len(wg.get_links_from(i)) == len(maxlinks))
        print('The number of articles with maxlinks = ', pageminlink)
        averagelink = statistics.mean(wg.get_number_of_links_from(i)for i in range(wg.get_number_of_pages()))
        print('The AVERAGE number of links = ', round(averagelink,0))
        links_on=[0]*wg.get_number_of_pages()
        for u in range(wg.get_number_of_pages()):
            for t in wg.get_links_from(u):
                links_on[t]+=1
        m = min(links_on)
        n = max(links_on)
        print('Min links on page = ', m)
        print('Max links on page =', n)
        print('Maxlinked page =', wg.get_title(links_on.index(n)))

        def find_links(i):
            number = 0
            for t in range(wg.get_number_of_pages()):
                for z in wg.get_links_from(t):
                    if z == i:
                        number += 1
            return(number)

        number_minlinked = sum(1 for i in range(wg.get_number_of_pages() + 1) if find_links(i) == m)
        numbermax_linked = sum(1 for i in range(wg.get_number_of_pages() + 1) if find_links(i) == n)
        dirs = [0] * wg.get_number_of_pages()
        for i in range(wg.get_number_of_pages()):
            if not wg.is_redirect(i):
                for lnk in wg.get_links_from(i):
                    dirs[lnk] += 1
        print('Minimum number of redirections to the links', min(dirs))
        print('Maximum number of redirections to the link', max(dirs))
        print('Number of links with minimum of redirections', dirs.count(min(dirs)))
        print('Number of links with maximum of redirections', dirs.count(max(dirs)))
        print('Number of minlinked pages = ', number_minlinked)
        print('Number of maxlinked pages = ', numbermax_linked)
        hist(fname='4-1.png', data=[wg.get_number_of_links_from(i) for i in range(wg._n)], bins=200,xlabel='Количество статей', ylabel="Количество ссылок", title="Распределение количества ссылок из статьи")
        plt.show()
        hist(fname='4-2.png', data=[links_on[i] for i in range(wg._n)], bins=50, xlabel='Количество статей',ylabel='Количество ссылок', title='Распределение количества ссылок на статью')
        plt.show()
        hist(fname='4-3.png', data=[wg.get_page_size(i) for i in range(wg._n) ], bins=200,xlabel='Количество статей',ylabel='Размер', title='Распределение размеров по статьям')
        plt.show()
        hist(fname='4-4.png', data=[math.log(wg.get_page_size(i),math.e) for i in range(wg._n)], bins=200,xlabel='Количество статей',ylabel='Размер', title='Распределение размеров по статьям в логарифмическом масштабе')
        plt.show()
        hist(fname='4-5.png', data=[dirs[i] for i in range(wg.get_number_of_pages())], bins=200, xlabel='Количество статей', ylabel='Количество перенаправлений на статью', title='Распределение количества перенаправлений на статью')
        plt.show()
    else:
        print('Файл с графом не найден')
        sys.exit(-1)
