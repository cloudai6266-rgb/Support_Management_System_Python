
from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String, nullable=False)

    phone = Column(String, nullable=True)

    email = Column(String, nullable=True)

    address = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<Customer(id={self.id}, "
            f"name='{self.name}', "
            f"email='{self.email}')>"
        )
