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
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def login():

    form = FORM(LEGEND('Login'), INPUT(_type='text', _name='username', _class = 'input-block-level', _placeholder='username', requires=IS_NOT_EMPTY()),
                 INPUT(_type='password',_name='password', _class = 'input-block-level', _placeholder='password', requires=IS_NOT_EMPTY()), INPUT(_type='submit', _class='btn btn-primary', _value='Login'),
                 A('Register',_href="{{=URL('default','register')}}", _role='button', _class='btn btn-info'))
    if form.process(onvalidation=login_validation).accepted:
        response.flash = 'form accepted'
        user = auth.login_bare(request.vars.username, request.vars.password)
        if(user is False):
            response.flash = DIV("Invalid Username/Password Combination", _class='alert alert-error')
        else:
            redirect(URL('index'))

    return dict(form=form)

def login_validation(form):
    if form.vars.username =="cat":
        form.errors.username= "Hello Cat"
    if form.vars.password == None:
        form.errors.password = "Password can not be empty"

def register():

    form= FORM(FIELDSET(

                        LEGEND('Personal Information'),
                        DIV(LABEL('First Name:', _for='first_name'),INPUT(_id='first_name', _name='first_name', _type='text', _class='span4'),
                            LABEL('Last Name:', _for='last_name'),INPUT(_id='last_name', _name='last_name', _type='text', _class='span4'),
                            LABEL('Date of Birth:', _for='date_of_birth'),INPUT(_id='date_of_birth', _name='date_of_birth', _type='text', _class='span4')
                            ,_class='controls control-group'),

                        LEGEND('Login Credentials'),
                        DIV(LABEL('Username:', _for='username'),INPUT(_id='username', _name='username', _type='text', _class='span4'),
                            LABEL('Password:', _for='password'),INPUT(_id='password', _name='password', _type='password', _class='span4'),
                            LABEL('Confirm Password:', _for='confirm_password'),INPUT(_id='confirm_password', _name='confirm_password', _type='password', _class='span4')
                            ,_class='controls control-group'),

                        LEGEND('Home Address'),
                        DIV(LABEL('Street:', _for='street'),INPUT(_id='street', _name='street', _type='text', _class='span4'),
                            LABEL('City:', _for='city'),INPUT(_id='city', _name='city', _type='text', _class='span4'),
                            LABEL('Postcode:', _for='postcode'),INPUT(_id='postcode', _name='postcode', _type='text', _class='span4'),
                            LABEL('Country:', _for='country'),INPUT(_id='country', _name='country', _type='text', _class='span4')
                            ,_class='controls control-group'),

                        LEGEND('Billing Address'),
                        DIV(LABEL('Card Number:', _for='card_number'),INPUT(_id='card_number', _name='card_number', _type='text', _class='span4'),
                            LABEL('Expiry Date:', _for='expiry_date'),INPUT(_id='expiry_date', _name='expiry_date', _type='text', _class='span4'),
                            LABEL('Security Code:', _for='security_code'),INPUT(_id='security_code', _name='security_code', _type='text', _class='span4')
                            ,_class='controls control-group'),

                        LEGEND('Billing Address'),
                        DIV(LABEL(INPUT(_id='billing_checkbox', _name='billing_checkbox', _value='yes', _onclick='javascript:toggleAddressAvailibility();', _type='checkbox' ), 'Same as Home Address',_class='checkbox'),
                            LABEL('Street:', _for='billing_street'),INPUT(_id='billing_street', _name='billing_street', _type='text', _class='span4'),
                            LABEL('City:', _for='billing_city'),INPUT(_id='billing_city', _name='billing_city', _type='text', _class='span4'),
                            LABEL('Postcode:', _for='billing_postcode'),INPUT(_id='billing_postcode', _name='billing_postcode', _type='text', _class='span4'),
                            LABEL('Country:', _for='billing_country'),INPUT(_id='billing_country', _name='billing_country', _type='text', _class='span4')
                            ,_class='controls control-group')






    ))

    return dict(form=form)



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
    return dict(form=auth())


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
