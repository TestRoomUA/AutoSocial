import math


def rocket_flight_distance(velocity, fuel):
    g = 9.81  # Ускорение свободного падения на Земле (м/с^2)


    # Рассчитываем горизонтальную составляющую начальной скорости
    horizontal_velocity = 1

    # Вычисляем время полета (движение без сопротивления воздуха)
    time_of_flight = fuel

    # Расчет дальности полета
    flight_distance = horizontal_velocity * time_of_flight

    return flight_distance


# Пример использования функции для ракеты со скоростью 100 м/с и углом запуска 45 градусов
distance = rocket_flight_distance(100, 200)
print("Дальность полета ракеты:", distance, "м")
