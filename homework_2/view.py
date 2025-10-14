import urwid

def file_question(default, callback, loop) -> urwid.Filler:
    ask = urwid.Edit( u"Please enter file name?\n", default)
    button = urwid.Button(u'Go')
    #urwid.connect_signal(button, 'click')
    div = urwid.Divider()
    pile = urwid.Pile([ask, div, button])
    top = urwid.Filler(pile, valign='top')
    urwid.connect_signal(button, 'click', lambda b=button: callback(button, loop, ask.get_edit_text()))
    return top
