from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from uuid import UUID

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(response: Response, book_id: int, db: Session = Depends(get_db)):
    if db.query(models.Book).filter(models.Book.id == book_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Book not found'
        }
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation

    if 'title' not in book or 'author' not in book or 'year' not in book or 'is_published' not in book:
        response.status_code = 400
        return {
            'message': 'Required data is missing'
        }
    elif db.query(models.Book).filter(models.Book.title == book['title']).first() is not None:
        response.status_code = 409
        return {
            'message': 'Book already exists'
        }

    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'], detail=book['detail'], short_desc=book['short_desc'], categories=book['categories'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(response: Response, book_id: int, book: dict, db: Session = Depends(get_db)):
    if db.query(models.Book).filter(models.Book.id == book_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Book not exists'
        }
    db.query(models.Book).filter(models.Book.id == book_id).update(book)
    db.commit()
    return {
        'message': 'Book updated'
    }

@router_v1.delete('/books/{book_id}')
async def delete_book(response: Response, book_id: int, db: Session = Depends(get_db)):
    if db.query(models.Book).filter(models.Book.id == book_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Book not exists'
        }

    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()
    return {
        'message': 'Book deleted'
    }

# Students

@router_v1.get('/students')
async def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router_v1.get('/students/{student_id}')
async def get_student(response: Response, student_id: int, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.id == student_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Student not found'
        }
    return db.query(models.Student).filter(models.Student.id == student_id).first()

@router_v1.post('/students')
async def create_student(student: dict, response: Response, db: Session = Depends(get_db)):

    if 'firstname' not in student or 'lastname' not in student or 'dob' not in student or 'id' not in student:
        response.status_code = 400
        return {
            'message': 'Required data is missing'
        }
    elif db.query(models.Student).filter(models.Student.id == student['id']).first() is not None:
        response.status_code = 409
        return {
            'message': 'Student already exists'
        }

    newstudent = models.Student(firstname = student['firstname'], lastname = student['lastname'], dob = student['dob'], id = student['id'], gender = student['gender'])
    db.add(newstudent)
    db.commit()
    db.refresh(newstudent)
    response.status_code = 201
    return newstudent

@router_v1.delete('/students/{student_id}')
async def delete_student(response: Response, student_id: int, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.id == student_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Student not exists'
        }
    db.query(models.Student).filter(models.Student.id == student_id).delete()
    db.commit()
    return {
        'message': 'Student deleted'
    }

@router_v1.patch('/students/{student_id}')
async def update_student(response: Response, student_id: int, student: dict, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.id == student_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Student not exists'
        }
    db.query(models.Student).filter(models.Student.id == student_id).update(student)
    db.commit()
    return {
        'message': 'Student updated'
    }

# Menus
@router_v1.get('/menus')
async def get_menus(db: Session = Depends(get_db)):
    return db.query(models.Menu).all()

@router_v1.get('/menus/{menu_id}')
async def get_menu(response: Response, menu_id: int, db: Session = Depends(get_db)):
    if db.query(models.Menu).filter(models.Menu.id == menu_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Menu not found'
        }
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()

@router_v1.post('/menus')
async def create_menu(menu: dict, response: Response, db: Session = Depends(get_db)):

    if 'name' not in menu or 'price' not in menu or 'img' not in menu:
        response.status_code = 400
        return {
            'message': 'Required data is missing'
        }
    elif db.query(models.Menu).filter(models.Menu.name == menu['name']).first() is not None:
        response.status_code = 409
        return {
            'message': 'Menu already exists'
        }

    newmenu = models.Menu(name = menu['name'], price = menu['price'], img = menu['img'])
    db.add(newmenu)
    db.commit()
    db.refresh(newmenu)
    response.status_code = 201
    return newmenu

# Orders
@router_v1.get('/orders')
async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.get('/orders/{order_id}')
async def get_order(response: Response, order_id: UUID, db: Session = Depends(get_db)):
    if db.query(models.Order).filter(models.Order.id == order_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Order not found'
        }
    return db.query(models.Order).filter(models.Order.id == order_id).first()

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):

    if 'id' not in order or 'menu_id' not in order or 'quantity' not in order or 'total_price' not in order or 'is_completed' not in order or 'order_time' not in order:
        response.status_code = 400
        return {
            'message': 'Required data is missing'
        }
    elif db.query(models.Order).filter(models.Order.id == order['id']).first() is not None:
        response.status_code = 409
        return {
            'message': 'Order already exists'
        }

    neworder = models.Order(id = order['id'], menu_id = order['menu_id'], quantity = order['quantity'], total_price = order['total_price'], is_completed = order['is_completed'], order_time = order['order_time'], note = order['note'])
    db.add(neworder)
    db.commit()
    db.refresh(neworder)
    response.status_code = 201
    return neworder

@router_v1.delete('/orders/{order_id}')
async def delete_order(response: Response, order_id: UUID, db: Session = Depends(get_db)):
    if db.query(models.Order).filter(models.Order.id == order_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Order not exists'
        }
    db.query(models.Order).filter(models.Order.id == order_id).delete()
    db.commit()
    return {
        'message': 'Order deleted'
    }

@router_v1.patch('/orders/{order_id}')
async def update_order(response: Response, order_id: UUID, order: dict, db: Session = Depends(get_db)):
    if db.query(models.Order).filter(models.Order.id == order_id).first() is None:
        response.status_code = 404
        return {
            'message': 'Order not exists'
        }
    db.query(models.Order).filter(models.Order.id == order_id).update(order)
    db.commit()
    return {
        'message': 'Order updated'
    }

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
