from random import choice

from homework_1.contacts_v1 import contacts_file
from model import ContactDatabase, Contact
from pathlib import Path
from view import *
import urwid

contacts_file = ""

def del_contact(choice, db, loop, button: urwid.Button):
    if choice is not None:
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


def menu(title: str, db, item_chosen, loop, choices=[], find=False) -> urwid.ListBox:
    body = [urwid.Text(title), urwid.Divider()]
    if not find:
        choices = db.contact_id_list()

    for cont_id, contact in db:
        if cont_id in choices:
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

def main_menu(button: urwid.Button, loop, file):
    global contacts_file
    contacts_file = file
    file_path = Path(contacts_file)
    if not file_path.exists():
        db = ContactDatabase.load_from_json("[]")
    else:
        with open(contacts_file, "r") as f:
            db = ContactDatabase.load_from_json(f)

    menu_widget(db, loop, item_chosen, menu)


def add_or_quit(key, loop):
    global contacts_file
    db = ContactDatabase()
    if key in ('q', 'Q'):
        with open(contacts_file, "w") as f:
            db.load_to_json(file=f)
        raise urwid.ExitMainLoop()
    elif key in ('a', 'A'):
        item_chosen(None, db, loop, add_contact, del_contact, "", "", "", None)
    elif key in ('e', 'E'):
        menu_widget(db, loop, item_chosen, menu)
    elif key in ('f', 'F'):
        main = urwid.Padding(find_menu(loop, find_by), left=2, right=2)
        loop.widget = urwid.Overlay(
            main,
            urwid.SolidFill(" "),
            align=urwid.LEFT,
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,
        )

def find_by(field: str, content: urwid.Edit, loop, button: urwid.Button):
    db = ContactDatabase()
    search_res =[]

    if field == "name":
        search_res = db.search_contacts_by_name(content.get_edit_text())
    elif field == "number":
        search_res = db.search_contacts_by_phone(content.get_edit_text())
    elif field == "comment":
        search_res = db.search_contacts_by_comment(content.get_edit_text())

    main_menu_wid = urwid.Padding(menu("Find contacts(press e to exit)", db, item_chosen, loop, choices=search_res, find=True), left=2, right=2)
    loop.widget = urwid.Overlay(
        main_menu_wid,
        urwid.SolidFill(" "),
        align=urwid.LEFT,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )



def main():

    loop = urwid.MainLoop(urwid.Filler(urwid.Text(""), valign='top'))
    loop.widget = file_question("./contacts.json", main_menu, loop)
    loop.unhandled_input = lambda k: add_or_quit(k, loop)

    loop.run()



