import sendgrid

from smtpapi import SMTPAPIHeader

#mongo stuff
from pymongo import MongoClient
client=MongoClient('localhost', 27017)
db=client.amherst_datamatch
participants=db.participants

#create email message
sg = sendgrid.SendGridClient('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')
message = sendgrid.Mail()
message.set_headers({'X-Sent-Using': 'SendGrid-API', 'X-Transport': 'web'});
message.set_from('acdatamatch@gmail.com')
message.set_from_name("Amherst Datamatch")
message.set_replyto("acdatamatch@gmail.com")
message.add_bcc('acdatamatch@gmail.com') #not working?
message.set_subject(':name, Your True Love Matches!')
#set html
message.set_html('Hi :name,<br><br> Your matches are: <br><br> 1. :match1, :phone1 <br> 2. :match2, :phone2 <br> 3. :match3, :phone3. <br><br>You\'re super compatible! Shoot them a text and hang out sometime!')

#get match names and emails for each entry in the database, one entry at a time

emails = [] #create empty array for participant emails
names = [] #create empty array for participant names

first_matches = [] #create empty array for first matches' names
second_matches = [] #create empty array for second matches' names
third_matches = [] #create empty array for third matches' names

first_phones = [] #create empty array for first matches' phone numbers
second_phones = [] #create empty array for second matches' phone numbers
third_phones = [] #create empty array for third matches' phone numbers
    
for entry in participants.find():
    emails+= ??? #append the participant's email to the emails array
    
    names+= ??? #append the entry's name to the names array
    
    first_matches+= ??? #append that person's first match to the first_match array
    second_matches+= ??? #append that person's second match to the second_match array
    third_matches+= ??? #append that person's third match to the third_match array

    first_phones+= ??? #append the first match's phone number to the first_phones array
    second_phones+= ??? #append the second match's phone number to the second_phones array
    third_matches+= ??? #append the third match's phone number to the third_phones array

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


