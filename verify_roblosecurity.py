import requests

def verify_cookie(cookie: str) -> bool:
    request = requests.get('https://users.roblox.com/v1/users/authenticated', cookies={ '.ROBLOSECURITY': cookie })

    if request.status_code == 200:
        return True

    return False