from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    win_rate = Column(Float, nullable=True)
    total_trades = Column(Integer, nullable=True)
    pnl = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
