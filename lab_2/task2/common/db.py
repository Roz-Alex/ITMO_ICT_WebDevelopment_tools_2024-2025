from lab_2.task2.common.connection import get_session
from lab_2.task2.common.models import Car


def save_car(car_data: dict):
    with next(get_session()) as session:
        car = Car(
            name=car_data["name"],
            year=car_data["year"],
            mileage=car_data["mileage"],
            price=car_data["price"],
            specs=car_data["specs"],
        )
        session.add(car)
        session.commit()
        session.refresh(car)
