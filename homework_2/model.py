import json


class InvalidFileException(Exception):
    def __init__(self):
        super().__init__(f"Файл поврежден.")

class Contact:
    def __init__(self, name, phone, comment):
        self._name = name
        self._comment = comment
        self._phone = phone


    def __repr__(self):
        return f"[name: {self._name}, phone: {self._phone}, comment: \"{self._comment}\"]"


    @property
    def phone(self):
        return self._phone


    @property
    def name(self):
        return self._name


    @property
    def comment(self) -> str:
        return self._comment


    @phone.setter
    def set_phone(self, phone):
        self._phone = phone


    @name.setter
    def set_name(self, name):
        self._name = name


    @comment.setter
    def set_comment(self, comment):
        self._comment = comment


class ContactDatabase:
    instance = None
    _contact_list = {}
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


    def add_contact(self, id: int, name, phone, comment: str) -> None:
        self._contact_list[id] = Contact(name, phone, comment)


    def add_new_contact(self, name, phone, comment: str) -> None:
        id = 0
        id_list = list(self._contact_list)
        while id in id_list:
            id += 1

        self.add_contact(id, name, phone, comment)


    def get_contact_by_id(self, id: int) -> Contact:
        return self._contact_list[id]


    def search_contacts_by_name(self, val) -> list:
        list = []
        for k, v in self._contact_list.items():
            if val in v.name:
                list.append(k)

        return list


    def search_contacts_by_phone(self, val) -> list:
        list = []
        for k, v in self._contact_list.items():
            if val in v.phone:
                list.append(k)

        return list


    def search_contacts_by_comment(self, val) -> list:
        list = []
        for k, v in self._contact_list.items():
            if val in v.comment:
                list.append(k)

        return list

    def contact_id_list(self):
        return list(self._contact_list)

    def delete_contact(self, id):
        del self._contact_list[id]


    def clean(self):
        self._contact_list = {}


    def load_to_json(self, file) -> None:
        db_map=[]
        for k, v in self._contact_list.items():
            db_map.append({"id": k, "name": v.name, "number": v.phone, "comment": v.comment})

        return json.dump(db_map, file, indent=4, ensure_ascii=False)


    @classmethod
    def load_from_json(cls, json_text):
        try:
            data = json.load(json_text)
        except Exception:
            raise InvalidFileException
        db = cls()
        db.clean()
        for i in data:
            db.add_contact(i["id"], i["name"], i["number"], i["comment"])

        return db
