from __future__ import annotations
from pathlib import Path
import json
import typing
import urwid


if typing.TYPE_CHECKING:
    from collections.abc import Iterable

choices = []
contacts = []
contacts_file = "contacts.json"

palette = [('I say', 'default,bold', 'default', 'bold'),]
ask = urwid.Edit(('I say', u"Please enter file name?\n"), contacts_file)
button = urwid.Button(u'Go')
div = urwid.Divider()
pile = urwid.Pile([ask, div, button])
top = urwid.Filler(pile, valign='top')

def on_ask_change(edit, new_edit_text):
    global contacts_file
    contacts_file = str(new_edit_text)


def menu(title: str, list) -> urwid.ListBox:
    body = [urwid.Text(title), urwid.Divider()]

    for c in list:
        button = urwid.Button(c["name"])
        urwid.connect_signal(button, "click", item_chosen, c["id"])
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))


    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def item_chosen(button: urwid.Button, choice) -> None:
    palette = [('I say', 'default,bold', 'default', 'bold'), ]

    contact_name = urwid.Edit(('I say', u"Please enter contact name?\n"))
    contact_number = urwid.Edit(('I say', u"Please enter contact number?\n"))
    contact_comment = urwid.Edit(('I say', u"Please enter contact comment?\n"))
    button_add = urwid.Button(u'Add')
    button_delete = urwid.Button(u'Delete')

    for i in contacts:
        if i["id"] == choice:
            contact_name.set_edit_text(i["name"])
            contact_number.set_edit_text(i["number"])
            contact_comment.set_edit_text(i["comment"])
            break

    pile = urwid.Pile([contact_name,
                       div,
                       contact_number,
                       div,
                       contact_comment,
                       div,
                       button_add,
                       button_delete])
    urwid.connect_signal(button_add, 'click', add_contact, user_args=[contact_name,
                                                                      contact_number,
                                                                      contact_comment,
                                                                      choice])
    urwid.connect_signal(button_delete, 'click', del_contact, user_args=[choice])
    top.original_widget = urwid.Filler(pile, valign='top')


def del_contact(choice, button: urwid.Button):
    for i in contacts:
        if i["id"] == choice:
            contacts.remove(i)
            break

    main = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", contacts), left=2, right=2)
    top.original_widget = urwid.Overlay(
        main,
        urwid.SolidFill(" "),
        align=urwid.LEFT,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )


def none_fiction(button: urwid.Button) -> None:
    global choices
    global contacts
    file_path = Path(contacts_file)
    if not file_path.exists():
        with open(contacts_file, "w") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
        choices = []
    else:
        with open(contacts_file, "r") as f:
            contacts = json.load(f)
            choices = [i["name"] for i in contacts]

    main = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", contacts), left=2, right=2)
    top.original_widget = urwid.Overlay(
        main,
        urwid.SolidFill(" "),
        align=urwid.LEFT,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )

def add_or_quit(key):
    if key in ('q', 'Q'):
        with open(contacts_file, "w") as f:
            json.dump(contacts, f, indent=4, ensure_ascii=False)
        raise urwid.ExitMainLoop()
    elif key in ('a', 'A'):
        top.original_widget = add_contact_form()

    elif key in ('e', 'E'):
        main = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", contacts), left=2, right=2)
        top.original_widget = urwid.Overlay(
            main,
            urwid.SolidFill(" "),
            align=urwid.LEFT,
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,
        )

    elif key in ('f', 'F'):
        main = urwid.Padding(find_menu(), left=2, right=2)
        top.original_widget = urwid.Overlay(
            main,
            urwid.SolidFill(" "),
            align=urwid.LEFT,
            width=(urwid.RELATIVE, 60),
            valign=urwid.MIDDLE,
            height=(urwid.RELATIVE, 60),
            min_width=20,
            min_height=9,
        )

def find_menu():
    body = [urwid.Text(u"Find by"), urwid.Divider()]
    items = ["name", "number", "comment"]
    for c in items:
        button = urwid.Button(c)
        urwid.connect_signal(button, "click", find_by_menu, c)
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def find_by_menu(button: urwid.Button, field: str):
    find_item = urwid.Edit(f"Enter field {field} content\n")
    button_search = urwid.Button(u"Search")
    form = urwid.Pile([find_item,
                       div,
                       button_search])
    urwid.connect_signal(button_search, 'click', find_by, user_args=[field, find_item])
    top.original_widget = urwid.Filler(form, valign='top')


def find_by(field: str, content: urwid.Edit, button: urwid.Button):
    finds = []
    text = content.get_edit_text()
    for i in contacts:
        if text in i[field]:
            finds.append(i)

    main = urwid.Padding(menu("Find contacts(press e to exit)", finds), left=2, right=2)
    top.original_widget = urwid.Overlay(
        main,
        urwid.SolidFill(" "),
        align=urwid.LEFT,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )


def add_contact_form() -> urwid.Widget:
    palette = [('I say', 'default,bold', 'default', 'bold'), ]
    contact_name = urwid.Edit(('I say', u"Please enter contact name?\n"))
    contact_number = urwid.Edit(('I say', u"Please enter contact number?\n"))
    contact_comment = urwid.Edit(('I say', u"Please enter contact comment?\n"))
    button_add = urwid.Button(u'Add')
    pile = urwid.Pile([contact_name,
                       div,
                       contact_number,
                       div,
                       contact_comment,
                       div,
                       button_add])
    urwid.connect_signal(button_add, 'click', add_contact, user_args=[contact_name,
                                                                      contact_number,
                                                                      contact_comment,
                                                                      None])

    return urwid.Filler(pile, valign='top')

def add_contact(name, number, comment: urwid.Edit, id, button: urwid.Button):
    if id is None:
        id = 0
        id_list = [c["id"] for c in contacts]
        while id in id_list:
            id+=1

        contacts.append({ "id": id,
                          "name": name.get_edit_text(),
                          "number": number.get_edit_text(),
                          "comment": comment.get_edit_text()})
    else:
        for c, i in enumerate(contacts):
            if i["id"] == id:
                contacts[c] = { "id": id,
                                "name": name.get_edit_text(),
                                "number": number.get_edit_text(),
                                "comment": comment.get_edit_text()}
                break

    global choices
    choices = [i["name"] for i in contacts]

    main = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", contacts), left=2, right=2)
    top.original_widget = urwid.Overlay(
        main,
        urwid.SolidFill(" "),
        align=urwid.LEFT,
        width=(urwid.RELATIVE, 60),
        valign=urwid.MIDDLE,
        height=(urwid.RELATIVE, 60),
        min_width=20,
        min_height=9,
    )


if __name__=="__main__":


    urwid.connect_signal(ask, 'change', on_ask_change)
    urwid.connect_signal(button, 'click', none_fiction)

    loop = urwid.MainLoop(top, palette, unhandled_input=add_or_quit).run()
