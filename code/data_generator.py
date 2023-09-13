import sys, os, re, csv, random, lorem, numpy


# Establim una seed per tal que surtin sempre els mateixos resultats
seed = 478513658
random.seed(seed)
numpy.random.seed(seed)


# La classe Idx és iterable i ens permet mantenir un registre dels índexs que 
# ja han estat fets servir per alguna altra instància del domini
class Idx:
    def __init__(self, start=0):
        self.idx = start-1
    def __iter__(self):
        return self
    def __next__(self):
        self.idx += 1
        return str(self.idx)


# Retorna un codi ISSN
def issn():
    return '%d-%d' % (random.randint(1000,9000), random.randint(1000, 9000))


# Definim l'Índex (Idx) per a les instàncies
i = Idx()
idx = iter(i)

# Method to get the final filepath given a filename
def fp(filename):
    parts = filename.split('_')
    fp = './data/'
    if 'rel' in parts: 
        parts.remove('rel')
        fp += 'relations/' + '_'.join(parts)
    else: 
        fp += 'individuals/' + '_'.join(parts)
    return fp

# Method to print a welcome messages
def welcomeMsg(msg):
    welcomeMsg = '''
--------------------------------------------------------------------------------
-- %s
--------------------------------------------------------------------------------
-- SDM Project
-- Authors: Arnau Arqué and Daniel Esquina
--------------------------------------------------------------------------------
    ''' % msg
    print(welcomeMsg)

# Method to print an info message
def infomsg(msg, pre=''):
    print('%s[INFO] %s' % (pre, msg))

# Mètode per crear els directoris necessaris per a l'execució del programa
def create_directories():
    dirs = os.listdir('.')
    if 'data' not in dirs: 
        os.mkdir('./data')
    dirs = os.listdir('./data/')
    if 'individuals' not in dirs: 
        os.mkdir('./data/individuals')
    if 'relations' not in dirs: 
        os.mkdir('./data/relations')

## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
## -- Inici del programa
## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------

