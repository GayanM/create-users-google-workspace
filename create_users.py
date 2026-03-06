import csv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

service = build('admin', 'directory_v1', credentials=creds)

#user = {
#    "name": {
#        "givenName": "Darshana",
#        "familyName": "Saman"
#    },
#    "password": "TempPassword123!",
#    "primaryEmail": "saman@oneiam.info"
#}
#service.users().insert(body=user).execute()
#print("User created")

with open("users.csv") as f:
    reader = csv.DictReader(f)

    for row in reader:
        user = {
            "name": {
                "givenName": row["firstname"],
                "familyName": row["lastname"]
            },
            "password": row["password"],
            "primaryEmail": row["email"]
        }

        service.users().insert(body=user).execute()
        print("Created:", row["email"])