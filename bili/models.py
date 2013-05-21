from config import *
from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import DateTime, Float
from sha import sha

__all__ = ['User', 'engine']

Base = declarative_base()
DB_URL = '%s://%s:%s@%s/%s%s' % (
        DATABASE['PREFIX'],
        DATABASE['USERNAME'],
        DATABASE['PASSWORD'],
        DATABASE['HOST'],
        DATABASE['NAME'],
        ':'+DATABASE['PORT'] if DATABASE['PORT'] else '',
    )
engine = create_engine(DB_URL)

class User(Base):
    '''
    User model
    '''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    email = Column(String(50))
    password = Column(String(50))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.raw_password = password
        self.password = self.encrypt(password)

    @staticmethod
    def encrypt(plaintext):
        '''
        use SHA to encrypt the password 
        '''
        return sha(plaintext).hexdigest()

    def __repr__(self):
        return "<User, %s>" % self.username

class Interest(Base):
    '''
    The goods user interested in
    '''
    __tablename__ = 'interests'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    updatetime = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    price = Column(Float)
    img_url = Column(String(2048))

    user = relationship("User", backref=backref('interests', order_by=id))

    def __init__(self, name, user, price, img_url):
        self.name = name
        self.updatetime = datetime()
        self.user = user
        self.user_id = user_id
        self.price = price
        self.img_url = img_url

    def update_price(self):
        '''
        TODO
        Update all the goods' information
        '''
        pass

    def __repr__(self):
        return "<Interest, %s, %s>" % (self.user.username, self.name)



if __name__ == '__main__':
    Base.metadata.create_all(engine)
