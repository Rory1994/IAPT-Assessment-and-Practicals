
@auth.requires_login(otherwise=URL('default','login'))
def profile():

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    number_of_projects = len(db(db.project.username == auth._get_user_id()).select())
    number_of_pledges = len(db(db.pledges.username == auth._get_user_id()).select())


    return dict(user=user, number_of_projects=number_of_projects, number_of_pledges=number_of_pledges )

@auth.requires_login(otherwise=URL('default','login'))
def projects():

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()

    open_for_pledges_projects = db(db.project.username == auth._get_user_id() and db.project.status  == "Open for Pledges").select()
    not_available_projects = db(db.project.username == auth._get_user_id() and db.project.status  == "Not Available").select()
    funded_projects = db(db.project.username == auth._get_user_id() and db.project.status  == "Funded").select()
    not_funded_projects = db(db.project.username == auth._get_user_id() and db.project.status  == "Not Funded").select()



    return dict(user=user, open_for_pledges_projects = open_for_pledges_projects, not_available_projects = not_available_projects,
                funded_projects = funded_projects, not_funded_projects = not_funded_projects)

@auth.requires_login(otherwise=URL('default','login'))
def pledges():

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()



    return dict(user=user)

@auth.requires_login(otherwise=URL('default','login'))
def information():

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()
    bank_details = db(db.bank_details.id == user.bank_details_id).select().first()
    address = db(db.address.id == user.address_id).select().first()
    bank_address = db(db.address.id == bank_details.address_id).select().first()

    return dict(user=user,  bank_details = bank_details, address=address, bank_address=bank_address)


