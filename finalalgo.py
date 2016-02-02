from pymongo import MongoClient
import random
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants
dbmatches = db.matches

#MAY NEED TO CHANGE Question names
QUESTIONS = ['class', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
MATRICES = [list(), list(), list(), list(), list()]      #an list of matrices
XY_GUIDE = [['man', 'woman'], ['man', 'man'], ['woman', 'woman'], ['man', 'nonbinary'], ['woman', 'nonbinary']]
COORD_TO_ID = [[dict(), dict()], [dict(), dict()], [dict(), dict()], [dict(), dict()], [dict(), dict()]]

entry_dict = dict()
entry_list = list()

class Heap(object):
        def __init__(self, count, match_dict, heap):
                self.count = count
                self.match_dict = match_dict
                self.heap = heap
        def swap(self, a, b):
                temp =self.heap[a]
                self.heap[a]=self.heap[b]
                self.heap[b] = temp
                
        def sift_up(self, pos):
                if pos>1:
                        parent = pos/2
                        if self.heap[pos]>self.heap[parent]:
                                self.swap(pos, parent)
                                self.sift_up(parent)
                                
        def insert(self, num):
                self.heap.append(num)
                self.count+=1
                self.sift_up(self.count)
                
        def sift_down(self, pos):
                first_child_ix = 2*pos
                second_child_ix = 2*pos+1

                if first_child_ix==self.count: #heap has one child
                        if self.heap[pos]>self.heap[first_child_ix]:
                                self.swap(pos, first_child_ix)
                elif first_child_ix<self.count:
                        biggest = second_child_ix
                        if self.heap[first_child_ix]>self.heap[second_child_ix]:
                                biggest = first_child_ix
                        if self.heap[pos]<self.heap[biggest]:
                                self.swap(pos, biggest)
                                self.sift_down(biggest)

        def remove_max(self):
                if self.count==0:
                        return -1
                result = self.heap[1]
                self.heap[1]=self.heap[self.count]
                self.count-=1
                self.sift_down(1)
                return result
                
def makeMatrix (target_gender, seeking_gender, matrix_type):
        global COORD_TO_ID
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

##        for i in range(xindex):
##                matrix.append([0 for i in range(yindex)])
        matrix = [[0 for j in range(yindex)] for i in range(xindex)]
        for x in range(xindex):
                x_entry = xdict[x]
                for y in range(yindex):
                        y_entry = ydict[y]
                        for q in QUESTIONS:
                                if x_entry[q]==y_entry[q]:
                                        matrix[x][y]+=1
        return matrix


def frommatrix_toheap(matrixnum, target, gender_combo, target_gender, heap):
        matrix = MATRICES[matrixnum]

        num_seeking=0
        if gender_combo[0]==target_gender:
                num_seeking = len(matrix[0])
                xOrY =1
        else:
                num_seeking = len(matrix)
                xOrY=0
        
        for seeking in range(num_seeking):
                if xOrY==1:
                        num_matches = matrix[target][seeking]
                else:
                        num_matches = matrix[seeking][target]
                seeking_id = COORD_TO_ID[matrixnum][xOrY][seeking]
                if num_matches in heap.match_dict:
                        heap.match_dict[num_matches].append(seeking_id)
                else:
                       heap.match_dict[num_matches] = [seeking_id]
                       heap.insert(num_matches)
        return heap

def init_matrices():
        global MATRICES
        global XY_GUIDE
        for entry in participants.find():
                name = entry['_id']
                entry_dict[name]=dict()
                entry_list.append(name)
        for i in range(5):
                MATRICES[i]=makeMatrix(XY_GUIDE[i][0], XY_GUIDE[i][1], i)

def put_in_database(_id, matches):
        match_dict = dict()

        for match in matches:
                if match!="NaN":
                        for p in participants.find( { '_id': match } ):
                                info = [p['name'], p['phone']]
                                match_dict[match]=info
                else:
                        match_dict[match]=["NaN", "NaN"]
        
        for entry in participants.find( { '_id': _id } ):
                m0= matches[0]
                print m0
                m1 = matches[1]
                m2 = matches[2]
                person = {
                        "_id": _id,
                        "name": entry['name'],
                        "email": entry['email'],
                        "m0": match_dict[m0][0],
                        "p0":  match_dict[m0][1],
                        "m1": match_dict[m1][0],
                        "p1":  match_dict[m1][1],
                        "m2": match_dict[m2][0],
                        "p2":  match_dict[m2][1]
                        }
                dbmatches.insert(person)
                

#shuffle at end
def main():
        global entry_list
        global entry_dict
        global MATRICES
        global XY_GUIDE
        init_matrices()
        for _id in entry_list:
                heap = Heap(0, dict(), [0])
                matrixnums_to_coords = entry_dict[_id]
                for matrixnum in range(5):
                        if matrixnum in matrixnums_to_coords:
                                target = matrixnums_to_coords[matrixnum]
                                gender_combo = XY_GUIDE[matrixnum]
                                target_gender = matrixnums_to_coords['gender']
                                heap = frommatrix_toheap(matrixnum, target, gender_combo, target_gender, heap)
                #print "for ", _id
                ix = 0
                num = heap.remove_max()
                final_matches = list()
                #ENSURE MATCHES ARE TWO WAY?
                while ix<3 and num!=-1:
                        matches = heap.match_dict[num]
                        #print num, " : ", matches
                        
                        if len(matches) >1:
                                random.shuffle(matches)
                                for match in matches:
                                        if ix<3:
                                                final_matches.append(match)
                                                ix+=1
                        else:
                                final_matches.append(matches[0])
                        num = heap.remove_max()
                        ix+=1
                        
                slack = 3-len(final_matches)
                for i in range(slack):
                        final_matches.append("NaN")
                put_in_database(_id, final_matches)

main()
