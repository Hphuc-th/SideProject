from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__="post"
    postId:Mapped[int]=mapped_column(primary_key=true)
    url:Mapped[str]=mapped_column(String(255))
    title:Mapped[str|None]=mapped_column(String(50))
    company:Mapped[str|None]=mapped_column(String(100))
    jobDescription
    jobRequirement
    JobBenefit

class Location(Base):
    __tablename__="location"
    locationId:Mapped[int]=mapped_column(primary_key=true)
    countryId:Mapped[int|None]
    cityId:Mapped[int|None]
    districtId:Mapped[int|None]

class Country(Base):
    __tablename__="country"
    countryId:Mapped[int]=mapped_column(primary_key=true)
    name:Mapped[str]=mapped_column(String(100))

class City(Base):
    __tablename__="city"
    cityId:Mapped[int]=mapped_column(primary_key=true)
    name:Mapped[str]=mapped_column(String(100))
    countryId:Mapped[int]

class District(Base):
    __tablename__="district"
    districtId:Mapped[int]=mapped_column(primary_key=true)
    name:Mapped[str]=mapped_column(String(100))
    cityId:Mapped[int]



