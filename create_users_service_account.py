import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---- CONFIGURATION ----

SERVICE_ACCOUNT_FILE = "workspace-provisioning-489400-08b0d01be679.json"

ADMIN_USER = "gayan@oneiam.info"

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user"
]

CSV_FILE = "users.csv"

# ---- AUTHENTICATION ----

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

delegated_credentials = credentials.with_subject(ADMIN_USER)

service = build(
    "admin",
    "directory_v1",
    credentials=delegated_credentials
)

# ---- CREATE USERS ----

def create_users_from_csv():

    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            user = {
                "name": {
                    "givenName": row["firstname"],
                    "familyName": row["lastname"]
                },
                "password": row["password"],
                "primaryEmail": row["email"]
            }

            try:
                result = service.users().insert(body=user).execute()

                print(f"Created user: {result['primaryEmail']}")

            except Exception as e:
                print(f"Error creating {row['primaryEmail']}:", e)


# ---- MAIN ----

if __name__ == "__main__":
    create_users_from_csv()