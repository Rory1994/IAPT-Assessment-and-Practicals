def index():
    return dict()

def books():
    product_id = request.args(0)
    if product_id is not None:
        features = db((db.products.type == 'Book') and (db.products.id==product_id)).select()

    else:
        features=db(db.products.type == 'Book').select()


    return dict(features=features)

def videos():

    product_id = request.args(0)
    if product_id is not None:
        features = db((db.products.type == 'Blu-ray') and (db.products.id==product_id)).select()

    else:
        features=db(db.products.type == 'Blu-ray').select()

    return dict(features=features)