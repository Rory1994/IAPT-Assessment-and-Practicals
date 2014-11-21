
@auth.requires_login(otherwise=URL('default','login'))
def profile():

    user = (db(db.auth_user.id == auth._get_user_id()).select())[0]

    number_of_projects = len(db(db.project.username == auth._get_user_id()).select())
    number_of_pledges = len(db(db.pledges.username == auth._get_user_id()).select())


    return dict(user=user, number_of_projects=number_of_projects, number_of_pledges=number_of_pledges )

@auth.requires_login(otherwise=URL('default','login'))
def projects():

    user = (db(db.auth_user.id == auth._get_user_id()).select())[0]



    return dict(user=user)

@auth.requires_login(otherwise=URL('default','login'))
def pledges():

    user = (db(db.auth_user.id == auth._get_user_id()).select())[0]



    return dict(user=user)

@auth.requires_login(otherwise=URL('default','login'))
def information():

    user = (db(db.auth_user.id == auth._get_user_id()).select())[0]
    bank_details = db(db.bank_details.id == user.bank_details_id).select()[0]
    address = db(db.address.id == user.address_id).select()[0]
    bank_address = db(db.address.id == bank_details.address_id).select()[0]

    return dict(user=user,  bank_details = bank_details, address=address, bank_address=bank_address)

