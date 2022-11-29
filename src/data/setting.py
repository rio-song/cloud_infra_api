from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base

# 接続先DBの設定
DATABASE = 'postgresql://postgres:*pwd*@localhost:5432/cloud_infra'

# Engine の作成
Engine = create_engine(
  DATABASE,
  encoding="utf-8",
  echo=True
)
Base = declarative_base()

# Sessionの作成
session = Session(
  autocommit = False,
  autoflush = True,
  bind = Engine
)
# modelで使用する
Base = declarative_base()

