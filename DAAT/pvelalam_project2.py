import sys
inputfile = sys.argv[1]
outfile = sys.argv[2]
queryfile = sys.argv[3]
dictInvertedIndex = {}
dictDocTerms = {}
with open(inputfile, 'r') as infile:
    for line in infile:
        currTokens = line.rstrip().split('\t')
        currDocid = currTokens[0]
        currTerms = currTokens[1].split(' ')
        dictDocTerms[currDocid] = len(currTerms)
        tempDict = {}
        for term in currTerms:
            if term in tempDict:
                tempDict[term][1] += 1
            else:
                tempDict[term] = [currDocid, 1]
        for term in tempDict:
            if term in dictInvertedIndex:
                dictInvertedIndex[term].append(tempDict[term])
            else:
                dictInvertedIndex[term] = [tempDict[term]]

def getPostingLists(term):
    if(term in dictInvertedIndex):
        return dictInvertedIndex[term]
    else:
        return []

def andDAAT(currPostingList):
    dl = len(dictDocTerms)
    comp = 0
    res = []
    l = len(currPostingList)
    empty = False
    b = False
    scores = []
    if len(currPostingList) == 0:
        return res, 0, scores
    if len(currPostingList) == 1 and len(currPostingList[0])==0:
        return res, 0, scores
    dID = currPostingList[0][0][0]
    tfIdf = 0
    count = 1
    tfIdf = (currPostingList[0][0][1]/dictDocTerms[currPostingList[0][0][0]])*(dl/len(currPostingList[0]))
    indexDict = {}
    for i in range(len(currPostingList)):
        indexDict[i] = 0
    init = True
    indexDict[0] = 1

    if (1 >= len(currPostingList[0])):
        empty = True
    # print (currPostingList)
    if len(currPostingList) == 1:
        for i in range(len(currPostingList[0])):
            tfIdf = (currPostingList[0][i][1]/dictDocTerms[currPostingList[0][i][0]])*(dl/len(currPostingList[0]))
            scores.append(tfIdf)
            res.append(currPostingList[0][i][0])
        return res, 0, scores
    while(not b):
        for i in range(len(currPostingList)):
            if init:
                init = False
                continue
            if len(currPostingList[i]) == 0:
                empty = True
                b = True
                break
            j = indexDict[i]
            if j >= len(currPostingList[i]):
                b = True
                break
            while (currPostingList[i][j][0] < dID):
                comp = comp + 1
                j = j + 1
                if j >= len(currPostingList[i]):
                    b = True
                    break
            if j >= len(currPostingList[i]):
                b = True
                break
            # comp = comp + 1
            if (currPostingList[i][j][0] == dID):
                tfIdf = tfIdf + (currPostingList[i][j][1]/dictDocTerms[currPostingList[i][j][0]])*(dl/len(currPostingList[i]))
                count = count + 1
                comp = comp + 1
                j = j + 1
                indexDict[i] = j
                if count == l:
                    res.append(dID)
                    scores.append(tfIdf)
                    if empty:
                        b = True
                        comp = comp + 1
                        break
                    count = 1
                    if j < len(currPostingList[i]):
                        dID = currPostingList[i][j][0]
                        tfIdf = (currPostingList[i][j][1]/dictDocTerms[currPostingList[i][j][0]])*(dl/len(currPostingList[i]))
                        indexDict[i] = j + 1
                    else:
                        empty = True
                        b = True
                        break
                if j >= len(currPostingList[i]):
                    empty = True
                    indexDict[i] = j

            else:
                count = 1
                comp = comp + 1
                if j < len(currPostingList[i]):
                    dID = currPostingList[i][j][0]
                    tfIdf = (currPostingList[i][j][1]/dictDocTerms[currPostingList[i][j][0]])*(dl/len(currPostingList[i]))
                    indexDict[i] = j + 1
                else:
                    empty = True
                    b = True
                    break

    return res, comp, scores

