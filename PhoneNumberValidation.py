import requests
import json
import phonenumbers
from phonenumbers import geocoder
from countryinfo import CountryInfo
import csv

# Background:
# There is a ton of friction when uploading SMS contacts into Klaviyo.
# This is one of our clients' first onboarding steps with SMS.
# The process can be extremely frustrating when phone #s aren’t successfully imported due to improper formatting.

# Solution:
# (1) Programmatically reformat phone #s in E.164 format.
# (2) Capture country & language as additional properties.
# (3) Upload SMS consent.

# Future considerations:
# (1) Consider this functionality be moved into the actual UI when uploading a CSV file of SMS contacts.
# (2) Consider iterating over each possible country that we service to pull out all viable phone numbers in a single csv.

# Relevant documentation:
# https://stackabuse.com/validating-and-formatting-phone-numbers-in-python/
# https://python.plainenglish.io/a-beginners-guide-to-formatting-csv-data-in-python-521421389fef
# https://stackoverflow.com/questions/5627425/what-is-a-good-way-to-handle-exceptions-when-trying-to-read-a-file-in-python

# open CSV file with error handling
# added utf encoding or the BOM (byte order mark) appears before Phone Number
try:
    file = open("csv_file_name.csv", mode='r', encoding='utf-8-sig')
    # Print "File opened" if opened successfully.
    print("File opened")

except IOError:
    # Print "Unable to open file" if not able to open the file (i.e file does not exist).
    print("Unable to open file")
else:
    with file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        # creating an empty list to add row data into
        rows = []
        # using a for loop to pull rows out of csv one by one
        for row in csvreader:
            rows.append(row)
    file.close()

# convert payload into json string for next function
json_rows = json.dumps(rows)

# parse through the csv & pull out the US phone numbers.
# US can be replaced with any country in ISO Alpha-2 format: https://countrycode.org/
for numbers in phonenumbers.PhoneNumberMatcher(json_rows, "US"):
    # formats the US phone numbers with a country code (+1) in E.164 format
    formatted_phone = phonenumbers.format_number(numbers.number, phonenumbers.PhoneNumberFormat.E164)
    # parses through the numbers (string) & converts to a phone number
    validated_phone = phonenumbers.parse(formatted_phone)
    # in a future iteration, write to a new csv file if the functions below are false &/or write the phone numbers that were not pulled out in the PhoneNumberMatcher function.
    print(formatted_phone)
    # is the phone number possible (i.e does it have the correct # of characters)
    if phonenumbers.is_possible_number(validated_phone) == True:
        print("Possible Number")
    else:
        print("Not a possible number")
    if phonenumbers.is_valid_number(validated_phone) == True:
        print("Valid Number")
    else:
        print("Not a valid number")

    # pull out country from phone number
    territory = geocoder.country_name_for_number(validated_phone, "en")

    # predict language based on country
    country = CountryInfo(territory)
    language = country.languages()

    # in a future iteration, pull out timezone from the phone number variable

    payload = {"profiles": [{
        "phone_number": formatted_phone,
        "$country": territory,
        "language": language,
        "sms_consent": True
        }]
        }

    json_payload = json.dumps(payload)

    PRIVATE = 'private API key, grab/create from Klaviyo > Accounts > Settings > API keys'
    LIST_ID = '6 digit List ID, grab from Klaviyo List URL'
    url = "https://a.klaviyo.com/api/v2/list/" + LIST_ID + "/subscribe?api_key=" + PRIVATE

    headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }

    response = requests.post(url, json_payload, headers=headers)
    print(response.text)

# If SMS is not enabled, console returns "SMS configuration is required to subscribe phone number only profiles."
