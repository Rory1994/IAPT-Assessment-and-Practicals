# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

#Exam Number: Y0071297

import datetime

#Initialise countries, years and months arrays for use in select statements later.
COUNTRIES=['United Kingdom', 'United States', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Ivory Coast', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea','South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'FYROM', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe', 'Other']
years = []
months = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]

for i in xrange(100):
    if i < 10:
        number = '0' + str(i)
    else:
        number = str(i)

    years.append(number)


def index():

    # Queries returning the 6 closest projects to funding and 6 most recently opened projects
    closest_projects_to_being_funded = db((db.project.funding_target > db.project.funding_raised)&(db.project.status == "Open for Pledges")).select(orderby=~(db.project.funding_raised/db.project.funding_target), limitby = (0,6))
    newest_projects = db((db.project.status == "Open for Pledges") &(db.project.funding_target > db.project.funding_raised)).select(orderby=~(db.project.opened_for_pledges_date), limitby = (0,6))

    return dict( closest_projects_to_being_funded =  closest_projects_to_being_funded, newest_projects = newest_projects)

def login():


    # Create login form
    form = FORM(LEGEND('Login'),
                INPUT(_type='text', _name='username', _class = 'input-block-level', _placeholder='username', requires=IS_NOT_EMPTY( error_message=T("Please enter a username"))),
                INPUT(_type='password',_name='password', _class = 'input-block-level', _placeholder='password', requires=IS_NOT_EMPTY(error_message=T("Please enter a password"))), INPUT(_type='submit', _class='btn btn-primary', _value='Login'),
                A('Register',_href=URL('register'), _role='button', _class='btn btn-info'))

    if form.process().accepted:
        # Log user in
        user = auth.login_bare(request.vars.username, request.vars.password)
        if(user is False):
            # If username and password combination is not found in database, return this message
            response.flash = DIV("Invalid Username/Password Combination", _class='alert alert-error')
        else:
            # Checks whether user was sent to login form when trying to pledge. If true, the user is redirected back
            # to the pledge they was trying to make.
            if request.vars.controller:
                redirect(URL(request.vars.controller, request.vars.function, args=[request.vars.project_id, request.vars.pledge_level_id]))
            else:
                # Redirect them to their profile page.
                redirect(URL('profile','profile'))
    elif form.errors:
        response.flash = DIV("Username or Password field is empty", _class='alert alert-error')


    return dict(form=form)




