# crud.py
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import func

#category
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def delete_category(db: Session, category_id: int):
    db.query(models.Category).filter(models.Category.id == category_id).delete()
    db.commit()

def get_all_categories(db: Session):
    return db.query(models.Category).all()

def update_category(db: Session, category_id: int, category: schemas.CategoryCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not db_category:
        raise ValueError("Category does not exist.")

    # Update category details
    db_category.name = category.name
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)
    return db_category

#product
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, db_product: models.Product, product: schemas.ProductUpdate):
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session):
    return db.query(models.Product).all()


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not db_product:
        raise ValueError("Product does not exist.")

    db.delete(db_product)
    db.commit()

#order
def create_order(db: Session, order: schemas.OrderCreate):
    total_amount = 0
    products_in_order = []

    # Fetch all the products in the order by their IDs
    products = db.query(models.Product).filter(models.Product.id.in_(order.products)).all()

    if not products or len(products) != len(order.products):
        raise ValueError("One or more products do not exist.")

    for product in products:
        # Check stock availability for each product
        if product.stock <= 0:
            raise ValueError(f"Product {product.name} is out of stock.")
        
        total_amount += product.price
        product.stock -= 1  # Decrease stock for each product ordered
        products_in_order.append(product)

    # Create the order
    db_order = models.Order(
        user=order.user,
        total_amount=total_amount,
        created_at=func.now()
    )
    db_order.products.extend(products_in_order)

    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except IntegrityError:
        db.rollback()
        raise ValueError("Error creating order.")

    # Return the order with product IDs, not full product objects
    return {
        "id": db_order.id,
        "user": db_order.user,
        "products": [product.id for product in products_in_order],  # Extract product IDs
        "total_amount": db_order.total_amount,
        "created_at": db_order.created_at
    }

# Function to retrieve an order by its ID
def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    
    return {
        "id": order.id,
        "user": order.user,
        "products": [product.id for product in order.products],  # Extract product IDs
        "total_amount": order.total_amount,
        "created_at": order.created_at
    }

def get_all_orders(db: Session):
    orders = db.query(models.Order).all()

    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "user": order.user,
            "products": [product.id for product in order.products],  # Extract product IDs
            "total_amount": order.total_amount,
            "created_at": order.created_at
        })

    return result