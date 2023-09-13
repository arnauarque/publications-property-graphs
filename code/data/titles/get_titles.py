import csv
import re

chars = '"\''

newfile = open('data/titles/titles.csv', mode='w+')
writer = csv.writer(newfile, delimiter='\n')

aux_titles = ['Data mining in education.', 'Machine learning in agriculture.', 'Deep learning for visual understanding.', 'One-class SVM for learning in image retrieval.', 
            'SSVM: a simple SVM algorithm.', 'SVM-KNN: Discriminative nearest neighbor classification for visual category recognition', 
            'Comparison of SVM and LS-SVM for regression']

with open('data/titles/dblp_article.csv', mode='r') as file: 
    reader = csv.reader(file, delimiter=';')
    next(reader)
    for row in reader: 
        line = re.sub('['+chars+']', '', row[29])
        if len(line) <= 10: 
            try: 
                line = aux_titles.pop()
            except: 
                print('More auxiliary titles needed!')
        writer.writerow([line])
        
with open('data/titles/dblp_inproceedings.csv', mode='r') as file: 
    reader = csv.reader(file, delimiter=';')
    next(reader)
    for row in reader: 
        line = re.sub('['+chars+']', '', row[24])
        if len(line) <= 10: 
            try: 
                line = aux_titles.pop()
            except: 
                print('More auxiliary titles needed!')
        writer.writerow([line])
