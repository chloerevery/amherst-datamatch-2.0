# amherst-datamatch-2.0

Steps to run datamatch:
1. after all participants have taken the survey, run final_algo.py. This will populate the mongo database with participants, their emails, their matches, and their matches' phone numbers
2. run email_script.py. this uses sendgrid to send emails to all participants with their matches and their matches' phone numbers.
