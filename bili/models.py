from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sha import sha
from config import *

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


if __name__ == '__main__':
    Base.metadata.create_all(engine)
