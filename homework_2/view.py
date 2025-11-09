import urwid


def item_chosen(contact, db, loop, add_callback, del_callback, name, phone, comment, button):
    palette = [('I say', 'default,bold', 'default', 'bold'), ]
    div = urwid.Divider()

    contact_name = urwid.Edit(('I say', u"Please enter contact name?\n"))
    contact_number = urwid.Edit(('I say', u"Please enter contact number?\n"))
    contact_comment = urwid.Edit(('I say', u"Please enter contact comment?\n"))
    button_add = urwid.Button(u'Add')
    button_delete = urwid.Button(u'Delete')

    contact_name.set_edit_text(name)
    contact_number.set_edit_text(phone)
    contact_comment.set_edit_text(comment)

    pile = urwid.Pile([contact_name,
                       div,
                       contact_number,
                       div,
                       contact_comment,
                       div,
                       button_add,
                       button_delete])
    urwid.connect_signal(button_add, 'click', add_callback, user_args=[contact_name,
                                                                      contact_number,
                                                                      contact_comment,
                                                                      contact,
                                                                      db,
                                                                      loop])
    urwid.connect_signal(button_delete, 'click', del_callback, user_args=[contact, db, loop])
    loop.widget = urwid.Filler(pile, valign='top')


def menu_widget(db, loop, callback, menu):
    form = urwid.Padding(menu("Contacts (press a to add, q to quit, f to search)", db, callback, loop), left=2,
                         right=2)
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

def file_question(default, callback, loop) -> urwid.Filler:
    ask = urwid.Edit( u"Please enter file name?\n", default)
    button = urwid.Button(u'Go')
    div = urwid.Divider()
    pile = urwid.Pile([ask, div, button])
    top = urwid.Filler(pile, valign='top')
    urwid.connect_signal(button, 'click', lambda b=button: callback(button, loop, ask.get_edit_text()))
    return top

def add_contact_form(callback) -> urwid.Widget:
    palette = [('I say', 'default,bold', 'default', 'bold'), ]
    contact_name = urwid.Edit(('I say', u"Please enter contact name?\n"))
    contact_number = urwid.Edit(('I say', u"Please enter contact number?\n"))
    contact_comment = urwid.Edit(('I say', u"Please enter contact comment?\n"))
    button_add = urwid.Button(u'Add')
    div = urwid.Divider()
    pile = urwid.Pile([contact_name,
                       div,
                       contact_number,
                       div,
                       contact_comment,
                       div,
                       button_add])
    urwid.connect_signal(button_add, 'click', callback, user_args=[contact_name,
                                                                      contact_number,
                                                                      contact_comment,
                                                                      None])

    return urwid.Filler(pile, valign='top')

def find_menu(loop, find):
    body = [urwid.Text(u"Find by"), urwid.Divider()]
    items = ["name", "number", "comment"]
    for c in items:
        button = urwid.Button(c)
        urwid.connect_signal(button, "click", find_by_menu, user_args=[c, loop, find])
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def find_by_menu(field: str, loop, find, button: urwid.Button):
    find_item = urwid.Edit(f"Enter field {field} content\n")
    div = urwid.Divider()
    button_search = urwid.Button(u"Search")
    form = urwid.Pile([find_item,
                       div,
                       button_search])
    urwid.connect_signal(button_search, 'click', find, user_args=[field, find_item, loop])
    loop.widget = urwid.Filler(form, valign='top')



