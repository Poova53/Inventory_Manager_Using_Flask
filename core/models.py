from core import db
from datetime import datetime

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<product {self.name}>"


class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    
    def __repr__(self):
        return f"<location {self.name}>"


class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    from_location_id = db.Column(db.Integer, db.ForeignKey("location.location_id"))
    to_location_id = db.Column(db.Integer, db.ForeignKey("location.location_id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"))
    quantity = db.Column(db.Integer, nullable=False)
    
    product = db.relationship("Product", foreign_keys=[product_id])
    from_location = db.relationship("Location", foreign_keys=[from_location_id])
    to_location = db.relationship("Location", foreign_keys=[to_location_id])
    
    def __repr__(self):
        return f"<{self.quantity} {self.product.name}(s) in {self.to_location.name}>"