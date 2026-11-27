from sqlalchemy import Column, Integer, String, DateTime, Text

from app.database.base import Base


class User(Base):

    __tablename__ = "users"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    # User Name
    name = Column(
        String(100),
        nullable=False
    )

    # User Type
    user_type = Column(
        String(20),
        nullable=False
    )

    # Country Code
    country_code = Column(
        String(5),
        nullable=True,
        default="+91"
    )

    # Phone Number
    phone = Column(
        String(10),
        nullable=False
    )

    # Email Address
    email = Column(
        String(150),
        nullable=False,
        unique=True
    )

    # Registration Date and Time
    registered_at = Column(
        DateTime,
        nullable=True
    )

    # Technologies
    technologies = Column(
        Text,
        nullable=True
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name='{self.name}', "
            f"email='{self.email}')>"
        )
