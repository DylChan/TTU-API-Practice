import json
import requests
# Read JSON file
response = requests.get(
    'https://v2.sherpa.ac.uk/cgi/retrieve?item-type=publication&format=Json&limit=1&offset=0&filter=%5B%5B%22title%22%2C%22equals%22%2C%22Applied%20Surface%20Science%22%5D%5D&api-key=4FB4B054-3ACC-11EE-AB97-40C413E8924B')
# Convert JSON to Python Object
data = response.text
parsed_json = json.loads(data)

publisher_policy = parsed_json['items'][0]['publisher_policy']
# need to break down the publisher_policy into its components
# important to look at: conditions, embargo, id, location, additional_oa_fee
publisher_policy_ids = []
# iterates through publisher policy and adds the ids to a list
for row in publisher_policy:
    publisher_policy_ids.append(row['id'])

publishers = parsed_json['items'][0]['publishers']
article_url = parsed_json['items'][0]['url']
issns = parsed_json['items'][0]['issns']
publication_id = parsed_json['items'][0]['id']
permitted_oa = []

for row in publisher_policy:
    if row['permitted_oa'][0]["additional_oa_fee"] == "no" and 'any_website' in row['permitted_oa'][0]['location']['location']:
        # might need to iterate through the permitted_oa list too
        permitted_oa.append(row['permitted_oa'][0])

# need to ask if we are looking at location or article version so that i know which permitted oa(s) we need
# maybe make separate lists for each type of article version

print(permitted_oa)
