# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    features = {'book1':{'id':'1', 'name': 'Batman: Arkham Asylum','publisher': 'DC Comics',
                         'price': '9.00', 'format': 'Paperback', 'writer':'Grant Morrison',
                         'pages':'216', 'description':'Written    by    Grant    Morrison.    Art    and    cover    by    Dave    McKean    In    celebration    of    the ...'},
                'book2':{'id': '2', 'name': 'Superman: Earth One', 'publisher':'DC Comics',
                         'price': '£7.00', 'format':'Paperback', 'writer': 'Mikey',
                         'pages':'136', 'description': 'J.    Michael    Straczynski,    the    creator    of    Babylon    5,    joins    forces    with    rising    star    artist    Shane    Davis    (Superman/Batman:    The Search    for Kryptonite)    to    create    this    original    graphic    novel    that    gives    new    insight    into    Clark    Kents    transformation    into Superman    and    his    first    year    as    The    Man    of    Steel.    This    is    the    first    in    a    new    wave    of    original    DC    Universe    graphic    novels, featuring    top    writers    and    illustrators    unique    takes    on    DC    characters.'
                         }}
   
    response.flash = T("Welcome to web2py!")
    user = None
    if auth.user is not None:
        user = db(db.auth_user.id == auth.user_id).select()
    return dict(features=db(db.products.id == db.features.product_id).select(), user=user)

def search():
    form=FORM('Search:', INPUT(_name='search', requires=IS_NOT_EMPTY()), INPUT(_type='submit'))

    query_result = ""

    if form.accepts(request, session):
         response.flash = 'Search Completed'
         query_result = db(db.products.name.like ('%' +request.vars.search + '%')).select()



    elif form.errors:
        response.flash = 'Please fill in the search box'


    else:
        response.flash = 'Please Enter a Keyword'





    return dict(form=form, features = query_result)

@auth.requires_login(otherwise=URL('login'))
def addproduct():

    form=FORM('New Record:', BR(), BR(), DIV( SPAN(LABEL( 'Name: ', _for='name' ), _class='formLabel'), INPUT(_name='name', requires=IS_NOT_EMPTY()), _class='formField')
              , DIV(SPAN(LABEL( 'Price: ', _for='price' ), _class='formLabel'), INPUT( _name='price', requires=IS_NOT_EMPTY()), _class='formField')
              , DIV(SPAN(LABEL( 'Publisher: ', _for='publisher' ), _class='formLabel'), INPUT( _name='publisher', requires=IS_NOT_EMPTY()), _class='formField')
              , DIV(SPAN(LABEL( 'Type: ', _for='type' ), _class='formLabel')  ,SELECT('Blu-ray','Book',_name="type", requires=IS_NOT_EMPTY()), _class='formField')
              , DIV(SPAN(LABEL( 'Description: ', _for='description' ), _class='formLabel'), TEXTAREA(_name='description', requires=IS_NOT_EMPTY()), _class='formField')
              ,DIV(INPUT(_type='submit'), _class='submitButtonContainer'), _class='addRecordForm')

    if form.accepts(request, session):
       db.products.insert(name=request.vars.name, type=request.vars.type,
                           description=request.vars.description, publisher=request.vars.publisher,
                           price=request.vars.price);
       response.flash = 'Record Entered'

    elif form.errors:
        response.flash = 'Form filled out incorrectly'

    else:
        response.flash = ""




    return dict(form=form);

@auth.requires_login(otherwise=URL('login'))
def updateProduct():

    db.products.description.widget = SQLFORM.widgets.text.widget

    db.products.type.widget = SQLFORM.widgets.options.widget

    db.products.type.requires = [IS_IN_SET(['Book', 'Blu-ray'], zero= None)]

    addform = SQLFORM(db.products)



    if addform.process().accepted:
        response.flash = 'Form Accepted'

    elif addform.errors:
        response.flash = 'Form has errors'

    else:
        response.flash = 'Please Fill Out the Form'

    return dict(form=addform)



def form_processing(form):
    if form.vars.search is None:
        form.errors.search = 'Search Box is empty'

def login():
    return dict()

def register():

    if(len(request.post_vars) is not 0):

        user = db.auth_user.insert(first_name = request.vars.first_name, last_name = request.vars.surname,
                                   password =  db.auth_user.password.validate(request.vars.password)[0], username = request.vars.username)

        auth.login_bare(request.vars.username, request.vars.password)



    return dict()



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth(), bank_details = SQLFORM(db.bank_details))


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
