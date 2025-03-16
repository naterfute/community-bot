from sqlalchemy import BigInteger, ForeignKey, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class ServerSettings(Base):
    __tablename__ = "guildSettings"

    guildID = Column(BigInteger, primary_key=True, unique=True)
    serverJoin = Column(Integer, autoincrement=True)
    ownerID = Column(BigInteger)
    userAmount = Column(Integer)
    economy = Column(Integer)  # NOTE: How much money is in the economy currently
    economyLeft = Column(Integer)  # NOTE: How much money is left in the public bank
    inflation = Column(Integer) # NOTE: Current market inflation value
    lotterypot = Column(Integer)  # NOTE: How much money has been burned or "Defaced"


    views = relationship("Views", back_populates="server")

class StorePages(Base):
    __tablename__ = "storePages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guildID = Column(BigInteger, ForeignKey(f"{ServerSettings.__tablename__}.guildID"))
    storeName = Column(String)
    storeLink = Column(String)
    description = Column(String)


    server = relationship("ServerSettings", back_populates="views")

class Views(Base):
    __tablename__ = "arcViews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    viewID = Column(BigInteger)
    guildID = Column(BigInteger, ForeignKey(f"{ServerSettings.__tablename__}.guildID"))

    server = relationship("ServerSettings", back_populates="views")


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(BigInteger, unique=True)
    balance = Column(Integer)
    messagesSent = Column(Integer)  # NOTE: Ballpark Estimation of How many messages have been sent by this user (Not 100% accurate)
    warnings = Column(Integer) # NOTE: How many times this user has been warned

    economy = relationship("Economy", back_populates="user")
    levels = relationship("Levels", back_populates="user")


class Levels(Base):  # NOTE: This wasn't asked for, I just like level systems, and it's a game engine. so it makes sense
    __tablename__ = "Levels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(BigInteger, ForeignKey("Users.uid"), unique=True)  # NOTE: This is the id of the discord user
    exp = Column(Integer)

    user = relationship("Users", back_populates="levels")

