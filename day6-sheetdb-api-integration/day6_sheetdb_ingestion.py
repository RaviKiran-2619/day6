import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read SheetDB API URL
SHEETDB_API_URL = os.getenv("SHEETDB_API_URL")


def append_candidate_record(name, email, role, status="Verified"):
    print(f"\n[SheetDB Ingestion] Preparing row payload for: {name}")

    # Prepare JSON payload
    payload = {
        "data": [
            {
                "Name": name,
                "Email": email,
                "Role": role,
                "Status": status
            }
        ]
    }

    # Request headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        # Send POST request to SheetDB
        response = requests.post(
            SHEETDB_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(
            f"[SheetDB Ingestion] HTTP Status Code: "
            f"{response.status_code}"
        )

        # Check successful creation
        if response.status_code == 201:
            print(
                "[SheetDB Ingestion] "
                "Record appended successfully!"
            )
            return response.json()

        else:
            print(
                f"[SheetDB Failure] Error payload: "
                f"{response.text}"
            )
            return None

    except Exception as e:
        print(
            f"[SheetDB Exception] "
            f"Network/API Error: {e}"
        )
        return None


if __name__ == "__main__":

    # Get candidate details from user
    name = input("Enter candidate name: ")
    email = input("Enter candidate email: ")
    role = input("Enter candidate role: ")
    status = input("Enter candidate status: ")

    # Use default status if user leaves it empty
    if not status:
        status = "Verified"

    # Append candidate record to Google Sheet
    append_candidate_record(
        name=name,
        email=email,
        role=role,
        status=status
    )