Solution Architect: Coding Challenge
Tyler Berman
tyler.berman@klaviyo.com

Phone Number Validation
Background:
There is a ton of friction when uploading phone numbers into Klaviyo for SMS consent. 
Often phone numbers are in an improper format, lack a country code or are phone numbers for countries that Klaviyo does not yet support for SMS messaging. 
This is one of our clients' first onboarding steps with SMS & the process can be extremely frustrating when phone #s aren’t successfully imported.

Solution:
(1) Programmatically parse out US phone numbers from a csv file.
(2) Reformat phone numbers into E.164.
(3) Capture country & language as additional properties.
(4) Upload SMS consent.

To get started:
(1) Download or clone the repository from Github.
(2) Create an .env file in the base directory of the project. 
(3) Create a Klaviyo account.
(4) Create a List in your Klaviyo account.
(5) Replace the following variables in your script:
    "csv_file_name.csv" - this is the name of your csv file
    PRIVATE - this is the private API key, which you can grab/create from Klaviyo > Accounts > Settings > API keys
    LIST_ID - this is the 6 digit List ID, which you can grab from the Klaviyo List's URL
    
  Things to note: 
    Ensure your csv file is in the same folder as your script.
    Including sample CSV - smsvalidatetesting.csv - for testing/formatting visualization.
    This script was written, created & debugged using Python 3.9 in PyCharm.
