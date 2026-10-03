from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.product import Product
from app.models.user import User


def seed():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@flight.ru").first():
            db.add(User(
                fio="Админ Админович",
                email="admin@flight.ru",
                password=hash_password("QWEasd123"),
                role="admin",
            ))
        if not db.query(User).filter(User.email == "user@flight.ru").first():
            db.add(User(
                fio="Иванов Иван Иванович",
                email="user@flight.ru",
                password=hash_password("password"),
                role="client",
            ))
        if db.query(Product).count() == 0:
            db.add_all([
                Product(name="SU-100 Москва - Сочи",
                        description="Рейс SU-100, Вылет 12:00, Эконом класс", price=8500),
                Product(name="SU-202 Москва - Санкт-Петербург",
                        description="Рейс SU-202, Вылет 15:30, Эконом класс", price=4200),
            ])
        db.commit()
        print("Seed OK")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

