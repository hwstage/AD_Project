import pickle
dbfilename = 'scoreDB.dat'

def readScoreDB():
    try:
        fH = open(dbfilename, 'rb')
    except FileNotFoundError as e:
        return {}

    scdb = {}
    try:
        scdb =  pickle.load(fH)
    except:
        pass
    fH.close()
    return scdb

def recordScoreDB(scdb, name, score, difficulty, operator):
    if name in scdb:
        if operator not in scdb[name]:
            scdb[name] = {operator : [score]}
            if difficulty not in scdb[name][operator]:
                scdb[name][operator] = {difficulty : [score]}
            else:
                scdb[name][operator][difficulty].append(score)
        elif operator in scdb[name]:
            if difficulty not in scdb[name][operator]:
                scdb[name][operator][difficulty] = [score]
            else:
                scdb[name][operator][difficulty].append(score)
    elif name not in scdb:
        scdb[name] = {operator : {difficulty : [score]}}
# scdb = {"Song" : {"+" : {"Easy Mode": [100.0, 60.0], "Hard Mode" : [100.0, 20.0]}}}
    

def writeScoreDB(scdb):
    fH = open(dbfilename, 'wb')
    pickle.dump(scdb, fH)
    fH.close()