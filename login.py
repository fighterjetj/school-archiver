import requests, json


def getLoginSession(username, password):
    s = requests.Session()
    payload = {"j_username": username, "j_password": password}
    loginURL = getLoginURL()
    print(loginURL)
    res = s.post(
        getLoginURL(),
        payload,
    )
    # print(res.content)
    """
    with open("error.html", "wb") as f:
        f.write(res.content)
    """
    return s


BRUINLEARN_URL = "https://bruinlearn.ucla.edu/login/saml"


def getLoginURL():
    r1 = requests.get(BRUINLEARN_URL)
    """
    r.history[0].url
    r.history[1].url
    [res.url for res in r.history]
    """
    r2 = requests.get(r1.history[1].url)
    [res.url for res in r2.history]
    r2.url
    # return r.url
    """
    with open("login.html", "wb") as f:
        f.write(r.content)
    """


getLoginURL()
session = getLoginSession("", "")
