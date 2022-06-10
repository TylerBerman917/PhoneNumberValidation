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

def get_json_rows_from_csv(csv_file_name):
    # open CSV file with error handling
    # add utf encoding or the BOM (byte order mark) appears before Phone Number
    try:
        file = open(csv_file_name, mode='r', encoding='utf-8-sig')
        # print "File opened" if opened successfully.
        print("File opened")

    except IOError:
        # print "Unable to open file" if not able to open the file (i.e file does not exist).
        print("Unable to open file")
    else:
        with file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            # create an empty list to add row data into
            rows = []
            # use a for loop to pull rows out of csv one by one
            for row in csvreader:
                rows.append(row)
        file.close()

    # convert rows into json string for next function
    json_rows = json.dumps(rows)
    return json_rows


def get_formatted_phone_numbers(json_rows):
    # create an empty list to add formatted phone numbers into
    formatted_phone_numbers = []
    # parse through csv file & pull out the US phone numbers.
    # US can be replaced with any country in ISO Alpha-2 format: https://countrycode.org/
    for phone_number in phonenumbers.PhoneNumberMatcher(json_rows, "US"):
        # format the US phone numbers with a country code (+1) in E.164 format
        formatted_phone = phonenumbers.format_number(phone_number.number, phonenumbers.PhoneNumberFormat.E164)
        # add formatted_phone into the formatted_phone_numbers list
        formatted_phone_numbers.append(formatted_phone)
    return formatted_phone_numbers


def get_location_details(formatted_phone_numbers):
    # create an empty list to add Profile data into
    profile_data = []
    for formatted_phone_number in formatted_phone_numbers:
        # reformat the phone number for next functions
        validated_phone = phonenumbers.parse(formatted_phone_number)
        # in a future iteration, write to a new csv file if the functions below are false &/or write the phone numbers that were not pulled out in the PhoneNumberMatcher function
        # this function evaluates as true if the phone number has the correct # of characters & if it is a valid phone number
        if phonenumbers.is_possible_number(validated_phone) and phonenumbers.is_valid_number(validated_phone):
            # pull out country from phone number
            territory = geocoder.country_name_for_number(validated_phone, "en")

            # predict language based on country
            country = CountryInfo(territory)
            language = country.languages()

            # in a future iteration, pull out timezone from the phone number variable

            profile_data.append(
                {
                "phone_number": formatted_phone_number,
                "$country": territory,
                "language": language,
                "sms_consent": True
                }
            )
    return profile_data


def send_grouped_profile_data_to_klaviyo(profile_data):
    # group profile_data list into batches of 100 using indexing to account for API rate limiting
    grouped_profiles = []
    for i in range(0, len(profile_data), 100):
        grouped_profiles.append(profile_data[i:i+100])

    # use subscribe endpoint: https://developers.klaviyo.com/en/reference/subscribe, which honors the opt-in settings of your subscriber List
    # API will respond with an empty list: [] if List is double opt-in. Users must confirm their subscription before they are added to your subscriber List
    url = "https://a.klaviyo.com/api/v2/list/" + LIST_ID + "/subscribe?api_key=" + PRIVATE_KEY

    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }

    # create a final payload with the profiles parameter for each group of 100 Profiles
    for group in grouped_profiles:
        final_payload = {"profiles": group}

        requests.post(url, json=final_payload, headers=headers)
        print("Profiles imported successfully. SMS Consent updated.")


csv_file_name = "csv_file_name_here"
json_rows = get_json_rows_from_csv(csv_file_name)
formatted_phone_numbers = get_formatted_phone_numbers(json_rows)
profile_data = get_location_details(formatted_phone_numbers)

PRIVATE_KEY = 'private API key, grab/create from Klaviyo > Accounts > Settings > API keys'
LIST_ID = '6 digit List ID, grab from Klaviyo List URL'
send_grouped_profile_data_to_klaviyo(profile_data)


# if SMS is not enabled, console returns "SMS configuration is required to subscribe phone number only profiles."
# if List doesn't exist, console returns "List does not exist."
