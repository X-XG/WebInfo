from skimage import io
import os
import json
from bool_search import Searcher
import semantic_search
import sys

def img_show(flist: list):
    rootdir_base = '../dataset/US_Financial_News_Articles/'
    i = 0
    for fname in flist:
        if i == 10:
            break
        fpath = rootdir_base + fname
        fp = open(fpath, 'r' ,encoding='utf-8')
        text = json.load(fp)
        img_url = text['thread']['main_image']
        if img_url == '':
            continue
        if img_url == 'https://s4.reutersmedia.net/resources_v2/images/rcom-default.png':
            continue
        print(text['thread']['main_image'])
        i += 1
        # if you want to open image directly with VPN, please cancel the Annotation below
        # image = io.imread(text['thread']['main_image'])
        # io.imshow(image)
        # io.show()

if __name__ == '__main__':
    if sys.argv[1] == '-s':
        S = semantic_search.Semantic_Search(sys.argv[2], max_doc=30,synonym_tag = False, embedding_type = "tf-idf")
        flist = S.ranking()
        del S
    elif sys.argv[1] == '-b':
        S = Searcher()
        flist = S.bool_search(sys.argv[2])
        del S
    else:
        print('error')
        exit(1)
    img_show(flist)

