import unittest

class DeliveryCalculator:
    """
    Класс для расчета стоимости доставки.
    """
    def __init__(self, distance: float, size: str, is_fragile: bool, load_level: str):
        self.cost = 0
        self.distance = distance
        self.size = size
        self.is_fragile = is_fragile
        self.load_level = load_level
        self.multiplier = 1

    def _calculate_distance_supplement(self):
        if self.distance > 30:
            self.cost += 300
        elif self.distance > 10:
            self.cost += 200
        elif self.distance > 2:
            self.cost += 100
        elif self.distance > 0 and self.distance <= 2:
            self.cost += 50
        else:
            raise ValueError('Некорректное значение расстояния.')

    def _calculate_size_supplement(self):
        if self.size == 'большие':
            self.cost += 200
        elif self.size == 'маленькие':
            self.cost += 100
        else:
            raise ValueError("Неизвестные габариты. Используйте 'большие' или 'маленькие'.")

    def _calculate_fragile_supplement(self):
        if self.is_fragile:
            if self.distance > 30:
                raise ValueError("Ошибка: Хрупкие грузы нельзя перевозить на расстояние более 30 км.")
            else:
                self.cost += 300
    
    def _calculate_multiplier(self):
        if self.load_level == 'очень высокая':
            self.multiplier = 1.6
        elif self.load_level == 'высокая':
            self.multiplier = 1.4
        elif self.load_level == 'повышенная':
            self.multiplier = 1.2
        else:
            self.multiplier = 1

    def calculate_delivery_cost(self):
        self._calculate_distance_supplement()
        self._calculate_size_supplement()
        self._calculate_fragile_supplement()

        total_cost = int(self.cost * self.multiplier)

        if total_cost < 400:
            total_cost = 400

        return total_cost


class TestDeliveryCalculator(unittest.TestCase):

    def test_small_distance_small_size_not_fragile_low_load(self):
        calc = DeliveryCalculator(1, 'маленькие', False, 'норма')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_medium_distance_big_size_not_fragile_high_load(self):
        calc = DeliveryCalculator(15, 'большие', False, 'высокая')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_long_distance_small_size_not_fragile_very_high_load(self):
        calc = DeliveryCalculator(35, 'маленькие', False, 'очень высокая')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_short_distance_small_size_not_fragile_normal_load(self):
        calc = DeliveryCalculator(1, 'маленькие', False, 'норма')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_fragile_within_limit(self):
        calc = DeliveryCalculator(29, 'маленькие', True, 'норма')
        self.assertEqual(calc.calculate_delivery_cost(), 600)

    def test_fragile_over_limit(self):
        with self.assertRaises(ValueError):
            calc = DeliveryCalculator(31, 'маленькие', True, 'норма')
            calc.calculate_delivery_cost()

    def test_min_cost_applied(self):
        calc = DeliveryCalculator(1, 'маленькие', False, 'норма')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            calc = DeliveryCalculator(10, 'средние', False, 'норма')
            calc.calculate_delivery_cost()

    def test_fragile_with_high_multiplier(self):
        calc = DeliveryCalculator(10, 'большие', True, 'очень высокая')
        self.assertEqual(calc.calculate_delivery_cost(), 600)

    def test_fragile_with_small_multiplier(self):
        calc = DeliveryCalculator(10, 'маленькие', True, 'норма')
        self.assertEqual(calc.calculate_delivery_cost(), 500)

class TestDeliveryCalculatorExtended(unittest.TestCase):

    def test_distance_less_than_2_km(self):
        calc = DeliveryCalculator(1.9, 'маленькие', False, 'другое')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_distance_equal_to_2_km(self):
        calc = DeliveryCalculator(2, 'маленькие', False, 'другое')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_distance_equal_to_10_km(self):
        calc = DeliveryCalculator(10, 'маленькие', False, 'другое')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_distance_equal_to_30_km(self):
        calc = DeliveryCalculator(30, 'маленькие', False, 'другое')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_medium_distance_with_normal_load(self):
        calc = DeliveryCalculator(25, 'маленькие', False, 'другое')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_high_multiplier_with_fragile_and_big_size(self):
        calc = DeliveryCalculator(20, 'большие', True, 'очень высокая')
        self.assertEqual(calc.calculate_delivery_cost(), 700)

    def test_exact_min_cost_boundary(self):
        calc = DeliveryCalculator(1, 'маленькие', False, 'другое')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_min_cost_applied_with_high_multiplier(self):
        calc = DeliveryCalculator(1, 'маленькие', False, 'очень высокая')
        self.assertEqual(calc.calculate_delivery_cost(), 400)

    def test_negative_distance(self):
        with self.assertRaises(ValueError):
            calc = DeliveryCalculator(-10, 'маленькие', False, 'другое')
            calc.calculate_delivery_cost()

    def test_zero_distance(self):
        with self.assertRaises(ValueError):
            calc = DeliveryCalculator(0, 'маленькие', False, 'другое')
            calc.calculate_delivery_cost()      

    def test_unknown_load_level(self):
        calc = DeliveryCalculator(10, 'маленькие', False, 'неизвестная загруженность')
        self.assertEqual(calc.calculate_delivery_cost(), 400)


if __name__ == '__main__':
    unittest.main()