def DaaTOR(currPostingList):
    dl = len(dictDocTerms)
    comp = 0
    tfIdf = 0
    scores = []
    listdoneDict = {}
    res = []
    for i in range(len(currPostingList)):
        if (len(currPostingList[i]) == 0):
            listdoneDict[i] = True
        else:
            listdoneDict[i] = False
    indexDict = {}
    minList = []
    for i in range(len(currPostingList)):
        indexDict[i] = 0
    while (True):
        mini = -1
        i = 0
        for i in range (len(currPostingList)):
            if (not listdoneDict[i]):
                mini = currPostingList[i][indexDict[i]][0]
                minList.append(i)
                break
        if mini == -1:
            break

        i = i+1
        # if i+1 == len(currPostingList):
        #     indexDict
        for j in range(i, len(currPostingList), 1):
            if (not listdoneDict[j]):
                if (currPostingList[j][indexDict[j]][0] < mini):
                    mini = currPostingList[j][indexDict[j]][0]
                    minList.clear()
                    minList.append(j)
                elif (currPostingList[j][indexDict[j]][0] == mini):
                    minList.append(j)
                comp = comp + 1
        res.append(mini)
        # print(minList)
        tfIdf = 0
        for index in minList:
            tfIdf = tfIdf + (currPostingList[index][indexDict[index]][1]/dictDocTerms[currPostingList[index][indexDict[index]][0]])*(dl/len(currPostingList[index]))
            indexDict[index] = indexDict[index] + 1
            if indexDict[index] >= len(currPostingList[index]):
                listdoneDict[index] = True
        scores.append(tfIdf)
        minList.clear()
    return res, comp, scores

# def cmp_items(a, b):
#     if a[0] < b[0]:
#         return 1
#     elif a[0] == b[0]:
#         return 0
#     else:
#         return -1

def scoreSort(docIDs, scores):
    pairL = []
    for i in range(len(docIDs)):
        pairL.append([scores[i], docIDs[i]])
    pairL.sort(key=lambda x: x[0], reverse = True)
    return pairL



output = open(outfile, 'w')

with open(queryfile, 'r') as infile:
    for line in infile:
        currQueryTerms = line.rstrip().split(' ')
        termPostingLists = []
        for query in currQueryTerms:
            # print(query)
            output.write("GetPostings\n")
            output.write(query + "\n")
            currPostingList = getPostingLists(query)
            output.write("Postings list:")
            if(len(currPostingList)>0):
                for docid in currPostingList:
                    output.write(" " + docid[0])
            else:
                output.write(" empty")
            output.write("\n")
            termPostingLists.append(currPostingList)

        # print(termPostingLists)
        ## AND Operation
        res, comp, scores = andDAAT(termPostingLists)
        pairs = scoreSort(res, scores)
        # print(pairs)
        output.write("DaatAnd" + "\n")
        output.write(line.rstrip() + "\n")
        output.write("Results: ")
        if(len(res)>0):
            for docs in res:
                output.write(docs + " ")
        else:
            output.write("empty")
        output.write("\n")
        output.write("Number of documents in results: {}".format(len(res)))
        output.write("\n")
        output.write("Number of comparisons: {}".format(comp))
        output.write("\n")
        output.write("TF-IDF" + "\n")
        output.write("Results: ")
        if(len(res)>0):
            for pair in pairs:
                output.write(pair[1] + " ")
        else:
            output.write("empty")
        output.write("\n")


        ## OR Operation
        res, comp, scores = DaaTOR(termPostingLists)
        pairs = scoreSort(res, scores)
        output.write("DaatOr" + "\n")
        output.write(line.rstrip() + "\n")
        output.write("Results: ")
        if(len(res)>0):
            for docs in res:
                output.write(docs + " ")
        else:
            output.write("empty")
        output.write("\n")
        output.write("Number of documents in results: {}".format(len(res)))
        output.write("\n")
        output.write("Number of comparisons: {}".format(comp))
        output.write("\n")
        output.write("TF-IDF" + "\n")
        output.write("Results: ")
        if(len(res)>0):
            for pair in pairs:
                output.write(pair[1] + " ")
        else:
            output.write("empty")
        output.write("\n")
        output.write("\n")


output.close()



