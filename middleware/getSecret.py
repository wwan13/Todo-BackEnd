import json

def getSecret():
    
    with open("secret.json","r") as jsonFile:
        jsonData = json.load(jsonFile)

    secretKey = jsonData["secret-key"]

    return secretKey


def getDatabasePW():
    with open("secret.json","r") as jsonFile:
        jsonData = json.load(jsonFile)

    PW = jsonData["mysql-password"]

    return PW