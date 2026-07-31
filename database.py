from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine(
    "sqlite:///translations.db"
)

Base = declarative_base()


class TranslationHistory(Base):

    __tablename__ = "history"

    id = Column(Integer, primary_key=True)

    source_text = Column(String)

    translated_text = Column(String)

    language_pair = Column(String)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)


def save_translation(source, target, pair):

    db = Session()

    record = TranslationHistory(
        source_text=source,
        translated_text=target,
        language_pair=pair
    )

    db.add(record)

    db.commit()

    db.close()



def get_history():

    db = Session()

    data = db.query(
        TranslationHistory
    ).all()

    db.close()

    return data



def clear_history():

    db = Session()

    db.query(
        TranslationHistory
    ).delete()

    db.commit()

    db.close()