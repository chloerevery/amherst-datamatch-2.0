from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants

#MAY NEED TO CHANGE Question names
QUESTIONS = ['class', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
MATRICES = [list(), list(), list(), list(), list()]      #an list of matrices
XY_GUIDE = [['man', 'woman'], ['man', 'man'], ['woman', 'woman'], ['man', 'nonbinary'], ['woman', 'nonbinary']]
COORD_TO_ID = [[dict(), dict()], [dict(), dict()], [dict(), dict()], [dict(), dict()], [dict(), dict()]]

entry_dict = dict()
entry_list = list()

class Node(object):
        """A class that describes nodes in our heap"""
        def __init__(self, best_same, best_matches):
                self.best_same = best_same
                self.best_matches = best_matches
        def update_best

def makeMatrix (target_gender, seeking_gender, matrix_type):
        global COORD_TO_ID
        matrix = list()
        xdict = dict()
        xindex=0
        ydict = dict()
        yindex=0
        for x in participants.find( { 'gender' : target_gender , seeking_gender: 1 }):
                _id = x['_id']
                entry_dict[_id][matrix_type] = xindex
                entry_dict[_id]['gender']=target_gender
                COORD_TO_ID[matrix_type][0][xindex]=_id
                xdict[xindex] = x
                xindex+=1
        for y in participants.find( { 'gender' : seeking_gender , target_gender: 1 }):
                _id = y['_id']
                entry_dict[_id][matrix_type] =yindex
                entry_dict[_id]['gender']=seeking_gender
                COORD_TO_ID[matrix_type][1][yindex]=_id
                ydict[yindex]=y
                yindex+=1

        for i in range(xindex):
                matrix.append([0 for i in range(yindex)])
        for x in range(xindex):
                x_entry = xdict[x]
                for y in range(yindex):
                        y_entry = ydict[y]
                        for q in QUESTIONS:
                                if x_entry[q]==y_entry[q]:
                                        matrix[x][y]+=1
        return matrix


def find3best(matrixnum, target, gender_combo, target_gender):
        result = list()
        for ix in range(3):
                node = Node(0, list())
                result.append(node)
##        best_matches = [list(), list(), list()]
##        best_same = [0, 0, 0]
        matrix = MATRICES[matrixnum]

        num_seeking=len(matrix)
        xOrY=0
        if gender_combo[0]==target_gender:
                num_seeking = len(matrix[0])
                xOrY =1
        
        for seeking in range(num_seeking):
                num_matches = matrix[target][seeking]
                if num_matches>best_same[0]:
                        for i in range(2, 0, -1):
                                best_same[i]=best_same[i-1]
                                best_matches[i]= list(best_matches[i-1])
                        best_same[0] = num_matches
                seeking_id = COORD_TO_ID[matrixnum][xOrY][seeking]
                for num in range (3):
                        if best_same[num]==num_matches:
                                best_matches[num].append(seeking_id)
        best_same.append(best_matches)
        return best_same

def init_matrices():
        global MATRICES
        global XY_GUIDE
        for entry in participants.find():
                name = entry['_id']
                entry_dict[name]=dict()
                entry_list.append(name)
        for i in range(5):
                MATRICES[i]=makeMatrix(XY_GUIDE[i][0], XY_GUIDE[i][1], i)
                print MATRICES[i]

#shuffle at end
def main():
        global entry_list
        global entry_dict
        global MATRICES
        global XY_GUIDE
        init_matrices()
        for _id in entry_list:
                matrixnums_to_coords = entry_dict[_id]
                for matrixnum in range(5):
                        if matrixnum in matrixnums_to_coords:
                                target = matrixnums_to_coords[matrixnum]
                                gender_combo = XY_GUIDE[matrixnum]
                                target_gender = matrixnums_to_coords['gender']
                                matches = find3best(matrixnum, target, gender_combo, target_gender)
                                print matches

main()
