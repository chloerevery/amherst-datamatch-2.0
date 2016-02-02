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
        def update_best(self, prev_same, prev_matches):
                self.best_same=prev_same
                self.best_matches = prev_matches

class Heap(object):
        """A class that describes nodes in our heap"""
        def __init__(self, count, heap):
                self.count = count
                self.heap = heap
        def swap(self, a, b):
                temp =self.heap[a]
                self.heap[a]=self.heap[b]
                self.heap[b] = temp
                
        def sift_up(self, pos):
                if pos>1:
                        parent = pos/2
                        if self.heap[pos].best_same>self.heap[parent].best_same:
                                self.swap(pos, parent)
                                self.sift_up(parent)
                                
        def insert(self, node):
                if node.best_same==self.heap[self.count].best_same:
                        self.heap[self.count].best_matches.append(node.best_matches)
                else
                        self.heap.append(node)
                        self.count+=1
                        self.sift_up(self.count)
                
        def sift_down(self, pos):
                first_child_ix = 2*pos
                second_child_ix = 2*pos+1

                if first_child_ix==self.count: #heap has one child
                        if self.heap[pos].best_same>self.heap[first_child_ix].best_same:
                                self.swap(pos, first_child_ix)
                elif first_child_ix<count:
                        biggest = second_child_ix
                        if self.heap[first_child_ix].best_same>self.heap[second_child_ix].best_same:
                                biggest = first_child_ix
                        if self.heap[pos].best_same<self.heap[biggest].best_same:
                                self.swap(pos, biggest)
                                self.sift_down(biggest)

        def remove_max(self):
                if self.count==0:
                        print "There's nothing here"
                        return 0
                result = self.heap[1]
                self.heap[1]=self.heap[self.count]
                self.count-=1
                self.sift_down[1]
                return result
                
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


def from_one_matrix(matrixnum, target, gender_combo, target_gender, heap):
        matrix = MATRICES[matrixnum]

        num_seeking=len(matrix)
        xOrY=0
        if gender_combo[0]==target_gender:
                num_seeking = len(matrix[0])
                xOrY =1
        
        for seeking in range(num_seeking):
                num_matches = matrix[target][seeking]
                if num_matches>result[0].best_same:
                        for i in range(2, 0, -1):
                                result[i].update_best(result[i-1].best_same, list(result[i-1].best_matches))
                        result[0].best_same = num_matches
                seeking_id = COORD_TO_ID[matrixnum][xOrY][seeking]
                for num in range (3):
                        if result[num].best_same==num_matches:
                                result[num].best_matches.append(seeking_id)
        return result

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

def node_print(heap):
        for ix in range(1, len(heap)):
                print heap[ix].best_same, " : ", heap[ix].best_matches

#shuffle at end
def main():
        global entry_list
        global entry_dict
        global MATRICES
        global XY_GUIDE
        init_matrices()
        for _id in entry_list:
                heap = Heap(0, [0])
                matrixnums_to_coords = entry_dict[_id]
                for matrixnum in range(5):
                        if matrixnum in matrixnums_to_coords:
                                target = matrixnums_to_coords[matrixnum]
                                gender_combo = XY_GUIDE[matrixnum]
                                target_gender = matrixnums_to_coords['gender']
                                heap = from_one_matrix(matrixnum, target, gender_combo, target_gender, heap)

main()
