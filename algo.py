from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants

#MAY NEED TO CHANGE Question names
questions = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
straight_matrix = list()
gay_matrix = list()
lesbian_matrix = list()
men_seeking_nb = list()
women_seeking_nb = list()

entry_dict = dict()
entry_list = list()

def makeMatrix (target_gender, seeking_gender):
        matrix = list()
        xdict = dict()
        xindex=0
        ydict = dict()
        yindex=0
        for x in participants.find( { 'gender' : target_gender , 'seeking': seeking_gender }):
                xdict[xindex] = x
                xindex+=1
        for y in participants.find( { 'gender' : seeking_gender , 'seeking': target_gender }):
                ydict[yindex]=y
                yindex+=1

        for i in range(xindex):
                matrix.append([0 for i in range(yindex)])
        for x in range(xindex):
                x_entry = xdict[x]
                for y in range(yindex):
                        y_entry = ydict[y]
                        for q in questions:
                                if x_entry[q]==y_entry[q]:
                                        matrix[x][y]+=1
        return matrix

def find_3best(target, num_seeking, matrix):
        best_matches = [list(), list(), list()]
        best_same = [0, 0, 0]
        
        for seeking in range(num_seeking):
                num_matches = matrix[target][seeking]
                if num_matches>best_same[0]:
                        best_same[2]=best_same[1]
                        best_matches[2]=best_matches[1]
                        best_same[1] = best_same[0]
                        best_matches[1] =best_matches[0]
                        best_same[0] = num_matches
                        best_matches[0].append(num_matches)
                for num in range (3):
                        if best_same[num]==num_matches:
                                best_matches[num].append(num_matches)
        best_same.append(best_matches)
        return best_same

def init_matrices():
        for entry in participants.find():
                name = entry['name']
                entry_dict[name]=list()
                entry_list.append(name)
        global straight_matrix
        straight_matrix = makeMatrix('man', 'woman')
        global gay_matrix
        gay_matrix = makeMatrix('man', 'man')
        global lesbian_matrix
        lesbian_matrix = makeMatrix('woman', 'woman')
        global men_seeking_nb
        men_seeking_nb = makeMatrix('man', 'nonbinary')
        global women_seeking_nb
        women_seeking_nb = makeMatrix('woman', 'nonbinary')

#shuffle at end

def main():
        init_matrices()
