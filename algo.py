from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants

#MAY NEED TO CHANGE Question names
questions = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
straight_male_dict = dict()
male_ix=0
straight_female_dict = dict()
female_ix=0
for m in participants.find( { 'gender' : 'man' , 'seeking':'woman' }):
        straight_male_dict[male_ix] = m
        male_ix+=1
for w in participants.find( { 'gender' : 'woman' , 'seeking':'man' }):
        straight_female_dict[female_ix]=w
        female_ix+=1

straight_matrix = []
for i in range(male_ix):
        straight_matrix.append([0 for i in range(female_ix)])
for x in range(male_ix):
        m_entry = straight_male_dict[x]
        for y in range(female_ix):
                f_entry = straight_female_dict[y]
                for q in questions:
                        if m_entry[q]==f_entry[q]:
                                straight_matrix[x][y]+=1
print(straight_matrix)

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

#shuffle at end
                        
gay_matrix=[]
lesb_matrix=[]
nb_matrix=[]
