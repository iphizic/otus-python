import json
from contact_class import Contact
from exceptions import InvalidFileException


class ContactDatabase:
    instance = None
    _contact_list = {}
    contacts_file_name = ""
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(ContactDatabase, cls).__new__(cls)
        return cls.instance


    def __str__(self):
        return str(self._contact_list)


    def __iter__(self):
        self.index = 0
        self._ids = list(self._contact_list)
        return self


    def __next__(self):
        if self.index < len(self._ids):
            contact_id = self._ids[self.index]
            x = self._contact_list[contact_id]
            self.index += 1
            return contact_id, x
        raise StopIteration


    def _add_contact(self, id: int, name, phone, comment: str) -> None:
        self._contact_list[id] = Contact(name, phone, comment)


    def add_new_contact(self, name, phone, comment: str) -> None:
        """Add new contact to db"""
        id = 0
        id_list = list(self._contact_list)
        while id in id_list:
            id += 1

        self._add_contact(id, name, phone, comment)


    def get_contact_by_id(self, id: int) -> Contact:
        """Return contact object from db by id"""
        return self._contact_list[id]


    def search_contacts_by_name(self, val) -> list:
        """Return list contacts id with name search substring"""
        list = []
        for k, v in self._contact_list.items():
            if val in v.name:
                list.append(k)

        return list


    def search_contacts_by_phone(self, val) -> list:
        """Return list contacts id with phone search substring"""
        list = []
        for k, v in self._contact_list.items():
            if val in v.phone:
                list.append(k)

        return list


    def search_contacts_by_comment(self, val) -> list:
        """Return list contacts id with comment search substring"""
        list = []
        for k, v in self._contact_list.items():
            if val in v.comment:
                list.append(k)

        return list

    def contact_id_list(self):
        """Return full contacts id list"""
        return list(self._contact_list)

    def delete_contact(self, id):
        """Delete contact by id"""
        del self._contact_list[id]


    def _clean(self):
        self._contact_list = {}


    def load_to_json(self, file) -> None:
        """Load db to file"""
        db_map=[]
        for k, v in self._contact_list.items():
            db_map.append({"id": k, "name": v.name, "number": v.phone, "comment": v.comment})

        return json.dump(db_map, file, indent=4, ensure_ascii=False)


    @classmethod
    def load_from_json(cls, json_text):
        """Load db from file or string"""
        try:
            data = json.load(json_text)
        except Exception:
            raise InvalidFileException
        db = cls()
        db._clean()
        for i in data:
            db._add_contact(i["id"], i["name"], i["number"], i["comment"])

        return db
