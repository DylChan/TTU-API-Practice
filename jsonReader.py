import json
import requests
import mysql.connector
# needs to read list of CSV titles and then get the following info from each JSON
# will temporarily make this the program that adds to database, will move to DatabasePopulater.py later


# Read JSON file
response = requests.get(
    'https://v2.sherpa.ac.uk/cgi/retrieve?item-type=publication&format=Json&limit=1&offset=0&filter=%5B%5B%22title%22%2C%22equals%22%2C%22Applied%20Surface%20Science%22%5D%5D&api-key=4FB4B054-3ACC-11EE-AB97-40C413E8924B')
# Convert JSON to Python Object
data = response.text
parsed_json = json.loads(data)

title = parsed_json['items'][0]['title'][0]['title']
sherpa_ID = parsed_json['items'][0]['id']
locations = ["any_website", "insitutional_repository", "named_repository"]

published_allowed = False
published_conditions = []
published_embargo = []
published_license = []

accepted_allowed = False
accepted_conditions = []
accepted_embargo = []
accepted_license = []

submitted_allowed = False
submitted_conditions = []
submitted_embargo = []
submitted_license = []

publisher_policy = parsed_json['items'][0]['publisher_policy']
# need to break down the publisher_policy into its components
# important to look at: conditions, embargo, id, location, additional_oa_fee

# publisher_policy_ids = []
# # iterates through publisher policy and adds the ids to a list
# for row in publisher_policy:
#     publisher_policy_ids.append(row['id'])

# article_url = parsed_json['items'][0]['url']
# issns = parsed_json['items'][0]['issns']

# permitted_oa = []
# print(row['permitted_oa'][0]['article_version'][0])
# print(row['permitted_oa'][0]['location']['location'])
# print(row['permitted_oa'][0]['additional_oa_fee'])


for row in publisher_policy:
    # checks for a fee, if we are under the location and article version is submitted
    for path in row['permitted_oa']:
        # print(path['article_version'][0])
        # print(path['location']['location'])
        # print(path['additional_oa_fee'])
        # if ('any_website' or 'insitutional_repository' or 'named_repository') in path['location']['location']:
        #     print('yes')
        #     print(path['location']['location'])
        if path["additional_oa_fee"] == "no" and any(ele in locations for ele in path['location']['location']) and path['article_version'][0] == 'submitted':
            submitted_allowed = True
            submitted_conditions.append(path['conditions'])
            if 'embargo' in path:
                submitted_embargo.append(path['embargo'])
            else:
                submitted_embargo.append('no embargo')
            if 'license' in path:
                submitted_license.append(path['license'][0]['license'])
            else:
                submitted_license.append('no license available')
    # repeat for each article version
        if path["additional_oa_fee"] == "no" and any(ele in locations for ele in path['location']['location']) and path['article_version'][0] == 'accepted':
            accepted_allowed = True
            accepted_conditions.append(path['conditions'])
            if 'embargo' in path:
                accepted_embargo.append(path['embargo'])
            else:
                accepted_embargo.append('no embargo')
            if 'license' in path:
                accepted_license.append(path['license'][0]['license'])
            else:
                accepted_license.append('no license available')
        if path["additional_oa_fee"] == "no" and any(ele in locations for ele in path['location']['location']) and path['article_version'][0] == 'published':
            published_allowed = True
            published_conditions.append(path['conditions'])
            if 'embargo' in path:
                published_embargo.append(path['embargo'])
            else:
                published_embargo.append('no embargo')
            if 'license' in path:
                published_license.append(path['license'][0]['license'])
            else:
                published_license.append('no license available')
    # repeat for each article version

# print(submitted_allowed)
# print(submitted_conditions)
# print(submitted_embargo)
# print(submitted_license)

# print(accepted_allowed)
# print(accepted_conditions)
# print(accepted_embargo)
# print(accepted_license)

# print(published_allowed)
# print(published_conditions)
# print(published_embargo)
# print(published_license)
# instead of printing, need to save to database

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Monty1010",
    database="journal_publishing_policy"
)

mycursor = db.cursor()

insert_stmt = ("INSERT INTO TITLE, SUBMITTED_ALLOWED, SUBMITTED_CONDITIONS, SUBMITTED_EMBARGO, SUBMITTED_LICENSE, ACCEPTED_ALLOWED, ACCEPTED_CONDITIONS, ACCEPTED_EMBARGO, ACCEPTED_LICENSE, PUBLISHED_ALLOWED, PUBLISHED_CONDITIONS, PUBLISHED_EMBARGO, PUBLISHED_LICENSE, SHERPA_ID, PUBLISHER_POLICY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)")

data = [(title, submitted_allowed, submitted_conditions, submitted_embargo, submitted_license, accepted_allowed, accepted_conditions,
         accepted_embargo, accepted_license, published_allowed, published_conditions, published_embargo, published_license, sherpa_ID, publisher_policy)]

try:
    mycursor.execute(insert_stmt, data)
    db.commit()
except:
    db.rollback()

print("Data inserted")
db.close()
