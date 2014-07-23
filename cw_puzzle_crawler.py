
# -*- coding: utf-8 -*-
#Data fetched from http://crosswordgiant.com/
#Data including:
    # New York Times
    # Wall Street Journal
    # Universal
    # Jonesin'
    # USA Today
    # Thomas Joseph - King Feature Syndicate
    # Eugene Sheffer - King Feature Syndicate
    # Premier Sunday - King Feature Syndicate
    # Newsday.com
    # Ink Well xwords
    # L.A. Times Daily
    # L.A. Times Magazine
    # L.A. Times Sunday
    # Canadiana
    # The A.V Club
    # Thinks.com
    # Boston Globe
    # Jonesin Crosswords
    # The Washington Post
    # The Chronicle of Higher Education
    # Irish Times (Crosaire)
    # Irish Times (Simplex)
    # The Guardian - Cryptic
    # The Guardian - Quick

from threading import Thread as thd
from pyquery import PyQuery as p
from datetime import datetime as dt
from ordereddict import OrderedDict as odict
import re
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


May0305


class UrlFetchThread(thd):
    """This class is used to fetch the urls which are used to get data"""
    def __init__(self, thd_name, url, path):
        super(UrlFetchThread, self).__init__(name = thd_name)
        self.URL = url
        self.rsc_store_path = path

    def run(self):
        base_rsc_url = self.URL
        page_number = 1
        rsc_url_para = '?page='
        input_date_format = '%b %d, %Y'
        output_date_format = '%Y.%m.%d'
        re_input_date = re.compile('(?<=\s-\s)\w+\s\d+,\s\d+')
        while True:
            rsc_url = base_rsc_url + rsc_url_para + str(page_number)
            try:
                date_page = p(url = rsc_url)
            except Exception, e:
                page_number += 1
                continue
            label_a_list = date_page('.information_text a')
            if len(label_a_list) == 0:
                break
            else:
                for a in label_a_list:
                    date_str = re_input_date.search(p(a).text()).group()
                    date = dt.strptime(date_str, input_date_format)
                    url = p(a).attr('href')
                    _date_store_path = self.rsc_store_path + date.strftime(output_date_format) + '.txt'
                    DataFetchThread(date_str, url, _date_store_path).start()
                page_number += 1


class DataFetchThread(thd):
    """This class is used to fetch data of days"""
    def __init__(self, thd_name, url, path):
        super(DataFetchThread, self).__init__(name = thd_name)
        self.URL = url
        self.Path = path

    def run(self):
        date_store_path = self.Path
        print self.Path
    #begin to fetch and write
        date_url = self.URL
        try:
            puzzle_page = p(url = date_url)
        except Exception, e:
            return None
        fout = open(date_store_path, 'w')
        label_tr_list = puzzle_page('table.search_results tr')
        label_tr_list.pop(0)         #remove the first element which is empty
        for line in label_tr_list:
            line_list = list(p(line)('td'))
            clue = p(line_list[0]).text()
            answer = p(line_list[1]).text()
            fout.write(answer)
            fout.write(' , ')
            fout.write(clue)
            fout.write('\r\n')
        fout.close()

        
def main():
    base_store_path = 'crossword_puzzles/'
    
#fetch the url dict of puzzle resources
    base_url = 'http://crosswordgiant.com/browse'
    rsc_page = p(url = base_url)
    label_a_list = rsc_page('.information_text a')
    for a in label_a_list:
        rsc_name = p(a).text()
        base_rsc_url = p(a).attr('href')
        rsc_store_path = base_store_path + rsc_name + '/'
        try:
            os.makedirs(rsc_store_path)
        except Exception, e:
            pass
#fetch data from each resource
        UrlFetchThread(rsc_name, base_rsc_url, rsc_store_path).start()

main()



# def main():
#     base_store_path = 'crossword_puzzles/'
#     input_date_format = '%b %d, %Y'
#     output_date_format = '%Y.%m.%d'
#     re_input_date = re.compile('(?<=\s-\s)\w+\s\d+,\s\d+')
    
# #fetch the url dict of puzzle resources
#     base_url = 'http://crosswordgiant.com/browse'
#     rsc_page = p(url = base_url)
#     label_a_list = rsc_page('.information_text a')
#     rsc_url_dict = odict()
#     # rsc_url_dict = {}
#     for a in label_a_list:
#         rsc_url_dict[p(a).text()] = p(a).attr('href')

# #fetch data from each resource
#     for rsc_name in rsc_url_dict:
#         print 'Fetching from ' + rsc_name + '...'
#         rsc_store_path = base_store_path + rsc_name + '/'
#         try:
#             os.makedirs(rsc_store_path)
#         except Exception, e:
#             pass
        
#         base_rsc_url = rsc_url_dict[rsc_name]
#         page_number = 1
#         rsc_url_para = '?page='
#         date_url_dict = odict()
#         # date_url_dict = {}

#     #get url dict of each date
#         while True:
#             rsc_url = base_rsc_url + rsc_url_para + str(page_number)
#             try:
#                 date_page = p(url = rsc_url)
#             except Exception, e:
#                 page_number += 1
#                 continue
#             label_a_list = date_page('.information_text a')
#             if len(label_a_list) == 0:
#                 break
#             else:
#                 for a in label_a_list:
#                     date_url_dict[re_input_date.search(p(a).text()).group()] = p(a).attr('href')
#                 page_number += 1

#     #fetch crossword puzzles of each date
#         for date_str in date_url_dict:
#             print 'Date: ' + date_str
#         #create a new file
#             date = dt.strptime(date_str, input_date_format)
#             date_store_path = rsc_store_path + date.strftime(output_date_format) + '.txt'

#         #begin to fetch and write
#             date_url = date_url_dict[date_str]
#             try:
#                 puzzle_page = p(url = date_url)
#             except Exception, e:
#                 continue
#             fout = open(date_store_path, 'w')
#             label_tr_list = puzzle_page('table.search_results tr')
#             label_tr_list.pop(0)         #remove the first element which is empty
#             for line in label_tr_list:
#                 line_list = list(p(line)('td'))
#                 clue = p(line_list[0]).text()
#                 answer = p(line_list[1]).text()
#                 fout.write(answer)
#                 fout.write(' , ')
#                 fout.write(clue)
#                 fout.write('\r\n')
#             fout.close()
