"Часть 2: Взаимодействие с базой данных"
from sqlalchemy import create_engine,select,update,delete
from sqlalchemy.orm import Session
from db_creation import Post, User

# добавляет в таблицу Users несколько записей
engine = create_engine('postgresql://postgres:1234@localhost/Backend')
engine.connect()
session = Session(engine)
def add_users():
    "добавляет в таблицу Users несколько записей"
    session.add(User(username="Pavel",email= 'Pavel@mail.com',password="123123"))
    session.add(User(username="IWishAgain",email= 'IWishAgain@mail.com',password="12121412424"))
    session.add(User(username="Seyn",email= 'Seyn@mail.com',password="141212321"))
    session.add(User(username="Tatara",email= 'Tatara@mail.com',password="qweqrqwreq"))
    session.commit()
def add_posts():
    "добавляет в таблицу Posts несколько записей"
    session.add(Post(title="Test",content= 'TestoTestoTesto',user_id=2))
    session.add(Post(title="IWish",content= 'I Wish To Be A Butterfly',user_id=3))
    session.add(Post(title="Cars",content= 'I love cars',user_id=1))
    session.add(Post(title="...",content= 'Cool!',user_id=4))
    session.commit()
def get_users():
    "извлекает все записи из таблицы Users"
    result = session.execute(select(User))
    for data in result.scalars():
        print(f"username: {data.username} | email: {data.email} | password: {data.password}")
def get_posts():
    "извлекает все записи из таблицы Posts"
    result = session.execute(select(Post))
    for data in result.scalars():
        print(f"title: {data.title} | content: {data.content} | user_id: {data.user_id}")
def get_posts_by_user(user):
    "извлекает записи из таблицы Posts, созданные конкретным пользователем"
    ident = session.execute(select(User.id).where(User.username == user)).scalar()
    result = session.execute(select(Post).where(Post.user_id == ident))
    for data in result.scalars():
        print(f"title: {data.title} | content: {data.content}")
def update_email(ident,email):
    "обновляет поле email у одного из пользователей"
    session.execute(update(User).where(User.id == ident).values(email=email))
    session.commit()
def update_content(ident,content):
    "обновляет поле content у одного из постов"
    session.execute(update(Post).where(Post.id == ident).values(content=content))
    session.commit()
def delete_post(ident):
    "удаляет один из постов"
    session.execute(delete(Post).where(Post.id == ident))
    session.commit()
def delete_user(ident):
    "удаляет пользователя и все его посты"
    session.execute(delete(Post).where(Post.user_id == ident))
    session.execute(delete(User).where(User.id == ident))
    session.commit()
