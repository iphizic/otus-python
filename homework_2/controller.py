from model import ContactDatabase, Contact
from pathlib import Path

def main():
    db = None
    contacts_file = "contacts.json"
    file_path = Path(contacts_file)
    if not file_path.exists():
        db = ContactDatabase.load_from_json("[]")
    else:
        with open(contacts_file, "r") as f:
            db = ContactDatabase.load_from_json(f)

    print(db)