if __name__ == '__main__':
    
    # if len(sys.argv) != 2: 
    #     print('[ERROR] Specify if you want to create train or test split')
    #     print('[USAGE] python3 data_generator.py [train] [test]')
    # train = sys.argv[1] == 'train'

    welcomeMsg('Data generation program')
    create_directories()

    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Keywords
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------

    # Keywords bàsiques
    keys = ['mitotic spindle', 'modeling', 'modularity', 'molecular diagnostics', 'molecular motors', 'multicellular systems', 'multiscale modelling', 'nanofabrication', 'nanoskiving', 'nonlinear chemistry', 'nucleic acid replication', 'nucleus deformation', 'origins of life', 'pattern formation', 'phospholipid biosynthesis', 'polymerase', 'polymerome', 'protein degradation', 'protein design', 'protein modification', 'protocell communication', 'quantum artificial intelligence', 'remote control', 'research management', 'RNA catalysis', 'RNA engineering', 'science communication', 'self-organization', 'septin', 'sequence design', 'signaling', 'simulation algorithms', 'single-molecule', 'soft matter', 'strain engineering', 'structural biology', 'supramolecular chemistry', 'synthetic genomics', 'synthetic microcompartments', 'synthetic proteome', 'synthetic tissue', 'system engineering', 'systems theory', 'therapeutic antibodies', 'thermodynamics', 'transcriptional regulation', 'transport', 'velocimetry', 'waste valorization', 'XNA']
    # Keywords que definiran les COMMUNITIES
    community_keys = ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']

    with open(fp('keywords.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['id', 'name'])
        for key in keys+community_keys: 
            writer.writerow([next(idx), key])


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Authors
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    authors = ['Stefan Mangard', 'M. Tamer Özsu', 'Christopher Habel', 'Uwe Reyle', 'Christoph Meinel', 'Volker Schillings', 'Peter Sturm', 'Hans L. Bodlaender', 'Klaus W. Wagner', 'Yvo Desmedt', 'Stefan Köpsell', 'William Whyte', 'Salvatore J. Stolfo', 'Tae Hwan Oh', 'Andrew Beng Jin Teoh', 'Graham Steel', 'Glenn Durfee', 'Wenyuan Xu', 'Jeffrey Hoffstein', 'Hugo Krawczyk', 'Sudeep Sarkar', 'Zongyi Liu', 'Akira Otsuka', 'Pijush Samui', 'Fahim Kawsar', 'Hari Sundaram', 'Anwitaman Datta', 'Václav Snásel', 'Naphtali Rishe', 'Michiel Steyaert', 'Eby G. Friedman', 'Suely Fragoso', 'B. John Oommen', 'Edward W. Tunstel', 'Birgit Vogel-Heuser', 'Gianluca Paravati', 'Fabrizio Cutolo', 'Wolfgang Hürst', 'Nadia Magnenat-Thalmann', 'Murat Yilmaz', "Gabriele D'Angelo", 'Stefano Ferretti', 'Damianos Gavalas', 'Christos-Nikolaos Anagnostopoulos', 'Paola Salomoni', 'Silvia Mirri', 'Daniel Thalmann', 'Pascal Volino', 'Xinguo Liu', 'Hujun Bao', 'Manfred Glesner', 'Yan Zhang', 'Weiyi Meng', 'Yi-Min Wang', 'Chengfei Liu', 'Kishor S. Trivedi', 'Seon Wook Kim', 'Douglas C. Schmidt', 'Jean-Michel Muller', 'Manish Parashar', 'Chi Hau Chen', 'B. Prabhakaran', 'Goce Trajcevski', 'Witold Pedrycz', 'Alex M. Andrew', 'Xian-Sheng Hua', 'Aditya P. Mathur', 'Soo Dong Kim', 'Vassilis Cutsuridis', 'Nigel H. Lovell', 'Jorge J. Riera', 'Vincent A. Billock', 'Rodolphe Sepulchre', 'Mitsuo Kawato', 'Anil K. Seth', 'Thomas M. Bartol', 'David M. Weiss', 'Ravishankar K. Iyer', 'Gopal Racherla', 'Sajal K. Das', 'Robert W. Heath Jr.', 'Ravi S. Sandhu', 'Jonathan Chan', 'Sridhar Radhakrishnan', 'Jelena V. Misic', 'Vojislav B. Misic', 'Vasilis Friderikos', 'Symeon Papavassiliou', 'Tero Ojanperä', 'Dewan Tanvir Ahmed', 'Shervin Shirmohammadi', 'Zhiwei Xu', 'Michael Losavio', 'Prabir Bhattacharya', 'Johan van Benthem', 'Gerald Schaefer', 'Emanuele Panizzi', 'Pasquale Pagano', 'Orna Kupferman', 'Gerard J. Holzmann']
    countries = ['China', 'India', 'USA', 'Spain', 'France', 'Germany', 'Iceland', 'Finland', 'Norway', 'Sweden', 'United Kingdom', 'Poland', 'Ukraine', 'Russia', 'Italy', 'Greece', 'Croatia']

    with open(fp('authors.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['id', 'author', 'country'])
        for author in authors: 
            writer.writerow([next(idx), author, random.choice(countries)])


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Conference Editions
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    neditions = 5
    ystart = 2010
    yrange = 6
    editions = [ str(x) for x in range(1,neditions+1) ]
    subjects = ['Communication in Multiagent Systems', 'ACM National Conference', 'Discrete Mathematics in the Schools', 'Coding Theory and Applications', 'Language Engineering Conference', 'Ershov Informatics Conference', 'Dance Notations and Robot Motion', 'Plan, Activity, and Intent Recognition', 'Semantic Grid', 'Complexity of Constraints', 'TPDL Workshops', 'Computational Methods for SNPs and Haplotype Inference', 'Caring Machines', 'Mathematical Methods Of Analysis Of Biopolymer Sequences', 'Web Application Security', 'Information Visualization', 'Theories of Programming and Formal Methods', 'Fault-Tolerant Distributed Computing', 'Three-Dimensional Imaging, Interaction, and Measurement', 'Webmedia']
    cities = ['London', 'Paris', 'New York', 'Moscow', 'Dubai', 'Tokyo', 'Singapore', 'Los Angeles', 'Barcelona', 'Chicago']

    with open(fp('conference_editions.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'edition', 'city', 'year'])
        
        for subject in subjects: 
            years = [ str(y) for y in range(ystart,ystart+yrange)]
            last_year = random.choice(years)
            for edition in editions: 
                writer.writerow([subject, edition, random.choice(cities), last_year])
                years = [ str(y) for y in range(int(last_year), int(last_year)+yrange) ]
                last_year = random.choice(years)


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Conferences
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    with open(fp('conferences.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['id', 'name'])
        for subject in subjects:
            writer.writerow([next(idx), subject])


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Journal Volumes
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    nvolumes = 5
    ystart = 2010
    yrange = 3
    volumes = [ str(x) for x in range(1,nvolumes+1) ]
    journals = ['Applied Engineering', 'Engineering and Applied Sciences', 'Engineering Science', 'International Journal of Science and Qualitative Analysis', 'International Journal of Science, Technology and Society', 'Science, Technology & Public Policy', 'Science Research', 'Frontiers', 'Innovation', 'Research & Development', 'Science Development', 'Applied and Computational Mathematics', 'Automation, Control and Intelligent Systems', 'Biomedical Statistics and Informatics', 'Computational Biology and Bioinformatics', 'Control Science and Engineering', 'Industrial Engineering', 'International Journal of Computational and Theoretical Chemistry', 'International Journal of Data Science and Analysis', 'International Journal of Discrete Mathematics']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    with open(fp('journal_volumes.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'volume', 'month', 'year', 'npages', 'issn'])
        
        for journal in journals: 
            years = [ str(y) for y in range(ystart,ystart+yrange)]
            last_year = random.choice(years)
            for volume in volumes: 
                writer.writerow([journal, volume, random.choice(months), last_year, str(random.randint(500,1500)), issn()])
                years = [ str(y) for y in range(int(last_year)+1, int(last_year)+yrange) ]
                last_year = random.choice(years)


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Journals
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    with open(fp('journals.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['id', 'name', 'online'])
        for journal in journals:
            writer.writerow([next(idx), journal, random.choice(['Yes', 'No'])])


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Papers
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    os.system('python3 ./data/titles/get_titles.py')
    titles_file = open('./data/titles/titles.csv', mode='r')
    titles = csv.reader(titles_file, delimiter='\n')
    
    # limit = 1800
    # titles = []
    # for i,row in enumerate(csv.reader(titles_file, delimiter='\n')):
    #     if train and i < limit:
    #         titles.append(row)
    #     elif not train and i >= limit:
    #         titles.append(row)

    with open(fp('papers.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow([ 'id', 'title', 'month', 'year', 'pages', 'issn', 'abstract' ])
        for title in titles: 
            writer.writerow([ next(idx), title[0], random.choice(months), random.randint(1999,2010), 
                            random.randint(20, 100), issn(), lorem.paragraph() ])

    titles_file.close()


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de Universities i Companies
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    universities = [('Massachusetts Institute of Technology (MIT)', 'United States'), ('University of Oxford', 'United Kingdom'), ('Stanford University', 'United States'), ('University of Cambridge', 'United Kingdom'), ('Harvard University', 'United States'), ('California Institute of Technology (Caltech)', 'United States'), ('Imperial College London', 'United Kingdom'), ('ETH Zurich (Swiss Federal Institute of Technology)', 'Switzerland'), ('UCL (University College London)', 'United Kingdom'), ('University of Chicago', 'United States')]
    companies = ['F. Hoffmann-La Roche AG.', 'IBM Corporation.' 'Novartis International AG.', 'Merck & Co., Inc.', 'AstraZeneca plc.', 'Butterfly Network, Inc', 'SnapTech', 'BenchSci', 'Novo Nordisk', 'Descartes Labs']

    with open(fp('universities.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'country'])
        for university in universities: 
            writer.writerow(list(university))


    with open(fp('companies.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name'])
        for company in companies: 
            writer.writerow([company])


    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------
    ## -- Generació de les relacions
    ## -----------------------------------------------------------------------------
    ## -----------------------------------------------------------------------------

    # Generem la relació de AUTHORS-AFFILIATED_TO->{UNIVERSITY, COMPANY}
    with open(fp('rel_affiliatedTo.csv'), mode='w+') as file: 
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['author_id', 'name'])
        
        with open(fp('authors.csv'), mode='r') as afile: 
            reader = csv.reader(afile, delimiter=';')
            next(reader) # Saltem la header
            
            for author in reader:
                if numpy.random.random_sample() < 0.5: # university
                    uni = random.choice(universities)
                    writer.writerow([author[0], uni[0]])
                else: # company
                    com = random.choice(companies)
                    writer.writerow([author[0], com])

    # A partir d'un fitxer CSV, retorna una llista amb el primer atribut de totes 
    # les instàncies
    def get_ids(filename):
        with open(filename, mode='r') as file: 
            reader = csv.reader(file, delimiter=';')
            next(reader)
            ids = [ row[0] for row in reader ]
        return ids

    # A partir del fitxer 'keywords.csv', retorna dues llistes: una amb els ID's de 
    # les keywords bàsiques i una altra amb els ID's de les community keywords
    def get_ids_keywords(filename):
        ids, community_ids = [], []
        with open(filename, mode='r') as file: 
            reader = csv.reader(file, delimiter=';')
            next(reader)
            for row in reader:
                if row[1] in community_keys: 
                    community_ids.append(row[0])
                else: 
                    ids.append(row[0])
        return ids, community_ids

    # A partir del fitxer de 'papers.csv', retorna una llista amb els ID's dels 
    # papers publicats
    def get_ids_published_papers(filename):
        with open(filename, mode='r') as file: 
            reader = csv.reader(file, delimiter=';')
            header = next(reader)
            header = [ item.split(':')[0] for item in header ]
            published_idx = header.index('published')
            ids = [ row[0] for row in reader if row[published_idx] == 'Yes' ]
        return ids

    # A partir del fitxer de 'papers.csv', retorna dues llistes: una pels ID's dels 
    # papers publicats i una altra pels ID's dels papers NO publicats
    def get_ids_papers(filename): 
        ids, ids_np = [], []
        with open(filename, mode='r') as file: 
            reader = csv.reader(file, delimiter=';')
            header = next(reader)
            header = [ item.split(':')[0] for item in header ]
            published_idx = header.index('published')
            for row in reader: 
                if row[published_idx] == 'Yes': 
                    ids.append(row[0])
                else:
                    ids_np.append(row[0])
        return ids, ids_np

    # Donat un fitxer CSV, retorna una llista de llistes amb tots els atributs de 
    # totes les instàncies
    def get_all_attributes(filename):
        with open(filename, mode='r') as file: 
            reader = csv.reader(file, delimiter=';')
            next(reader) # Ometem la header
            rows = [ row for row in reader ]
        return rows

    # Obtenim ID's de autors, keywords i papers
    authors = get_ids(fp('authors.csv'))
    keywords, community_keywords = get_ids_keywords(fp('keywords.csv'))
    papers = get_ids(fp('papers.csv'))
    # Obtenim tots els attr. dels journal volumes i les conference editions
    journal_volumes = get_all_attributes(fp('journal_volumes.csv'))
    conference_editions = get_all_attributes(fp('conference_editions.csv'))

    # Creem els fitxers per emmagatzemar les relacions
    cites_file = open(fp('rel_cites.csv'), mode='w+')
    hasMainAuthor_file = open(fp('rel_hasMainAuthor.csv'), mode='w+')
    hasCoAuthor_file = open(fp('rel_hasCoAuthor.csv'), mode='w+')
    hasReviewer_file = open(fp('rel_hasReviewer.csv'), mode='w+')
    hasKeyword_file = open(fp('rel_hasKeyword.csv'), mode='w+')
    isPublishedInJournal_file = open(fp('rel_isPublishedInJournal.csv'), mode='w+')
    isPublishedInConference_file = open(fp('rel_isPublishedInConference.csv'), mode='w+')

    # Creem els writers dels fitxers de relacions
    cites = csv.writer(cites_file, delimiter=';')
    hasMainAuthor = csv.writer(hasMainAuthor_file, delimiter=';')
    hasCoAuthor = csv.writer(hasCoAuthor_file, delimiter=';')
    hasReviewer = csv.writer(hasReviewer_file, delimiter=';')
    hasKeyword = csv.writer(hasKeyword_file, delimiter=';')
    isPublishedInJournal = csv.writer(isPublishedInJournal_file, delimiter=';')
    isPublishedInConference = csv.writer(isPublishedInConference_file, delimiter=';')

    # Generem les capçaleres
    cites.writerow(['start_id','end_id'])
    hasMainAuthor.writerow(['start_id','end_id'])
    hasCoAuthor.writerow(['start_id','end_id'])
    hasReviewer.writerow(['start_id','end_id','description','decision'])
    hasKeyword.writerow(['start_id','end_id'])
    isPublishedInJournal.writerow(['paper_id', 'journal_name', 'volume', 'month', 'year', 'npages', 'issn'])
    isPublishedInConference.writerow(['paper_id', 'conference_name', 'edition', 'city', 'year'])

    # Funcions que retornen un nombre aleatori de citations, coauthors, reviewers,
    # i keywords
    num_cites = lambda: random.randint(1,10)
    num_coauthors = lambda: random.randint(1,5)
    num_reviewers = lambda: random.randint(3,5)
    num_keywords = lambda: random.randint(3,5)
    num_community_keywords = lambda: random.randint(1,6)

    # Seleccionem un subconjunt de papers per tal que no siguin citats per 
    # cap altre paper
    non_cited_papers_ids = random.sample(papers, k=20)

    # Donat un paper i tots els papers disponibles, retornem les seves citacions
    def get_citations_rel(paper, papers):
        citations = random.sample(papers, k=num_cites())
        # No citem cap paper que estigui a 'non_cited_papers_ids'
        while paper in citations or any([ cited_paper in non_cited_papers_ids for cited_paper in citations ]): 
            citations = random.sample(papers, k=num_cites())
        rows = [ [paper, citation] for citation in citations ]
        return rows

    # Donat un paper, tots els authors disponibles i el mainAuthor del paper, 
    # retornem les relacions hasCoAuthor corresponents al paper. També retornem 
    # els ID's dels coauthors seleccionats
    def get_coauthors_rel(paper, authors, mainAuthor):
        coauthors = random.sample(authors, k=num_coauthors())
        while mainAuthor in coauthors: 
            coauthors = random.sample(authors, k=num_coauthors())
        rows_co = [ [paper,coauthor] for coauthor in coauthors ]
        return rows_co, coauthors

    # Donat un nombre 'n' de suposats reviewers, retornem una llista amb, per a cada
    # review, una llista amb el text descriptiu de la review i la decisió (accepted 
    # o denied). També retornem la overall_acceptance, que tindrà valor 'Yes' si 
    # almenys la meitat dels reviewers ha acceptat el paper. Altrament tindrà valor 'No'
    def get_decisions(n):
        perc_acceptance = 0.8
        decisions = []
        accepted = 0
        for _ in range(n):
            text = lorem.paragraph()
            decision = 'accepted' if numpy.random.random_sample() < perc_acceptance else 'denied'
            if decision == 'accepted': 
                accepted += 1
            decisions.append([text,decision])
        overall_acceptance = 'Yes' if accepted >= n/2 else 'No'
        return decisions, overall_acceptance

    # Donat un paper, tots els authors disponibles, el mainAuthor del paper, i els 
    # coAuthors del paper, retornem les relacions hasReviewer corresponents al paper
    # i la overall_acceptance (veure 'get_decisions(...)' per a +info)
    def get_reviewers_rel(paper, authors, mainAuthor, coAuthors):
        reviewers = random.sample(authors, k=num_reviewers())
        while mainAuthor in reviewers or any([coauthor in reviewers for coauthor in coAuthors]):
            reviewers = random.sample(authors, k=num_reviewers())
        
        decisions, overall_acceptance = get_decisions(len(reviewers))
        rows_rw = [ [paper,reviewer] + decisions[i] for i,reviewer in enumerate(reviewers) ]
        return rows_rw, overall_acceptance

    # Donat un paper i les keywords disponibles, retornem les keywords del paper
    # en qüestió
    def get_keywords_rel(paper, keywords):
        kws = random.sample(keywords, k=num_keywords())
        # Afegim les keywords d'entre el conjunt de keywords bàsiques
        rows = [ [paper,keyword] for keyword in kws ]
        # Afegim les keywords d'entre les keywords de community
        kws = random.sample(community_keywords, k=num_community_keywords())
        rows += [ [paper, keyword] for keyword in kws ]
        return rows    

    # ------
    # PAS 1:
    # ------
    # Determinem les relacions que no depenen de cap altra, i.e.:
    #   cites 
    #   hasMainAuthor
    #   hasCoAuthor
    #   hasReviewer
    #   hasKeyword
    # Encara no generem isPublishedIn(...) perquè depenen de si la majoria de 
    # reviewers ha acceptat o no el paper

    acceptance = [] # Llista per mantenir l'overall acceptance de cada paper (i.e. si el paper està acceptat o no)
    for paper in papers: 
        # CITES
        crels = get_citations_rel(paper, papers)
        cites.writerows(crels)
        
        # MAIN-AUTHOR
        mainAuthor = random.choice(authors)
        hasMainAuthor.writerow([paper,mainAuthor])
        
        # CO-AUTHORS
        carels, coAuthors = get_coauthors_rel(paper, authors, mainAuthor)
        hasCoAuthor.writerows(carels)
        
        # REVIEWERS (amb les DECISIONS preses)
        rrels, overall_acceptance = get_reviewers_rel(paper, authors, mainAuthor, coAuthors)
        acceptance.append(overall_acceptance)
        hasReviewer.writerows(rrels)
        
        # KEYWORDS
        krels = get_keywords_rel(paper, keywords)
        hasKeyword.writerows(krels)

    # Comprovació
    # aux = [ x == 'Yes' for x in acceptance ]
    # print('Accepted: %d / 2000\t(%d perc.)' % (sum(aux), sum(aux)*100/2000))
    # sys.exit(0)

    # ------
    # PAS 2:
    # ------
    # Afegim un nou atribut 'published' dels papers en funció de la decisió que han 
    # pres els reviewers

    with open(fp('papers.csv'), mode='r') as file: 
        reader = csv.reader(file, delimiter=';')
        
        with open(fp('aux.csv'), mode='w+') as newfile:
            writer = csv.writer(newfile, delimiter=';')
            writer.writerow(next(reader) + ['published'])
            
            for i, row in enumerate(reader): 
                writer.writerow(row + [acceptance[i]])

    os.remove(fp('papers.csv'))
    os.rename(fp('aux.csv'), fp('papers.csv'))

    # Comprovació que s'ha escrit correctament la variable 'published'
    # aux = []
    # with open('papers.csv', mode='r') as file: 
    #     reader = csv.reader(file, delimiter=';')
    #     next(reader)
    #     aux = [ row[7] for row in reader ]
    # aux = [ x == 'Yes' for x in aux ]
    # print('Accepted: %d / 2000\t(%d perc.)' % (sum(aux), sum(aux)*100/2000))
    # sys.exit(0)

    # ------
    # PAS 3:
    # ------
    # Assignem tots els papers acceptats a una Conference o un Journal
    # (exactament el mateix procediment que feiem directament des d'un inici a 
    # 'data-generator.py', però únicament assignant Conferences i Journals)

    # Obtenim tots els papers (publicats i no publicats per separat)
    published_papers = get_ids_published_papers(fp('papers.csv'))

    # Fem l'assignació de Conference/Journal
    for paper in published_papers: 
        if numpy.random.random_sample() < 0.5: # CONFERENCE
            edition = random.choice(conference_editions)
            isPublishedInConference.writerow([paper] + edition)
        else: # JOURNAL
            volume = random.choice(journal_volumes)
            isPublishedInJournal.writerow([paper] + volume)

    # Tanquem tots els fitxers oberts anteriorment
    cites_file.close()
    hasMainAuthor_file.close()
    hasCoAuthor_file.close()
    hasReviewer_file.close()
    hasKeyword_file.close()
    isPublishedInJournal_file.close()
    isPublishedInConference_file.close()

    # Final del programa
    infomsg('Data generated successfully!\n')





