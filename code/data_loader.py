import os, sys, shutil
from neo4j import GraphDatabase
from data_generator import welcomeMsg, infomsg

## -------------------------------------------------------------------------
## -- Some useful functions
## -------------------------------------------------------------------------

def clean_db(session):
    session.run('MATCH (n) DETACH DELETE n')

def macos():
    path = os.path.abspath('.')
    return path[1] != ':'

def get_abs_path():
    path = os.path.abspath('.')
    if path[1] == ':':
        path = path[2:]
    return path

def get_neo4j_path():
    if macos():
        return '/Users/arnau/Library/Application Support/Neo4j Desktop/Application/relate-data/dbmss/dbms-192f971e-48ea-48ae-9781-486d9e7a70b6/'
    else: 
        print('[ERROR] Unknown absolute neo4j path for windows.')
        sys.exit(1)

def move_file(orig, dest):
    res = ''
    if os.path.exists(orig):
        if os.path.exists(dest):
            os.remove(dest)
        shutil.copy(orig, dest)
        os.remove(orig)
    else: 
        res = '[ERROR] (move_file) File %s not found.' % orig
    return res


def parse_arguments():
    options = sys.argv[1:]
    if not options or ('load' not in options and 'store' not in options):
        # ('train' not in options and 'test' not in options) or \
        # ('train' in options and 'test' in options):
        print('[ERROR] No valid arguments provided')
        print('[USAGE] python3 data_loader.py load [store] [all]')
        print('        python3 data_loader.py [load] store [all]')
        sys.exit(1)
    return options

