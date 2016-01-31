from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants

#MAY NEED TO CHANGE Question names
QUESTIONS = ['class', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
MATRICES = [list(), list(), list(), list(), list()]      #an list of matrices
XY_GUIDE = [['man', 'woman'], ['man', 'man'], ['woman', 'woman'], ['man', 'nonbinary'], ['woman', 'nonbinary']]

entry_dict = dict()
entry_list = list()

def makeMatrix (target_gender, seeking_gender, matrix_type):
        matrix = list()
        xdict = dict()
        xindex=0
        ydict = dict()
        yindex=0
        for x in participants.find( { 'gender' : target_gender , seeking_gender: 1 }):
                _id = x['_id']
                entry_dict[_id][matrix_type] = xindex
                entry_dict[_id]['gender']=target_gender
                xdict[xindex] = x
                xindex+=1
        for y in participants.find( { 'gender' : seeking_gender , target_gender: 1 }):
                _id = y['_id']
                entry_dict[_id][matrix_type] =yindex
                entry_dict[_id]['gender']=seeking_gender
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


def find3best(matrix, target, num_seeking):
        best_matches = [list(), list(), list()]
        best_same = [0, 0, 0]
        
        for seeking in range(num_seeking):
                num_matches = matrix[target][seeking]
                if num_matches>best_same[0]:
                        for i in range(2, 0, -1):
                                best_same[i]=best_same[i-1]
                                best_matches[i]= list(best_matches[i-1])
                        best_same[0] = num_matches
                for num in range (3):
                        if best_same[num]==num_matches:
                                best_matches[num].append(seeking)
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
                                matrix = MATRICES[matrixnum]
                                target = matrixnums_to_coords[matrixnum]
                                num_seeking=0
                                gender_combo = XY_GUIDE[matrixnum]
                                target_gender = matrixnums_to_coords['gender']
                                if gender_combo[0]==target_gender:
                                        num_seeking = len(matrix[0])
                                else:
                                        num_seeking = len(matrix)
                                matches = find3best(matrix, target, num_seeking)
                                print matches

main()
