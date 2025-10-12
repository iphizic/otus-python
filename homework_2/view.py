import urwid

def file_question(default, callback) -> urwid.Filler:
    ask = urwid.Edit(('I say', u"Please enter file name?\n"), default)
    button = urwid.Button(u'Go')
    #urwid.connect_signal(button, 'click')
    div = urwid.Divider()
    pile = urwid.Pile([ask, div, button])
    top = urwid.Filler(pile, valign='top')
    urwid.connect_signal(button, 'click', callback, user_args=[top.original_widget])
    return top
