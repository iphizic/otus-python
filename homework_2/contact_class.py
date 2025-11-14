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

