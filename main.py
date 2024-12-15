"Часть 3: Базовые операции с базой данных в веб-приложении"
from fastapi import FastAPI, Form,status
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine,select,update,delete
from sqlalchemy.orm import Session
from db_creation import Post, User
engine = create_engine('postgresql://postgres:1234@localhost/Backend')
engine.connect()
session = Session(engine)
app = FastAPI()
@app.get("/")
def read_root():
    "Main page"
    return FileResponse("main.html")

@app.get("/create-user")
def create_user():
    "loads create-user page"
    return FileResponse("create_user.html")

@app.post("/cruser")
def create_user_post(username = Form(),email=Form(),password = Form()):
    "gets create-user info"
    session.add(User(username=username,email= email,password=password))
    session.commit()
    return RedirectResponse('/watch-users', status_code=status.HTTP_302_FOUND)

@app.get("/create-post")
def create_post():
    "loads create-post page"
    return FileResponse("create_post.html")

@app.post("/crpost")
def create_post_post(title = Form(),content = Form(), user_id=Form()):
    "gets create-user info"
    session.add(Post(title = title, content = content, user_id = user_id))
    session.commit()
    return RedirectResponse("/watch-posts", status_code=status.HTTP_302_FOUND)

@app.get("/watch-posts")
def watch_posts():
    "loads create-post page"
    result = session.execute(select(Post))
    page = ""
    for data in result.scalars():
        page+=f"title: {data.title} | content: {data.content} | user_id: {data.user_id}<br>"
    return HTMLResponse(page)
@app.get("/watch-users")
def watch_users():
    "loads create-post page"
    result = session.execute(select(User))
    page = ""
    for data in result.scalars():
        page += f"username: {data.username} | email: {data.email} | password: {data.password}<br>"
    return HTMLResponse(page)
@app.get("/redact-post")
def redact_post():
    "loads create-post page"
    return FileResponse("edit_post.html")

@app.post("/redactp")
def redact_post_put(id=Form(),title=Form(),content=Form()):
    "loads create-post page"
    session.execute(update(Post).where(Post.id==id).values(title=title,content = content))
    session.commit()
    return RedirectResponse("/watch-posts", status_code=status.HTTP_302_FOUND)

@app.get("/redact-user")
def redact_user():
    "loads create-post page"
    return FileResponse("edit_user.html")

@app.post("/redactu")
def redact_user_put(id = Form(),username=Form(),email=Form(),password=Form()):
    "loads create-post page"
    session.execute(update(User).where(User.id == id).values(username=username,
                                                               email=email,
                                                               password=password))
    session.commit()
    return RedirectResponse("/watch-users", status_code=status.HTTP_302_FOUND)
@app.get("/delete-user")
def delete_user():
    "deletes user"
    return FileResponse("delete_user.html")
@app.post ("/deleteu")
def delete_user_delete(username=Form()):
    "deletes user"
    session.execute(delete(Post).where(Post.user_id==select(User.id).where(User.username==username)))
    session.execute(delete(User).where(User.username==username))
    session.commit()
    return RedirectResponse("/watch-users", status_code=status.HTTP_302_FOUND)
@app.get("/delete-post")
def delete_post():
    "deletes post"
    return FileResponse("delete_post.html")
@app.post ("/deletep")
def delete_post_delete(user_id=Form(),title=Form()):
    "deletes post"
    session.execute(delete(Post).where(Post.user_id==user_id, Post.title==title))
    session.commit()
    return RedirectResponse("/watch-posts", status_code=status.HTTP_302_FOUND)
