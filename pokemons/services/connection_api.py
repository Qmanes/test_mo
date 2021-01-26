import requests
def api_get(url):

    try:

        return requests.get(url).json()

    except:

        raise Exception("Error connecting with api")