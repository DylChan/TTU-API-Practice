import json
import requests
import mysql.connector
import pandas as pd
# needs to read list of CSV titles and then get the following info from each JSON
journals = pd.read_csv("TTU_Journals_2022.csv")
firstThirty = journals[['Title']].head(30).values.tolist()


# will temporarily make this the program that adds to database, will move to DatabasePopulater.py later
for value in firstThirty:
    requestTitle = str(value)
    requestTitle = requestTitle.replace("'", "")
    requestTitle = requestTitle.replace("[", "")
    requestTitle = requestTitle.replace("]", "")
    unformattedTitle = requestTitle
    requestTitle = requestTitle.replace(" ", "%20")
    requestURL = ('https://v2.sherpa.ac.uk/cgi/retrieve?item-type=publication&format=Json&limit=1&offset=0&filter=%5B%5B%22title%22%2C%22equals%22%2C%22' +
                  requestTitle + '%22%5D%5D&api-key=4FB4B054-3ACC-11EE-AB97-40C413E8924B')
# Read JSON file
    response = requests.get(requestURL)
    # Convert JSON to Python Object
    data = response.text
    parsed_json = json.loads(data)

    if parsed_json['items'] == []:
        title = unformattedTitle
        sherpaID = '0'
        published_allowed = 0
        published_conditions = 'NA'
        published_embargo = 'NA'
        published_license = 'NA'

        accepted_allowed = 0
        accepted_conditions = 'NA'
        accepted_embargo = 'NA'
        accepted_license = 'NA'

        submitted_allowed = 0
        submitted_conditions = 'NA'
        submitted_embargo = 'NA'
        submitted_license = 'NA'

    else:
        title = str(parsed_json['items'][0]['title'][0]['title'])
        sherpa_ID = str(parsed_json['items'][0]['id'])
        locations = ["any_website",
                     "insitutional_repository", "named_repository"]

        published_allowed = 0
        published_conditions = 'NA'
        published_embargo = 'NA'
        published_license = 'NA'

        accepted_allowed = 0
        accepted_conditions = 'NA'
        accepted_embargo = 'NA'
        accepted_license = 'NA'

        submitted_allowed = 0
        submitted_conditions = 'NA'
        submitted_embargo = 'NA'
        submitted_license = 'NA'

        publisher_policy = parsed_json['items'][0]['publisher_policy']

        for row in publisher_policy:
            # checks for a fee, if we are under the location and article version is submitted
            for path in row['permitted_oa']:

                if 'additional_oa_fee' in path:
                    if path["additional_oa_fee"] == "no" and any(ele in locations for ele in path['location']['location']) and path['article_version'][0] == 'submitted':
                        submitted_allowed = 1
                        # submitted_conditions.append(path['conditions'])
                        if 'conditions' in path:
                            submitted_conditions = str(path['conditions'])
                        # else:
                        #     submitted_conditions = 'no found conditions'
                        if 'embargo' in path:
                            submitted_embargo = str(path['embargo'])
                        else:
                            submitted_embargo = ('no embargo')
                        if 'license' in path:
                            submitted_license = str(
                                path['license'][0]['license'])
                        else:
                            submitted_license = ('no license available')
            # repeat for each article version
                    if path["additional_oa_fee"] == "no" and any(ele in locations for ele in path['location']['location']) and path['article_version'][0] == 'accepted' and 'additional_oa_fee' in path:
                        accepted_allowed = 1
                        if 'conditions' in path:
                            accepted_conditions = str(path['conditions'])
                        if 'embargo' in path:
                            accepted_embargo = str(path['embargo'])
                        else:
                            accepted_embargo = ('no embargo')
                        if 'license' in path:
                            accepted_license = str(
                                path['license'][0]['license'])
                        else:
                            accepted_license = ('no license available')
                    if path["additional_oa_fee"] == "no" and any(ele in locations for ele in path['location']['location']) and path['article_version'][0] == 'published' and 'additional_oa_fee' in path:
                        published_allowed = 1
                        if 'conditions' in path:
                            published_conditions = str(path['conditions'])
                        if 'embargo' in path:
                            published_embargo = str(path['embargo'])
                        else:
                            published_embargo = ('no embargo')
                        if 'license' in path:
                            published_license = str(
                                path['license'][0]['license'])
                        else:
                            published_license = ('no license available')
            # repeat for each article version

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Monty1010",
            database="journal_publishing_policy"
        )

        mycursor = db.cursor()

        insert_stmt = """INSERT INTO items(title, submitted_allowed, submitted_conditions, submitted_embargo, submitted_license, accepted_allowed, accepted_conditions, accepted_embargo, accepted_license, published_allowed, published_conditions, published_embargo, published_license, sherpa_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"""

        data = (title, submitted_allowed, submitted_conditions, submitted_embargo, submitted_license, accepted_allowed, accepted_conditions,
                accepted_embargo, accepted_license, published_allowed, published_conditions, published_embargo, published_license, sherpa_ID)

        mycursor.execute(insert_stmt, data)
        db.commit()
        print("Data inserted")
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
if db.is_connected():
    db.close()
    print("MySQL connection is closed")
