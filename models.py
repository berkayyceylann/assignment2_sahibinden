from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_no = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product {self.description}>'
