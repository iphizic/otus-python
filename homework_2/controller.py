from model import ContactDatabase, Contact
from pathlib import Path
from view import *
import urwid

def item_chosen(c: Contact):
    pass


def menu(title: str, db, item_chosen) -> urwid.ListBox:
    body = [urwid.Text(title), urwid.Divider()]

    for c in db:
        button = urwid.Button(c.name)
        urwid.connect_signal(button, "click", item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def none_fiction(button: urwid.Button, top):
    contacts_file = "contacts.json"
    file_path = Path(contacts_file)
    if not file_path.exists():
        db = ContactDatabase.load_from_json("[]")
    else:
        with open(contacts_file, "r") as f:
            db = ContactDatabase.load_from_json(f)

    form = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", db, item_chosen), left=2, right=2)
    top = urwid.Overlay(
        form,
        urwid.SolidFill(" "),
        align=urwid.LEFT,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )

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

    urwid.MainLoop(file_question("./contacts.py", none_fiction)).run()

