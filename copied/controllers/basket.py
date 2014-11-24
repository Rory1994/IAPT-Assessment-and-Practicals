# coding: utf8

def index(): 
    grid=SQLFORM.grid(db.line_item)
    return locals()

def basket(): 
    form=crud.select(db.line_item)
    return locals()

def updater():
    db.line_item.id.readable=False
    db.line_item.id.writable=False
    db.line_item.description.readable=False
    db.line_item.description.writable=False

    form = SQLFORM(db.line_item, record = request.args(0))
    if form.process().accepted:
        response.flash = 'Form good!'
    elif form.errors:
        response.flash = 'Form Bad'
        
    return locals()
