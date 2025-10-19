from model import ContactDatabase, Contact
from pathlib import Path
from view import *
import urwid

def del_contact(choice, db, loop, button: urwid.Button):
    db.delete_contact(choice)
    menu_widget(db, loop, item_chosen, menu)


def add_contact(name: urwid.Edit,
                number: urwid.Edit,
                comment: urwid.Edit,
                contact,
                db: ContactDatabase,
                loop,
                button: urwid.Button):
    if contact is None:
        db.add_new_contact(name.get_edit_text(), number.get_edit_text(),comment.get_edit_text())
    else:
        db.get_contact_by_id(contact).name = name.get_edit_text()
        db.get_contact_by_id(contact).phone = number.get_edit_text()
        db.get_contact_by_id(contact).comment = comment.get_edit_text()

    menu_widget(db, loop, item_chosen, menu)


def menu(title: str, db, item_chosen, loop) -> urwid.ListBox:
    body = [urwid.Text(title), urwid.Divider()]

    for cont_id, contact in db:
        button = urwid.Button(contact.name)
        urwid.connect_signal(button, "click", item_chosen, user_args=[cont_id,
                                                                      db,
                                                                      loop,
                                                                      add_contact,
                                                                      del_contact,
                                                                      contact.name,
                                                                      contact.phone,
                                                                      contact.comment
                                                                      ])
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def main_menu(button: urwid.Button, loop, contacts_file):

    file_path = Path(contacts_file)
    if not file_path.exists():
        db = ContactDatabase.load_from_json("[]")
    else:
        with open(contacts_file, "r") as f:
            db = ContactDatabase.load_from_json(f)

    menu_widget(db, loop, item_chosen, menu)


def add_or_quit(key):
    if key in ('q', 'Q'):
        with open(contacts_file, "w") as f:
            json.dump(contacts, f, indent=4, ensure_ascii=False)
        raise urwid.ExitMainLoop()


def main():
    # db = None
    #
    #
    # contacts_file = "contacts.json"
    # file_path = Path(contacts_file)
    # if not file_path.exists():
    #     db = ContactDatabase.load_from_json("[]")
    # else:
    #     with open(contacts_file, "r") as f:
    #         db = ContactDatabase.load_from_json(f)
    loop = urwid.MainLoop(urwid.Filler(urwid.Text(""), valign='top'))
    loop.widget = file_question("./contacts.json", main_menu, loop)

    loop.run()