## -------------------------------------------------------------------------
## -- Start of the program
## -------------------------------------------------------------------------
if __name__ == '__main__':
    
    ## -------------------------------------------------------------------------
    ## -- Arguments parsing
    ## -------------------------------------------------------------------------

    options = parse_arguments()

    welcomeMsg('Data loader program')

    ## -------------------------------------------------------------------------
    ## -- Connecting to database (local)
    ## -------------------------------------------------------------------------
    db = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "arnaudaniel"))
    session = db.session()


    if 'load' in options: 
        ## -------------------------------------------------------------------------
        ## -- Removing previous data
        ## -------------------------------------------------------------------------
        infomsg('Removing previous data...')
        clean_db(session)

        path = get_abs_path()
        infomsg('Absolute path: %s\n' % path)

        statements = {
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Paper nodes
            ## -------------------------------------------------------------------------
            'papers':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/papers.csv' AS line FIELDTERMINATOR ';'
            CREATE (:Paper {id:line.id,
                            title: line.title, 
                            month: line.month, 
                            year: toInteger(line.year),
                            pages: toInteger(line.pages),
                            issn: line.issn,
                            abstract: line.abstract,
                            published: line.published}
                    )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Author nodes
            ## -------------------------------------------------------------------------
            'authors':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/authors.csv' AS line FIELDTERMINATOR ';'
            CREATE ( :Author {id:line.id, 
                              name: line.author, 
                              country: line.country}
                   )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Conference nodes
            ## -------------------------------------------------------------------------
            'conferences':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/conferences.csv' AS line FIELDTERMINATOR ';'
            CREATE (:Conference {name: line.name} )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Journal nodes
            ## -------------------------------------------------------------------------
            'journals':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/journals.csv' AS line FIELDTERMINATOR ';'
            CREATE (:Journal {name: line.name, 
                              online: line.online} 
                   )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Keyword nodes
            ## -------------------------------------------------------------------------
            'keywords':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/keywords.csv' AS line FIELDTERMINATOR ';'
            CREATE (:Keyword {id:line.id, 
                              name: line.name} 
                   )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Cites relations
            ## -------------------------------------------------------------------------
            'cites':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/cites.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Paper) WHERE a.id = line.start_id AND  b.id = line.end_id
            CREATE (a)-[r:CITES]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating hasMainAuthor relations
            ## -------------------------------------------------------------------------
            'hasMainAuthor':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/hasMainAuthor.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Author) WHERE a.id = line.start_id AND  b.id = line.end_id
            CREATE (a)-[r:HAS_AUTHOR {type:'MainAuthor'}]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating hasCoAuthor relations
            ## -------------------------------------------------------------------------
            'hasCoAuthor':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/hasCoAuthor.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Author) WHERE a.id = line.start_id AND  b.id = line.end_id
            CREATE (a)-[r:HAS_AUTHOR {type:'CoAuthor'}]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating hasKeyword relations
            ## -------------------------------------------------------------------------
            'hasKeyword':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/hasKeyword.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Keyword) WHERE a.id = line.start_id AND  b.id = line.end_id
            CREATE (a)-[r:HAS_KEYWORD]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating hasReviewer relations
            ## -------------------------------------------------------------------------
            'hasReviewer':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/hasReviewer.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Author) WHERE a.id = line.start_id AND  b.id = line.end_id
            CREATE (a)-[r:HAS_REVIEWER]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating isPublishedInConference relations
            ## -------------------------------------------------------------------------
            'isPublishedInConference':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/isPublishedInConference.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Conference) WHERE a.id = line.paper_id AND  b.name = line.conference_name
            CREATE (a)-[r:EDITION { number:toInteger(line.edition), 
                                    city:line.city, 
                                    year:toInteger(line.year)}]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating isPublishedInJournal relations
            ## -------------------------------------------------------------------------
            'isPublishedInJournal':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/isPublishedInJournal.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper), (b:Journal) WHERE a.id = line.paper_id  AND  b.name = line.journal_name
            CREATE (a)-[r:VOLUME { number:toInteger(line.volume), 
                                    month:line.month, 
                                    year:toInteger(line.year),
                                    pages:toInteger(line.npages),
                                    issn:line.issn} ]->(b)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Updating hasReviewer relations
            ## -------------------------------------------------------------------------
            'hasReviewer':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/hasReviewer.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Paper)-[r:HAS_REVIEWER]->(b:Author) WHERE a.id = line.start_id AND  b.id = line.end_id
            SET r.description = line.description,
                r.decision = line.decision
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating University nodes
            ## -------------------------------------------------------------------------
            'universities':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/universities.csv' AS line FIELDTERMINATOR ';'
            CREATE (:University {name: line.name, country:line.country} )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating Company nodes
            ## -------------------------------------------------------------------------
            'companies':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/individuals/companies.csv' AS line FIELDTERMINATOR ';'
            CREATE (:Company {name: line.name} )
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating affiliatedTo relations (author->university)
            ## -------------------------------------------------------------------------
            'affiliatedToUniversity':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/affiliatedTo.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Author), (u:University) WHERE a.id = line.author_id  AND u.name = line.name
            CREATE (a)-[r:AFFILIATED_TO]->(u)
            ''',
            ## -------------------------------------------------------------------------
            ## -- Loading/Instantiating affiliatedTo relations (author->company)
            ## -------------------------------------------------------------------------
            'affiliatedToCompany':'''
            LOAD CSV WITH HEADERS FROM 'file://%s/data/relations/affiliatedTo.csv' AS line FIELDTERMINATOR ';'
            MATCH (a:Author), (c:Company) WHERE a.id = line.author_id  AND c.name = line.name
            CREATE (a)-[r:AFFILIATED_TO]->(c)
            '''
        }

        ## -------------------------------------------------------------------------
        ## -- Executing previous statements
        ## -------------------------------------------------------------------------
        data_to_load = ['papers', 'authors', 'hasMainAuthor', 'hasCoAuthor', 'hasReviewer']
        for id in statements:
            if 'all' in options or id in data_to_load:
                if not 'all' in options: 
                    data_to_load.remove(id)
                infomsg('Loading %s...' % id)
                session.run(statements[id] % path)
        if not 'all' in options and data_to_load:
            print('[WARNING] Some required data couldn\'t be loaded:', data_to_load)
        print()

    if 'store' in options:
        # Declaring path variables
        # split = 'train' if 'train' in options else 'test'
        filename = 'graph.graphml'
        neo4jpath = get_neo4j_path() + filename
        datapath = './data/' + filename
        # Storing graph to Neo4j default folder
        infomsg('Storing graph at %s\n' % datapath)
        session.run('CALL apoc.export.graphml.all("%s", {useTypes:true})' % filename)
        # Moving file to ./data/ folder
        res = move_file(neo4jpath, datapath)
        if res: 
            print(res)
            sys.exit(1)

    db.close()
