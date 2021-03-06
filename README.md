# binance-exchange-api
Binance Exchange API Utility Project

Read account information from binance.com exchange API

### API ###
https://binance-docs.github.io/apidocs/

##### Requirements #####
- https://www.python.org/downloads/

1. python3 installed:
   
   `python3 -v`
   
2. pip installed:
   
   `python3 -m pip --version`

3. python Virtual Environment installed
    - Ubuntu/Debian
        - sudo apt-get update
        - sudo apt-get install python-virtualenv
        - sudo pip install virtualenv
    - Mac / Windows
        - should be installed with python and pip 
##### Setup #####
Enter project root directory:
1. Edit the `.env` file your API Key and Secret
    ```
    API_KEY=changeme
    API_SECRET=changeme
    ```
- Follow this link to generate the API Key
    - https://exchange-docs.crypto.com/spot/index.html#generating-the-api-key

2. Create a Python Virtual Environment:
   
   `python3 -m venv env`
   
3. Activate the Virtual Environment:
   
   `source ./env/bin/activate`
   
    - your console should change adding `(env)` as prefix
    - To exit type refer to 'Deactivate the Virtual Environment'
   
4. Install dependencies:
   
   `pip3 install -r requirements.txt`
   
    Ignore warning messages.

5. Deactivate the Virtual Environment:
   
   `deactivate`
   - the `(env)` prefix should be removed from the console

##### Run #####
Enter project root directory:
1. Activate the Virtual Environment:

    `source ./env/bin/activate`

1. Run the script:

   `python3 app_cdc_account.py`

3. You should see something like:
   ```
   Reading account from API url 'https://api.crypto.com/v2/private/get-account-summary' at 'YYYY-MM-DD HH:MM:SS'
   API Response '200' - 'OK'
   
   The balance for currency 'CRO' is 1.00000000, the balance for pair 'CRO_USDT' in USDT is: 0.21000000
   The total balance for the account is 0.21000000 USDT
   ```