import sendgrid

from smtpapi import SMTPAPIHeader

#mongo stuff
from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants
matches = db.matches

#create email message
sg = sendgrid.SendGridClient('PUT KEY HERE')
message = sendgrid.Mail()
message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'});
message.set_from('acdatamatch@gmail.com')
message.set_from_name("Amherst Datamatch")
message.set_replyto("acdatamatch@gmail.com")
message.add_bcc('acdatamatch@gmail.com') #not working?
message.set_subject(':name, Your True Love Matches!')
#set html
message.set_html('Hi :name,<br><br> Your matches are: <br><br> :match1 :phone1 <br>:match2 :phone2 <br>:match3 :phone3. <br><br>You\'re super compatible! Shoot them a text and hang out sometime!')

#get match names and emails for each entry in the database, one entry at a time

emails = [] #create empty array for participant emails
names = [] #create empty array for participant names

first_matches = [] #create empty array for first matches' names
second_matches = [] #create empty array for second matches' names
third_matches = [] #create empty array for third matches' names

first_phones = [] #create empty array for first matches' phone numbers
second_phones = [] #create empty array for second matches' phone numbers
third_phones = [] #create empty array for third matches' phone numbers
    
for entry in matches.find():
    print(entry['email'])
    emails.append(entry['email']) #append the participant's email to the emails array
    
    names.append(entry['name']) #append the entry's name to the names array

    # a if test else b
    
    first_matches.append("" if entry['m0']=="NaN" else entry['m0']) #append that person's first match to the first_match array
    second_matches.append("" if entry['m1']=="NaN" else entry['m1']) #append that person's second match to the second_match array
    third_matches.append("" if entry['m2']=="NaN" else entry['m2']) #append that person's third match to the third_match array

    first_phones.append("" if entry['p0']=="NaN" else entry['p0']) #append the first match's phone number to the first_phones array
    second_phones.append("" if entry['p1']=="NaN" else entry['p1']) #append the second match's phone number to the second_phones array
    third_phones.append("" if entry['p2']=="NaN" else entry['p2']) #append the third match's phone number to the third_phones array

print("first_matches: ")
print(first_matches)
print("first_phones: ")
print(first_phones)
#set 'send to'
message.smtpapi.add_to(emails)

#set the substitutions for the email template
message.set_substitutions({':name': names,
                           ':match1': first_matches,
                           ':match2': second_matches,
                           ':match3': third_matches,
                           ':phone1': first_phones,
                           ':phone2': second_phones,
                           ':phone3': third_phones
                           })

#send that wildebeast!
sg.send(message)


