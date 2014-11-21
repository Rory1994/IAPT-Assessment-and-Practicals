# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################


COUNTRIES=('United States', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Ivory Coast', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea','South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'FYROM', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe')



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


    form = FORM(LEGEND('Login'), INPUT(_type='text', _name='username', _class = 'input-block-level', _placeholder='username', requires=IS_NOT_EMPTY( error_message=T("Please enter a username"))),
                 INPUT(_type='password',_name='password', _class = 'input-block-level', _placeholder='password', requires=IS_NOT_EMPTY(error_message=T("Please enter a password"))), INPUT(_type='submit', _class='btn btn-primary', _value='Login'),
                 A('Register',_href=URL('register'), _role='button', _class='btn btn-info'))
    if form.process(onvalidation=login_validation).accepted:
        response.flash = 'form accepted'
        user = auth.login_bare(request.vars.username, request.vars.password)
        if(user is False):
            response.flash = DIV("Invalid Username/Password Combination", _class='alert alert-error')
        else:
            redirect(URL('index'))
    elif form.errors:
        response.flash = DIV("Username or Password field is empty", _class='alert alert-error')




    return dict(form=form)

def login_validation(form):
    if form.vars.username =="cat":
        form.errors.username= "Hello Cat"
    if form.vars.password == None:
        form.errors.password = "Password can not be empty"


def register():

    form= FORM(FIELDSET(

                        LEGEND('Personal Information'),
                        DIV(LABEL('First Name:', _for='first_name'),INPUT(_id='first_name', _name='first_name', _type='text', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('Last Name:', _for='last_name'),INPUT(_id='last_name', _name='last_name', _type='text', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                            ,_class='controls control-group'),


                        DIV( LABEL('Date of Birth:'),
                             INPUT( _name='dob', _type='date', _class='span4', _placeholder='yyyy',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                             ,_class="controls controls-row"),

                        LEGEND('Login Credentials'),
                        DIV(LABEL('Username:', _for='username'),INPUT(_id='username', _name='username', _type='text', _class='span4',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_NOT_IN_DB(db, 'auth_user.username', error_message='Username already taken')]),
                            LABEL('Password:', _for='password'),INPUT(_id='password', _name='password', _type='password', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('Confirm Password:', _for='confirm_password'),INPUT(_id='confirm_password', _name='confirm_password', _type='password', _class='span4'
                            , requires=[IS_EQUAL_TO(request.vars.password, error_message=T("Passwords do not match")), IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))])
                            ,_class='controls control-group'),

                        LEGEND('Home Address'),
                        DIV(LABEL('Street:', _for='street'),INPUT(_id='street', _name='street', _type='text', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('City:', _for='city'),INPUT(_id='city', _name='city', _type='text', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('Postcode:', _for='postcode'),INPUT(_id='postcode', _name='postcode', _type='text', _class='span4',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")),
                            IS_MATCH('^[A-Z0-9]{4} [A-Z0-9]{3}$', error_message="Postcode is not valid" )]),
                            LABEL('Country:', _for='country'),INPUT(_id='country', _name='country', _type='text', _class='span4',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_IN_SET(COUNTRIES)])
                            ,_class='controls control-group'),

                        LEGEND('Billing Information'),
                        DIV(LABEL('Card Number:', _for='card_number'),INPUT(_id='card_number', _name='card_number', _type='text', _class='span4', requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")),
                            IS_LENGTH(minsize=12, maxsize=12, error_message="Card number must be 12 digits long"), IS_MATCH('^[0-9]{12,12}$', error_message="Card number must be 12 digits long" )]),
                            LABEL('Expiry Date:', _for='expiry_date'),INPUT(_id='expiry_date', _name='expiry_date', _type='text', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('Security Code:', _for='security_code'),INPUT(_id='security_code', _name='security_code', _type='text', _class='span4',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")),
                            IS_LENGTH(minsize=3, maxsize=3, error_message="Security code contain 3 numbers"), IS_MATCH('^[0-9]{3}$', error_message='Security code must contain 3 numbers')])
                            ,_class='controls control-group'),

                        LEGEND('Billing Address'),
                        DIV(LABEL(INPUT(_id='billing_checkbox', _name='billing_checkbox', _value='yes', _onclick='javascript:toggleAddressAvailibility();', _type='checkbox' ), 'Same as Home Address',_class='checkbox'),
                            DIV(LABEL('Street:', _for='billing_street'),INPUT( _name='billing_street', _type='text', _class='span4'), _id='billing_street'),
                            DIV(LABEL('City:', _for='billing_city'),INPUT( _name='billing_city', _type='text', _class='span4'), _id='billing_city'),
                            DIV(LABEL('Postcode:', _for='billing_postcode'),INPUT( _name='billing_postcode', _type='text', _class='span4'), _id='billing_postcode'),
                            DIV(LABEL('Country:', _for='billing_country' ),INPUT( _name='billing_country', _type='text', _class='span4'), _id='billing_country')
                            ,_class='controls control-group last_form_section'),

                         INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Register')


    ))





    if form.process().accepted:



        addressAlreadyInDBQuery = db((db.address.street ==request.vars.street) and (db.address.city == request.vars.city)
                                         and (db.address.country == request.vars.country) and
                                        (db.address.postcode == request.vars.postcode)).select()

        if(len(addressAlreadyInDBQuery) >0):
            address = addressAlreadyInDBQuery[0].id
        else:
            address = db.address.insert(street = request.vars.street, city = request.vars.city, country = request.vars.country,
                        postcode = request.vars.postcode)

        bankDetailsAlreadyInDBQuery = db(db.bank_details.card_number == request.vars.card_number).select()


        if(len( bankDetailsAlreadyInDBQuery) >0):
            bank_details = bankDetailsAlreadyInDBQuery[0].id

        else:

            if(request.vars.billing_checkbox == 'yes'):
                bank_details = db.bank_details.insert(card_number = request.vars.card_number, security_code = request.vars.security_code,
                                              address_id = address, expiry_date = request.vars.expiry_date)

            else:
                billingAddressAlreadyInDBQuery = db((db.address.street ==request.vars.billing_street) and (db.address.city == request.vars.billing_city)
                                             and (db.address.country == request.vars.billing_country) and
                                            (db.address.postcode == request.vars.billing_postcode)).select()

                if(len(billingAddressAlreadyInDBQuery) >0):
                    bank_address = billingAddressAlreadyInDBQuery[0].id
                else:
                    bank_address = db.address.insert(street = request.vars.billing_street, city = request.vars.billing_city, country = request.vars.billing_country,
                                    postcode = request.vars.billing_postcode)



                bank_details = db.bank_details.insert(card_number = request.vars.card_number, security_code = request.vars.security_code,
                                                  address_id = bank_address, expiry_date = request.vars.expiry_date)






        #Should add date as a datetime object using datetime.date(YYYY, MM, DD)
        db.auth_user.insert(username = request.vars.username, password = db.auth_user.password.validate(request.vars.password)[0],
                       first_name = request.vars.first_name, last_name = request.vars.last_name, birthdate = request.vars.dob, bank_details_id = bank_details,
                       address_id = address)

        auth.login_bare(request.vars.username, request.vars.password)
        redirect(URL('profile','profile'))


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
