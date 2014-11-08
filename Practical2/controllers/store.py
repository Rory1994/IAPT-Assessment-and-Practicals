def index():
    return dict()

def books():
    return dict(features=db(db.products.type == 'Book').select())

def videos():
    return dict()