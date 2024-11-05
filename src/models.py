import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base

from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(120), unique=True)

    followers = relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="user")


class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    

    user = relationship("User", foreign_keys=[user_to_id], back_populates="followers")


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    

    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")


# Tabla de Media
class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum("image", "video", name="media_type"))
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'))
    

    post = relationship("Post", back_populates="media")


# Tabla de Comentarios
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    

    author = relationship("User")
    post = relationship("Post", back_populates="comments")


User.posts = relationship("Post", back_populates="user")


if __name__ == '__main__':

    try:
        result = render_er(Base, 'diagram.png')
        print("Success! Check the diagram.png file")
    except Exception as e:
        print("There was a problem generating the diagram")
        raise e
