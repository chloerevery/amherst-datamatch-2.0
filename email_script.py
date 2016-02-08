import sendgrid

from smtpapi import SMTPAPIHeader

#mongo stuff
from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants
matches = db.matches

#create email message
sg = sendgrid.SendGridClient('<key here>')
message = sendgrid.Mail()
message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'});
message.set_from('acdatamatch@gmail.com')
message.set_from_name("Amherst Datamatch")
message.set_replyto("acdatamatch@gmail.com")
message.add_bcc('acdatamatch@gmail.com') #not working?
message.set_subject(':name, Your True Love Matches!')
#set html
message.set_html('Hi :name,<br><br> Your matches are: <br><br>:number1 :match1 :comma1 :phone1 <br>:number2 :match2 :comma2 :phone2 <br>:number3 :match3 :comma3 :phone3 <br><br>You\'re super compatible! Shoot them a text and hang out sometime!')

#get match names and emails for each entry in the database, one entry at a time

emails = [] #create empty array for participant emails
names = [] #create empty array for participant names

match1, match2, match3 = [], [], []
phone1, phone2, phone3 = [], [], []

number1, number2, number3 = [], [], []
comma1, comma2, comma3 = [], [], []
    
for entry in matches.find():
    print(entry['email'])
    emails.append(entry['email']) #append the participant's email to the emails array
    
    names.append(entry['name']) #append the entry's name to the names array
    
    # match names
    if entry['m0']=="NaN":
        match1.append("")
    else:
        match1.append(entry['m0']) #append that person's first match to the first_match array
        number1.append("1. ")
        commas1.append(", ")

    if entry['m1']=="NaN": 
        match2.append("")
    else:
        match2.append(entry['m1']) #append that person's second match to the second_match arra
        number2.append("2. ")
        comma2.append(", ")
        
    if entry['m2']=="NaN": 
        match3.append("") #append that person's third match to the third_match array
    else:
        match3.append(entry['m2'])
        number3.append("3. ")
        comma3.append(", ")

    #phones
    if entry['p0']=="NaN": 
        phone1.append("")
    else:
        phone1.append(entry['p0']) #append that person's first match's number to the first_phones array
        
    if entry['p1']=="NaN": 
        phone2.append("") #append that person's second match's number to the second_phones array
    else:
        phone2.append(entry['p1'])
        
    if entry['p2']=="NaN": 
        phone3.append("") #append that person's third match's number to the third_phones array
    else:
        phone3.append(entry['p2'])
 

print("match1: ")
print(match1
print("phone1: ")
print(phone1)
#set 'send to'
message.smtpapi.add_to(emails)

#set the substitutions for the email template
message.set_substitutions({':name': names,
                           ':match1': match1,
                           ':match2': match2,
                           ':match3': match3,
                           ':phone1': phone1,
                           ':phone2': phone2,
                           ':phone3': phone3,
                           ':number1': number1,
                           ':number2': number2,
                           ':number3': number3,
                           ':comma1': comma1,
                           ':comma2': comma2,
                           ':comma3': comma3
                           })

#send that wildebeast!
sg.send(message)