def register():

    form_has_errors = False

    # Create register form for step one of user registration
    form= FORM(FIELDSET(

                        LEGEND('Personal Information'),
                        DIV(LABEL('First Name:', _for='first_name'),INPUT(_id='first_name', _name='first_name', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Last Name:', _for='last_name'),INPUT(_id='last_name', _name='last_name', _type='text', _class='span4',_style="display: block;")
                            ,_class='controls control-group'),


                        DIV( LABEL('Date of Birth:', A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Example: 25/02/1994",href="#", rel='tooltip')),
                             INPUT( _name='dob', _id='dob', _type='text',_placeholder = ('dd/mm/yyyy'),_maxlength='10', _class='date',_style="display: block;")
                             ,_class="controls controls-row"),

                        LEGEND('Login Credentials'),
                        DIV(LABEL('Username:', _for='username'),INPUT(_id='username', _name='username', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Password:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Password must be at least six characters long",href="#", rel='tooltip') ,_for='password'),INPUT(_id='password', _name='password', _type='password', _class='span4',_style="display: block;"),
                            LABEL('Confirm Password: ',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be be the same as password",href="#", rel='tooltip'), _for='confirm_password'),INPUT(_id='confirm_password', _name='confirm_password', _type='password', _class='span4',_style="display: block;")
                            ,_class='controls control-group'),

                        LEGEND('Home Address'),
                        DIV(LABEL('Street:', _for='street'),INPUT(_id='street', _name='street', _type='text', _class='span4',_style="display: block;"),
                            LABEL('City:', _for='city'),INPUT(_id='city', _name='city', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Postcode:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be in the format **** ***. Example: IG90 7GH",href="#", rel='tooltip'), _for='postcode'),INPUT(_id='postcode', _name='postcode', _type='text', _class='span4',_style="display: block;"),
                            LABEL('Country:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Choose a country from the list",href="#", rel='tooltip') ,_for='country'),SELECT(*COUNTRIES, _id='country', _name='country',_style="display: block;")
                            ,_class='controls control-group'),

                        BUTTON('Go on to step two ', I(_class="icon-arrow-right icon-white"), _type='submit', _class='btn btn-block btn-primary btn-large', )

    ))

    # Checks if the user has just come back from a later step. If they have the form is prepopulated.
    if (request.vars.coming_back_from_step_two == "True"):
        form.vars.first_name = session.register.first_name
        form.vars.last_name = session.register.last_name
        form.vars.dob = session.register.dob
        form.vars.street = session.register.street
        form.vars.city = session.register.city
        form.vars.country = session.register.country
        form.vars.postcode = session.register.postcode
        form.vars.username = session.register.username


    if form.process(onvalidation=register_validation).accepted:
        # If form passes validation, store request.vars in a session variable and redirect to step 2.
        session.register = request.vars
        redirect(URL('default','register_step2'))

    elif form.errors:
        # Ensure errors are displayed.
        form_has_errors = True
        response.flash = form.errors


    return dict(form=form, form_has_errors = form_has_errors)

def register_validation(form):

    # Ensures first name cannot be left empty
    if form.vars.first_name == "":
        form.errors.first_name = "First name must be entered"

    # Ensures last name cannot be left empty
    if form.vars.last_name == "":
        form.errors.last_name = "Last name must be entered"

    # Ensures date is entered in the right format
    date_validator = IS_DATE(format='%d/%m/%Y', error_message=T("Date should be given as dd/mm/yyyy"))
    if date_validator(form.vars.dob)[1] is not None:
        form.errors.dob = "Date should be given as dd/mm/yyyy"

    # Ensures username is not already in database
    username_validator = IS_NOT_IN_DB(db, 'auth_user.username', error_message='Username already taken')
    if username_validator(form.vars.username)[1] is not None:
        form.errors.username = username_validator(form.vars.username)[1]

    # Ensures a username is entered
    if form.vars.username == "":
        form.errors.username = "Username must be entered"

    if form.vars.password == "":
        form.errors.password = "Password must be entered"

    # Ensures password of at least length 6 is entered
    password_length_validator =  IS_LENGTH(minsize=6, error_message="Password must be at least 6 characters")
    if password_length_validator(form.vars.password)[1] is not None:
        form.errors.password = password_length_validator(form.vars.password)[1]

    # Ensures password is not empty
    if form.vars.confirm_password == "":
        form.errors.confirm_password = "Password must be entered"

    #Ensures two password are the same
    confirm_password_validator = IS_EQUAL_TO(form.vars.password, error_message=T("Passwords do not match"))
    if confirm_password_validator(form.vars.confirm_password)[1] is not None:
        form.errors.confirm_password = confirm_password_validator(form.vars.confirm_password)[1]

    #Ensures the street is entered
    if form.vars.street == "":
        form.errors.street = "Street must be entered"

    # Ensures the city is entered
    if form.vars.city == "":
        form.errors.city = "City must be entered"

    # Ensures the country is entered.
    if form.vars.country == "":
        form.errors.country = "Country must be entered"

    # Ensures the postcode is entered in the correct format.
    postcode_validator =  IS_MATCH('^[A-Z0-9]{4} [A-Z0-9]{3}$', error_message="Postcode is not valid. Must be split into a block of 4 characters and a block of 3 characters. Example: IG90 7GH" )
    if postcode_validator(form.vars.postcode)[1] is not None:
        form.errors.postcode = postcode_validator(form.vars.postcode)[1]


def register_step2():

    form_has_errors = False

    #Brings forward the request variables from step one
    if session.register:
        request.vars.update(session.register)

    # Initiliases the form for step 2
    form= FORM(FIELDSET(

                        LEGEND('Billing Information'),
                        DIV(LABEL('Card Number:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be a 12 digits consisting of just numbers. No spaces should be included",href="#", rel='tooltip') ,_for='card_number'),INPUT(_id='card_number', _name='card_number', _type='text',_maxlength='12' ,_class='span4',_style="display: block;"),
                            LABEL('Security Code:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be 3 digits consisting of just numbers",href="#", rel='tooltip'), _for='security_code'),INPUT(_id='security_code', _name='security_code', _type='text',_maxlength='3', _class='span4',_style="display: block;")
                            ,_class='controls control-group'),

                        DIV(
                            LABEL('Expiry Date:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Select a valid date in the format mm/yy",href="#", rel='tooltip')),
                            SELECT(*months, _value='mm', _name='expiry_date_month', _id='expiry_date_month' ),
                            SPAN(' / '),
                            SELECT(*years, _value='yy', _name='expiry_date_year', _id='expiry_date_year')
                            , _class='controls controls-row'),

                        LEGEND('Billing Address'),
                        DIV(LABEL(INPUT(_id='billing_checkbox', _name='billing_checkbox', _value='yes', _onclick='javascript:toggleAddressAvailibility();', _type='checkbox' ), 'Same as Home Address',_class='checkbox'),
                            DIV(LABEL('Street:', _for='billing_street'),INPUT( _name='billing_street', _type='text', _class='span4',_style="display: block;"), _id='billing_street'),
                            DIV(LABEL('City:', _for='billing_city'),INPUT( _name='billing_city', _type='text', _class='span4',_style="display: block;"), _id='billing_city'),
                            DIV(LABEL('Postcode:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Must be in the format **** ***. Example: IG90 7GH",href="#", rel='tooltip'), _for='billing_postcode'),INPUT( _name='billing_postcode', _type='text', _style="display: block;", _class='span4'), _id='billing_postcode'),
                            DIV(LABEL('Country:',A(I(_class=" icon-question-sign"), _id='tip',_class='tip',_title="Choose a country from the list",href="#", rel='tooltip'), _for='billing_country'),SELECT(*COUNTRIES, _name='billing_country'), _id='billing_country')
                            ,_class='controls control-group last_form_section'),

                         INPUT(_type='submit', _class='btn btn-primary btn-large btn-block', _value='Register')

     ))

    if form.process(onvalidation=register_step2_validation).accepted:

        # Combines expiry date into correct format
        expiry_date = request.vars.expiry_date_month + "/" + request.vars.expiry_date_year

        # Checks whether address is already in the database.
        addressAlreadyInDBQuery = db((db.address.street == request.vars.street) & (db.address.city == request.vars.city) & (db.address.country == request.vars.country) &(db.address.postcode == request.vars.postcode)).select()

        # If address already in database, just link to that record. Otherwise insert address
        if(len(addressAlreadyInDBQuery) >0):
            address = addressAlreadyInDBQuery[0].id
        else:
            address = db.address.insert(street = request.vars.street, city = request.vars.city, country = request.vars.country,
                        postcode = request.vars.postcode)

        # Checks whether bank details already in database
        bankDetailsAlreadyInDBQuery = db(db.bank_details.card_number == request.vars.card_number).select()

         # If bank details already in database, just link to that record.
        if(len( bankDetailsAlreadyInDBQuery) >0):
            bank_details = bankDetailsAlreadyInDBQuery[0].id

        else:
            # If not already in db, check whether billing address is same as home
            if(request.vars.billing_checkbox == 'yes'):
                bank_details = db.bank_details.insert(card_number = request.vars.card_number, security_code = request.vars.security_code,
                                              address_id = address, expiry_date = expiry_date)

            else:
                #If address for card is different from home, check if address is already in db
                billingAddressAlreadyInDBQuery = db((db.address.street ==request.vars.billing_street) & (db.address.city == request.vars.billing_city)
                                             & (db.address.country == request.vars.billing_country) &
                                            (db.address.postcode == request.vars.billing_postcode)).select()

                # If address is already in db, link to it. Otherwise insert it.
                if(len(billingAddressAlreadyInDBQuery) >0):
                    bank_address = billingAddressAlreadyInDBQuery[0].id
                else:
                    bank_address = db.address.insert(street = request.vars.billing_street, city = request.vars.billing_city, country = request.vars.billing_country,
                                    postcode = request.vars.billing_postcode)



                bank_details = db.bank_details.insert(card_number = request.vars.card_number, security_code = request.vars.security_code,
                                                  address_id = bank_address, expiry_date = request.vars.expiry_date)

        #Break up date of birth into an array in the format [DAY, MONTH, YEAR]
        date_of_birth = request.vars.dob.split('/')

        # Insert user into user table.
        db.auth_user.insert(username = request.vars.username, password = db.auth_user.password.validate(request.vars.password)[0],
                       first_name = request.vars.first_name, last_name = request.vars.last_name, birthdate = datetime.date(int(date_of_birth[2]), int(date_of_birth[1]), int(date_of_birth[0])), bank_details_id = bank_details,
                       address_id = address)

        #Log user in, clear session variables and redirect to their profile.
        auth.login_bare(request.vars.username, request.vars.password)
        session.register = None
        session.flash = DIV( H4("You successfully registered for BootUp"),_class="alert alert-success")
        redirect(URL('profile','profile'))

    elif form.errors:
        form_has_errors = True
        response.flash = form.errors





    return dict(form=form, form_has_errors = form_has_errors)

def register_step2_validation(form):

    # Ensure secuity code is in correct format
    security_code_validator = IS_MATCH('^[0-9]{3}$', error_message='Security code must contain 3 numbers')
    if security_code_validator(form.vars.security_code)[1] is not None:
        form.errors.security_code = security_code_validator(form.vars.security_code)[1]

    # Ensure card number is in correct format
    card_number_validator = IS_MATCH('^[0-9]{12,12}$', error_message="Card number must be 12 digits long. No spaces should be included" )
    if card_number_validator(form.vars.card_number)[1] is not None:
        form.errors.card_number = card_number_validator(form.vars.card_number)[1]

    # If billing address isnt same as home.
    if form.vars.billing_checkbox != "yes":

        #Ensure billing street isnt empty
        if form.vars.billing_street =="":
            form.errors.billing_street = "Street must be entered"

        #Ensure billing city isnt empty
        if form.vars.billing_city =="":
            form.errors.billing_city = "City must be entered"

        # Ensure billing country isnt empty
        if form.vars.billing_country =="":
            form.errors.billing_country = "Country must be entered"

        # Ensure billing postcode isnt empty
        if form.vars.billing_postcode =="":
            form.errors.billing_postcode = "Postcode must be entered"

        # Ensure postcode is in the right format.
        postcode_validator =  IS_MATCH('^[A-Z0-9]{4} [A-Z0-9]{3}$', error_message="Postcode is not valid. Must be split into a block of 4 characters and a block of 3 characters. Example: IG90 7GH" )
        if postcode_validator(form.vars.billing_postcode)[1] is not None:
            form.errors.billing_postcode = postcode_validator(form.vars.billing_postcode)[1]

    if form.vars.expiry_date_month not in months or form.vars.expiry_date_year not in years:
        form.errors.expiry_date_year = "Expiry Date must be entered"


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
