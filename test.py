import pandas as pd
# needs to read list of CSV titles and then get the following info from each JSON
journals = pd.read_csv("TTU_Journals_2022.csv")
firstTen = journals[['Title']].head(10).values.tolist()
requestTitle = ''

for value in firstTen:
    requestTitle = str(value)
    requestTitle = requestTitle.replace(" ", "%20")
    requestTitle = requestTitle.replace("'", "")
    requestTitle = requestTitle.replace("[", "")
    requestTitle = requestTitle.replace("]", "")
    requestURL = ('https://v2.sherpa.ac.uk/cgi/retrieve?item-type=publication&format=Json&limit=1&offset=0&filter=%5B%5B%22title%22%2C%22equals%22%2C%22' +
                  requestTitle + '%22%5D%5D&api-key=4FB4B054-3ACC-11EE-AB97-40C413E8924B')
    print(requestTitle)
    # print(requestURL)
