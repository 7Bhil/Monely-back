import requests
import json

BASE_URL = 'http://localhost:8000/api'
EMAIL = 'user_verify_2@example.com'
PASSWORD = 'StrongPass123!'

def run():
    # 1. Login
    login_resp = requests.post(f'{BASE_URL}/auth/login/', json={
        'email': EMAIL,
        'password': PASSWORD
    })
    
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.status_code} {login_resp.text}")
        # Try to register if login fails (maybe db was flushed?)
        print("Trying to register...")
        reg_resp = requests.post(f'{BASE_URL}/auth/register/', json={
            'email': EMAIL,
            'password': PASSWORD,
            'name': 'Verify User',
            'username': 'verifyuser2',
            'password_confirm': PASSWORD
        })
        print(f"Register response: {reg_resp.status_code}")
        # Login again
        login_resp = requests.post(f'{BASE_URL}/auth/login/', json={
            'email': EMAIL,
            'password': PASSWORD
        })

    token = login_resp.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    # 2. Try to create wallet with frontend payload
    payload = {
        "name": "Compte Courant",
        "balance": 5000,
        "type": "checking",
        "currency": "XOF",
        "color": "blue",
        "icon": "account_balance"
    }
    
    print(f"Sending payload: {json.dumps(payload, indent=2)}")
    
    try:
        resp = requests.post(f'{BASE_URL}/wallets/wallets/', json=payload, headers=headers)
        print(f"Response Status: {resp.status_code}")
        print(f"Response Body: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
