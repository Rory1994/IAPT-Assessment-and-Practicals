
@auth.requires_login(otherwise=URL('default','login'))
def profile():

    user = (db(db.auth_user.id == auth._get_user_id()).select())[0]

    number_of_projects = len(db(db.project.username == auth._get_user_id()).select())
    number_of_pledges = len(db(db.pledges.username == auth._get_user_id()).select())


    return dict(user=user, number_of_projects=number_of_projects, number_of_pledges=number_of_pledges )