@auth.requires_login(otherwise=URL('default','login'))
def create():



    options = ['Art', 'Comics', 'Crafts', 'Fashion', 'Film', 'Games', 'Music', 'Photography', 'Technology']


    form= FORM(FIELDSET(

                        DIV(LABEL('Project Title:', _for='project_title'),
                            INPUT(_id='project_title', _name='project_title', _type='text', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),

                            LABEL('Short Project Description:', _for='short_project_description'),
                            TEXTAREA(_id='short_project_description', _name='short_project_description', _cols = '50', _rows = '5', _class='span6',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_LENGTH(120, error_message=T("Must be at most 120 characters"))]),

                            LABEL('Category:', _for='category'),
                            SELECT(*options, _name='category', _id='category', requires= [IS_IN_SET(options, error_message=T("Category from list must be chosen"))]),

                             LABEL('Project Image:', _for='image'),
                            INPUT(_id='image', _name='image', _type='file', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))

                            ,_class='controls control-group'),


                            DIV(LABEL('Funding Goal (in GBPs):', _for='funding_goal'),
                            INPUT(_id='funding_goal', _name='funding_goal', _type='text', _class='span4',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),

                            LABEL('Long Description of Project Goals:', _for='long_description'),
                            TEXTAREA(_id='long_description', _name='long_description',_cols = '50', _rows = '10', _class='span6',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),

                            LABEL('Project Story:', _for='project_story'),
                            TEXTAREA(_id='project_story', _name='project_story',_cols = '50', _rows = '10', _class='span6',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))

                            ,_class='controls control-group'),



                            DIV(
                                LEGEND('Pledges'),

                                DIV(
                                    LABEL('Pledge 1:'),
                                    INPUT(_id='pledge_amount1', _name='pledge_amount1', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
                                    TEXTAREA(_placeholder = 'Reward', _id='pledge_reward1', _name='pledge_reward1',_cols = '50', _rows = '5', _class='span5', requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                                , _class='controls controls-group'),


                                DIV(
                                    LABEL('Pledge 2:'),
                                    INPUT(_id='pledge_amount2', _name='pledge_amount2', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
                                    TEXTAREA(_placeholder = 'Reward', _id='pledge_reward2', _name='pledge_reward2',_cols = '50', _rows = '5', _class='span5',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                                , _class='controls controls-group'),

                                DIV(
                                    LABEL('Pledge 3:'),
                                    INPUT(_id='pledge_amount3', _name='pledge_amount3', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
                                    TEXTAREA(_placeholder = 'Reward', _id='pledge_reward3', _name='pledge_reward3',_cols = '50', _rows = '5', _class='span5',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                                , _class='controls controls-group'),

                                DIV(
                                    LABEL('Pledge 4:'),
                                    INPUT(_id='pledge_amount4', _name='pledge_amount4', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
                                    TEXTAREA(_placeholder = 'Reward', _id='pledge_reward4', _name='pledge_reward4',_cols = '50', _rows = '5', _class='span5',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                                , _class='controls controls-group'),

                                DIV(
                                    LABEL('Pledge 5:'),
                                    INPUT(_id='pledge_amount5', _name='pledge_amount5', _type='text', _placeholder = "£", _class='span2',requires=[IS_NOT_EMPTY(error_message=T("Field cannot be left empty")), IS_INT_IN_RANGE(0, 1000000000, error_message=T("Must be a whole number between £0 and £1000000000"))]),
                                    TEXTAREA(_placeholder = 'Reward', _id='pledge_reward5', _name='pledge_reward5',_cols = '50', _rows = '5', _class='span5',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty")))
                                , _class='controls controls-group')


                            ,_class='controls control-group'),


                         INPUT(_type='submit', _class='btn btn-primary btn-large', _value='Create Project')


    ))

    if form.process().accepted:
        project = db.project.insert(username = auth._get_user_id, short_description = request.vars.short_project_description,
                                    status='Not Available', image = request.vars.image, category = request.vars.category,
                                    total_raised = 0, story = request.vars.project_story, time_opened_for_pledges = request.now,
                                    funding_goal = int(request.vars.funding_goal), title = request.vars.project_title,
                                    long_description = request.vars.long_description)


        db.pledge_levels.insert(project_id = project, amount = request.vars.pledge_amount1, reward = request.vars.pledge_reward1)
        db.pledge_levels.insert(project_id = project, amount = request.vars.pledge_amount2, reward = request.vars.pledge_reward2)
        db.pledge_levels.insert(project_id = project, amount = request.vars.pledge_amount3, reward = request.vars.pledge_reward3)
        db.pledge_levels.insert(project_id = project, amount = request.vars.pledge_amount4, reward = request.vars.pledge_reward4)
        db.pledge_levels.insert(project_id = project, amount = request.vars.pledge_amount5, reward = request.vars.pledge_reward5)

        redirect(URL('projects'))



    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()


    return dict(user=user, form=form)

@auth.requires_login(otherwise=URL('default','login'))
def change_password():
    form = FORM(FIELDSET(
                        LEGEND('Change Password'),
                        DIV(LABEL('Current Password:', _for='current_password'),INPUT(_id='current_password', _name='current_password', _type='password', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('New Password:', _for='new_password'),INPUT(_id='new_password', _name='new_password', _type='password', _class='span4',requires=IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))),
                            LABEL('Confirm New Password:', _for='confirm_new_password'),INPUT(_id='confirm_new_password', _name='confirm_new_password', _type='password', _class='span4'
                            , requires=[IS_EQUAL_TO(request.vars.confirm_new_password, error_message=T("Passwords do not match")), IS_NOT_EMPTY(error_message=T("Field cannot be left empty"))]),
                            _class='controls control-group'),

                        INPUT(_type='submit', _class='btn btn-primary', _value='Change Password')
    ))

    if form.process(onvalidation = change_password_validation).accepted:

        user = db(db.auth_user.id == auth._get_user_id).select()
        user.update_record(password = db.auth_user.password.validate(form.vars.new_password)[0])

        response.flash = DIV('Password has been successfully changed', _class="alert alert-success")

    elif form.errors:
         response.flash = DIV('Form not filled out successfully', _class="alert alert-error")

    user = (db(db.auth_user.id == auth._get_user_id()).select()).first()


    return dict(form = form, user = user)

def change_password_validation(form):

    check_current_password_is_correct = db(db.auth_user.id == auth._get_user_id and db.auth_user.password == db.auth_user.password.validate(form.vars.current_password)[0]).select()

    if(len(check_current_password_is_correct) == 0):
        form.errors.current_password = "Current password is incorrect"
