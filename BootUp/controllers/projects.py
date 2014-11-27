def project():

    session.old_url = request.env.http_referer
    project_id = request.args(0)
    project = db(db.project.id == project_id).select().first()

    if project.status == "Not Available":
        redirect(URL('default','index'))
    percentage_completed = int((float(project.funding_raised)/float(project.funding_target))*100)
    pledge_levels = db(db.pledge_levels.project_id ==project_id).select(orderby=db.pledge_levels.pledge_amount)
    pledges_made_on_project = db((db.pledge_levels.project_id == project_id)  & (db.pledge_levels.id == db.pledges.pledge_levels_id)).select()


    return dict(project = project, percentage_completed = percentage_completed, pledge_levels = pledge_levels,
                pledges_made_on_project = pledges_made_on_project)


def make_pledge():

    project_id = request.args(0)
    pledge_level_id = request.args(1)

    if auth.is_logged_in() is False:
        redirect(URL('default','login', vars=dict(function = request.function,controller = request.controller, project_id = project_id, pledge_level_id = pledge_level_id )))

    form= FORM(BUTTON( I(_class="icon-shopping-cart icon-white"),' Yes, make the pledge', _type='submit', _class='btn btn-primary btn-large'))

    project = db(db.project.id == project_id).select().first()
    pledge_level = db(db.pledge_levels.id == pledge_level_id).select().first()

    if form.process().accepted:

        db.pledges.insert(username = auth._get_user_id(), pledge_levels_id = pledge_level_id)
        new_funding_raised = project.funding_raised + pledge_level.pledge_amount
        project.update_record(funding_raised = new_funding_raised)
        redirect(URL('projects', 'project', args=project.id))



    return dict(project = project, pledge_level = pledge_level, form = form)