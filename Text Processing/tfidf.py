import csv
import re
import math
from collections import defaultdict, Counter
# PART ONE: PREPROCESSING
def preprocessing(docfile):
    cleanwords = []
    with open(docfile) as dfile:
        for line in dfile:
            # Clean the document
            cleaned = re.sub(r'http\S+', '', line)
            cleaned = re.sub(r'[^\w\s]', '', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned)
            cleaned = cleaned.replace('\n', '')
            # convert to lowercase
            cleaned = cleaned.lower()
            # remove stopwords
            stopwords = getstopwords('stopwords.txt')
            for word in cleaned.split():
                if not re.match(r'^https?://\S+', word):
                    if word not in stopwords:
                        # stemming and lemmatization
                        word = re.sub(r'ing$', '', word)
                        word = re.sub(r'ly$', '', word)
                        word = re.sub(r'ment$', '', word)
                        cleanwords.append(word)
    return cleanwords
def getstopwords(f):
    stopwords = []
    with open(f) as stopwordfile:
        for line in stopwordfile:
            word = line.strip()
            stopwords.append(word)
    return stopwords
def getdocfilenames(f):
    docfilenames = []
    with open(f) as tdfile:
        for line in tdfile:
            docname = line.strip()
            docfilenames.append(docname)
    return docfilenames
# taking tfidf_docs.txt as input and creates preproc file
def createpreprocfile(f):
    # f is tfidf_doc.txt
    docfilenames = getdocfilenames(f)
    preprocfilelist = []
    for docfilename in docfilenames:
        cleanwords = preprocessing(docfile=docfilename)
        preprocname = "preproc_"+docfilename
        with open(preprocname, 'w') as preprocfile:
            preprocfile.write(' '.join(cleanwords))
            preprocfilelist.append(str(preprocname))
    return preprocfilelist

# PART TWO: COMPUTING TF-IDF SCORES
# step a: compute frequencies of each word in a document
def computefrequencies(preprocfile):
    wordfreq = Counter()
    with open(preprocfile) as pfile:
        for line in pfile:
            words = line.split()
            wordfreq.update(words)
    return wordfreq
# step b: compute term frequence for each term
def computetf(wordfreq):
    wfreq = {}
    totalcount = sum(wordfreq.values())
    for word, counter in wordfreq.items():
        wfreq[word] = round(counter/totalcount, 2)
    return wfreq
def computetfscores(preprocfile): # returns dictionary of word:tf scores
    wordfreq = computefrequencies(preprocfile=preprocfile)
    tf = computetf(wordfreq= wordfreq)
    return tf
# step c: compute inverse document frequence
def findnumberofdocumentswordisfoundin(word, preprocfilelist):
    numberofdocs = 0
    # go through every word in all of the preprocfiles in preproclist
    for preprocfile in preprocfilelist:
        with open(preprocfile) as pfile:
            for line in pfile:
                words = line.split()
                # if word is found, increment number of docs
                if word in words:
                    numberofdocs += 1
                    break
        # go to next document
    # return numberofdocs
    return numberofdocs
def computeidf (preprocfilelist) : # returns dictionary of word:idf scores
    # find total number of documents
    totalnumberofdocs = len(preprocfilelist)
    # create a dictionary (k: word, v: idf)
    idf = {}
    # for each word in preprocfile in preprocfilelist
    for preprocfile in preprocfilelist:
        with open(preprocfile) as pfile:
            for line in pfile:
                words = line.split()
                for word in words:
                    # if word not in idf dictionary
                    if word not in idf:
                        # find numberofdocs
                        numberofdocs = findnumberofdocumentswordisfoundin(word= word, preprocfilelist=preprocfilelist)
                        # find idf using formula
                        log = float(math.log((totalnumberofdocs)/numberofdocs))
                        idf[word] = (log) + 1.0
    return idf
# step d: compute tf*idf
def computetfidf(tf, idf):
    tfidf = {} # word: tfidf score
    # get word from tf dictionary
    for word, tfval in tf.items():
        # if word in idf dictionary
        if word in idf:
            idfval = idf[word]
            # get tf-idf value (tf*idf, round to 2 decimals)
            tfidfval = round(tfval*idfval, 2)
            # store word: tf-idf in tfidf dictionary
            tfidf[word] = tfidfval
    return tfidf
# step e: print list of top 5 tf-idf scores
def gettop5(tfidf):
    sortedtfidf = sorted(tfidf.items(), key=lambda x: (-x[1], x[0]))
    sortedtfidf = sortedtfidf[:5]
    return sortedtfidf
def printtop5(f, filenum, tfidf):
    sortedtfidf = gettop5(tfidf=tfidf)
    docfilenames = getdocfilenames(f)
    docfilename = docfilenames[filenum]
    tfidfname = "tfidf_"+docfilename
    with open(tfidfname, 'w') as tfidffile:
        tfidffile.write(str(sortedtfidf))

# MAIN
def tfidf():
    # PART ONE:
    preprocfilelist = createpreprocfile('tfidf_docs.txt')
    # PART TWO:
    filenum = 0
    for preprocfile in preprocfilelist:
        tf = computetfscores(preprocfile= preprocfile)
        idf = computeidf(preprocfilelist=preprocfilelist)
        tfidf = computetfidf(tf=tf, idf=idf)
        printtop5(f='tfidf_docs.txt', filenum= filenum, tfidf=tfidf)
        filenum += 1

tfidf()