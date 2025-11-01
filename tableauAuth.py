import requests

def tableau_pat_signin(tableau_base_url, site_content_url, pat_name, pat_secret):
    api_version = "3.22"
    signin_url = f"{tableau_base_url}/api/{api_version}/auth/signin"

    payload = {
        "credentials": {
            "personalAccessTokenName": pat_name,
            "personalAccessTokenSecret": pat_secret,
            "site": {"contentUrl": site_content_url}
        }
    }

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    resp = requests.post(signin_url, json=payload, headers=headers)
    resp.raise_for_status()

    data = resp.json()
    token = data["credentials"]["token"]
    site_id = data["credentials"]["site"]["id"]
    user_id = data["credentials"]["user"]["id"]
    return token, site_id, user_id