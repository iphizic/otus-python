from model import ContactDatabase, Contact
from pathlib import Path
from view import *
import urwid

def item_chosen(contact: Contact, loop, button):
    palette = [('I say', 'default,bold', 'default', 'bold'), ]
    div = urwid.Divider()

    contact_name = urwid.Edit(('I say', u"Please enter contact name?\n"))
    contact_number = urwid.Edit(('I say', u"Please enter contact number?\n"))
    contact_comment = urwid.Edit(('I say', u"Please enter contact comment?\n"))
    button_add = urwid.Button(u'Add')
    button_delete = urwid.Button(u'Delete')

    contact_name.set_edit_text(contact.name)
    contact_number.set_edit_text(contact.phone)
    contact_comment.set_edit_text(contact.comment)

    pile = urwid.Pile([contact_name,
                       div,
                       contact_number,
                       div,
                       contact_comment,
                       div,
                       button_add,
                       button_delete])
    urwid.connect_signal(button_add, 'click', add_contact, user_args=[contact, loop])
    urwid.connect_signal(button_delete, 'click', del_contact, user_args=[contact, loop])
    loop.widget = urwid.Filler(pile, valign='top')

def del_contact(choice, button: urwid.Button):
  pass


def add_contact(contact, button):
    pass


def menu(title: str, db, item_chosen, loop) -> urwid.ListBox:
    body = [urwid.Text(title), urwid.Divider()]

    for contact in db:
        button = urwid.Button(contact.name)
        urwid.connect_signal(button, "click", item_chosen, user_args=[contact, loop])
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def main_menu(button: urwid.Button, loop, contacts_file):

    file_path = Path(contacts_file)
    if not file_path.exists():
        db = ContactDatabase.load_from_json("[]")
    else:
        with open(contacts_file, "r") as f:
            db = ContactDatabase.load_from_json(f)

    form = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", db, item_chosen, loop), left=2, right=2)
    loop.widget = urwid.Overlay(
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
    loop = urwid.MainLoop(urwid.Filler(urwid.Text("")))
    loop.widget = file_question("./contacts.json", main_menu, loop)

    loop.run()



