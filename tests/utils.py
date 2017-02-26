import pytest

from lib.utils import number_to_text, MAX_NUMBER


class NumberToTextTest:

    def test_number_zero(self):
        number_zero = number_to_text(0)
        assert 'cero' == number_zero

    def test_number_one(self):
        number_one = number_to_text(1)
        assert 'un' == number_one

    def test_number_nine(self):
        number_nine = number_to_text(9)
        assert 'nueve' == number_nine

    def test_max_number(self):
        number_to_text(MAX_NUMBER)
        assert True  # if no number_to_text fails, `assert True` will be never achieved

    def test_number_greater_than_max_number(self):
        with pytest.raises(ValueError):
            number_to_text(MAX_NUMBER + 1)
