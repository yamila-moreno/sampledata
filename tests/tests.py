import unittest

import decimal
import math
import string
import datetime
import os
import io
import six
from pytz import utc

from sampledata.helper import SampleData
from sampledata.exceptions import ParameterError, NotChoicesFound
from sampledata.mixins import image_mixin


class TestNumberHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sd = SampleData(datetime.datetime.now())

    def test_int(self):
        self.assertEqual(self.sd.int(min_value=5, max_value=5), 5)

        self.assertTrue(self.sd.int(min_value=1000000000) >= 1000000000)
        self.assertTrue(self.sd.int(max_value=3) <= 3)

        self.assertTrue(isinstance(self.sd.int(), int))

        val = self.sd.int(5, 10)
        self.assertTrue(val <= 10)
        self.assertTrue(val >= 5)

        with self.assertRaises(ParameterError):
            self.sd.int(10, 5)

    def test_number(self):
        self.assertTrue(len(str(self.sd.number(5))) <= 5)

        with self.assertRaises(ParameterError):
            self.sd.number(0)

        with self.assertRaises(ParameterError):
            self.sd.number(-1)

    def test_digits(self):
        self.assertEqual(len(str(self.sd.digits(5))), 5)

        with self.assertRaises(ParameterError):
            self.sd.digits(0)

        with self.assertRaises(ParameterError):
            self.sd.digits(-1)

    def test_float(self):
        value = self.sd.float(1, 5)
        self.assertTrue(isinstance(value, float))
        self.assertTrue(value >= 1)
        self.assertTrue(value <= 5)

        self.assertEqual(self.sd.float(0, 0), 0)
        self.assertEqual(self.sd.float(5, 5), 5)
        self.assertEqual(self.sd.float(-5, -5), -5)

        with self.assertRaises(ParameterError):
            self.sd.float(10, 5)

    def test_number_string(self):
        value = self.sd.number_string(5)
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value), 5)

        self.assertEqual(self.sd.number_string(0), '')

        with self.assertRaises(ParameterError):
            self.sd.number_string(-1)

    def test_decimal(self):
        value = self.sd.decimal(5, 3)

        self.assertTrue(isinstance(value, decimal.Decimal))

        (entire, fractional) = divmod(value, 1)

        self.assertTrue(len(str(entire)) == 5)

        self.assertTrue(entire >= decimal.Decimal(10000))
        self.assertTrue(entire < decimal.Decimal(100000))

        self.assertTrue(len(str(fractional)) == 5)


class TestTextHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sd = SampleData()

    def test_char(self):
        value = self.sd.char()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertTrue(value in string.ascii_letters)

    def test_chars(self):
        value = self.sd.chars()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertTrue(len(value) >= 1)
        self.assertTrue(len(value) <= 5)

        value = self.sd.chars(5, 5)
        self.assertTrue(len(value) == 5)

        self.assertEqual(self.sd.chars(0, 0), '')

        with self.assertRaises(ParameterError):
            value = self.sd.chars(10, 5)

    def test_word(self):
        value = self.sd.word()
        self.assertTrue(isinstance(value, six.string_types))

    def test_words(self):
        value = self.sd.words()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertTrue(len(value.split(' ')) >= 1)
        self.assertTrue(len(value.split(' ')) <= 5)

        value = self.sd.words(5, 5)
        self.assertTrue(len(value.split(' ')) == 5)

        self.assertEqual(self.sd.words(0, 0), '')

        with self.assertRaises(ParameterError):
            value = self.sd.words(10, 5)

    def test_sentence(self):
        for x in range(1, 10):
            value = self.sd.sentence()
            self.assertTrue(isinstance(value, six.string_types))
            self.assertTrue(len(value) <= 255)

    def test_short_sentence(self):
        for x in range(1, 10):
            value = self.sd.short_sentence()
            self.assertTrue(isinstance(value, six.string_types))
            self.assertTrue(len(value) <= 100)

    def test_long_sentence(self):
        for x in range(1, 10):
            value = self.sd.long_sentence()
            self.assertTrue(isinstance(value, six.string_types))
            self.assertTrue(len(value) >= 150)

    def test_paragraph(self):
        value = self.sd.paragraph()
        self.assertTrue(isinstance(value, six.string_types))

    def test_paragraphs(self):
        for x in range(1, 10):
            value = self.sd.paragraphs()
            self.assertTrue(isinstance(value, six.string_types))

            self.assertTrue(len(value.split('\n\n')) >= 1)
            self.assertTrue(len(value.split('\n\n')) <= 5)

        with self.assertRaises(ParameterError):
            value = self.sd.paragraphs(5, 1)

    def test_slug(self):
        value = self.sd.slug()

        value = self.sd.slug(5, 5)
        self.assertEqual(len(value.split(' ')), 1)
        self.assertEqual(len(value.split('-')), 5)

        with self.assertRaises(ParameterError):
            value = self.sd.slug(10, 5)

    def test_tags(self):
        value = self.sd.tags()
        self.assertTrue(isinstance(value, six.string_types))

        value = self.sd.tags(5, 5)
        self.assertEqual(len(value.split(',')), 5)

        value = self.sd.tags(5, 5, ['a', 'b', 'c'])
        self.assertTrue(value.split(',')[0] in ['a', 'b', 'c'])

        with self.assertRaises(ParameterError):
            value = self.sd.tags(10, 5)


class TestTimeHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sd = SampleData()

    def test_date_between(self):
        value = self.sd.date_between(
            datetime.date(year=2000, month=1, day=1),
            datetime.date(year=2001, month=1, day=1),
        )
        self.assertTrue(isinstance(value, datetime.date))
        self.assertTrue(value > datetime.date(year=2000, month=1, day=1))
        self.assertTrue(value < datetime.date(year=2001, month=1, day=1))

        with self.assertRaises(ParameterError):
            self.sd.date_between(
                datetime.date(year=2001, month=1, day=1),
                datetime.date(year=2000, month=1, day=1),
            )

    def test_future_date(self):
        value = self.sd.future_date()
        self.assertTrue(isinstance(value, datetime.date))

        self.assertTrue(value >= datetime.date.today())
        self.assertTrue(value <= (datetime.date.today() + datetime.timedelta(days=365)))

        value = self.sd.future_date(0, 10)
        self.assertTrue(value >= datetime.date.today())
        self.assertTrue(value <= (datetime.date.today() + datetime.timedelta(days=10)))

        with self.assertRaises(ParameterError):
            self.sd.future_date(100, 0)

        with self.assertRaises(ParameterError):
            self.sd.future_date(-10, 10)

    def test_past_date(self):
        value = self.sd.past_date()
        self.assertTrue(isinstance(value, datetime.date))

        self.assertTrue(value <= datetime.date.today())
        self.assertTrue(value >= (datetime.date.today() - datetime.timedelta(days=365)))

        value = self.sd.past_date(0, 10)
        self.assertTrue(value <= datetime.date.today())
        self.assertTrue(value >= (datetime.date.today() - datetime.timedelta(days=10)))

        with self.assertRaises(ParameterError):
            self.sd.past_date(100, 0)

        with self.assertRaises(ParameterError):
            self.sd.past_date(-10, 10)

    def test_datetime_between(self):
        value = self.sd.datetime_between(
            datetime.datetime(year=2000, month=1, day=1),
            datetime.datetime(year=2001, month=1, day=1),
        )
        self.assertTrue(isinstance(value, datetime.datetime))
        self.assertTrue(value > datetime.datetime(year=2000, month=1, day=1))
        self.assertTrue(value < datetime.datetime(year=2001, month=1, day=1))

        with self.assertRaises(ParameterError):
            self.sd.datetime_between(
                datetime.datetime(year=2001, month=1, day=1),
                datetime.datetime(year=2000, month=1, day=1),
            )

    def test_future_datetime(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        value = self.sd.future_datetime()
        self.assertTrue(isinstance(value, datetime.datetime))

        self.assertTrue(value >= now)
        self.assertTrue(value <= (now + datetime.timedelta(minutes=1440)))

        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        value = self.sd.future_datetime(1, 10)
        self.assertTrue(value >= now)
        self.assertTrue(value <= (now + datetime.timedelta(minutes=10)))

        with self.assertRaises(ParameterError):
            self.sd.future_datetime(100, 0)

        with self.assertRaises(ParameterError):
            self.sd.future_datetime(-10, 10)

    def test_past_datetime(self):
        value = self.sd.past_datetime()
        self.assertTrue(isinstance(value, datetime.datetime))

        self.assertTrue(value <= datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertTrue(value >= (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=1440)))

        value = self.sd.past_datetime(0, 10)
        self.assertTrue(value <= datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertTrue(value >= (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=10)))

        with self.assertRaises(ParameterError):
            self.sd.past_datetime(100, 0)

        with self.assertRaises(ParameterError):
            self.sd.past_datetime(-10, 10)

    def test_date(self):
        value = self.sd.date()
        self.assertTrue(isinstance(value, datetime.date))

        self.assertTrue(value >= (datetime.date.today() - datetime.timedelta(days=365)))
        self.assertTrue(value <= (datetime.date.today() + datetime.timedelta(days=365)))

        value = self.sd.date(-10, 10)
        self.assertTrue(value >= (datetime.date.today() - datetime.timedelta(days=10)))
        self.assertTrue(value <= (datetime.date.today() + datetime.timedelta(days=10)))

        with self.assertRaises(ParameterError):
            self.sd.date(100, 0)

    def test_datetime(self):
        value = self.sd.datetime()
        self.assertTrue(isinstance(value, datetime.datetime))

        self.assertTrue(value >= (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=1440)))
        self.assertTrue(value <= (datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(minutes=1440)))

        value = self.sd.datetime(-10, 10)
        self.assertTrue(value >= (datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(minutes=10)))
        self.assertTrue(value <= (datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(minutes=10)))

        with self.assertRaises(ParameterError):
            self.sd.datetime(100, 0)

    def test_time(self):
        value = self.sd.time()
        self.assertTrue(isinstance(value, datetime.time))


class TestLocalizedHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sd = SampleData()

    def test_state_code(self):
        value = self.sd.state_code('es')
        self.assertTrue(value in ['01', '02', '03', '04', '05', '06', '07',
                                  '08', '09', '10', '11', '12', '13', '14',
                                  '15', '16', '17', '18', '19', '20', '21',
                                  '22', '23', '24', '25', '26', '27', '28',
                                  '29', '30', '31', '32', '33', '34', '35',
                                  '36', '37', '38', '39', '40', '41', '42',
                                  '43', '44', '45', '46', '47', '48', '49',
                                  '50', '51', '52', 'AD', ])

        value = self.sd.state_code('us')
        self.assertTrue(value in ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT',
                                  'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN',
                                  'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                                  'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                                  'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH',
                                  'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN',
                                  'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
                                  'WY', 'AS', 'DC', 'FM', 'GU', 'MH', 'MP',
                                  'PW', 'PR', 'VI', ])

        with self.assertRaises(ParameterError):
            self.sd.state_code('invalid-code')

    def test_name(self):
        value = self.sd.name()
        self.assertTrue(isinstance(value, six.string_types))

        value = self.sd.name(as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        value = self.sd.name(number=3, as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 3)

        value = self.sd.name(locale='es', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        value = self.sd.name(locale='cat', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        value = self.sd.name(locale='fr', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        value = self.sd.name(locale='us', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        with self.assertRaises(ParameterError):
            value = self.sd.name(number=0)

        with self.assertRaises(ParameterError):
            value = self.sd.name(number=-1)

        with self.assertRaises(ParameterError):
            value = self.sd.name(locale="not-valid-locale")

    def test_surname(self):
        value = self.sd.surname()
        self.assertTrue(isinstance(value, six.string_types))

        value = self.sd.surname(as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        value = self.sd.surname(number=3, as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 3)

        value = self.sd.surname(locale='es', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)

        value = self.sd.surname(locale='cat', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)

        value = self.sd.surname(locale='fr', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        value = self.sd.surname(locale='us', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 1)

        with self.assertRaises(ParameterError):
            value = self.sd.surname(number=0)

        with self.assertRaises(ParameterError):
            value = self.sd.surname(number=-1)

        with self.assertRaises(ParameterError):
            value = self.sd.surname(locale="not-valid-locale")

    def test_fullname(self):
        value = self.sd.fullname()
        self.assertTrue(isinstance(value, six.string_types))

        value = self.sd.fullname(as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)

        value = self.sd.fullname(locale='es', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 3)

        value = self.sd.fullname(locale='cat', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 3)

        value = self.sd.fullname(locale='fr', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)

        value = self.sd.fullname(locale='us', as_list=True)
        self.assertTrue(isinstance(value, list))
        self.assertEqual(len(value), 2)

        with self.assertRaises(ParameterError):
            value = self.sd.fullname(locale="not-valid-locale")

    def test_phone(self):
        value = self.sd.phone(locale='es')
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value), 9)
        self.assertTrue(value[0] in ['6', '9'])

        value = self.sd.phone(locale='es', country_code=True)
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value), 13)
        self.assertTrue(value[0:5] in ['+34 6', '+34 9'])

        with self.assertRaises(ParameterError):
            value = self.sd.phone(locale="not-valid-locale")

    def test_zip_code(self):
        value = self.sd.zip_code(locale='es')
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value), 5)

        with self.assertRaises(ParameterError):
            value = self.sd.zip_code(locale="not-valid-locale")

    def test_id_card(self):
        value = self.sd.id_card(locale='es')
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value), 9)
        self.assertTrue(value[8] in "TRWAGMYFPDXBNJZSQVHLCKET")

        with self.assertRaises(ParameterError):
            value = self.sd.id_card(locale="not-valid-locale")


class TestImageHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sd = SampleData()

    def test_image_path_from_directory(self):
        value = self.sd.image_path_from_directory(os.path.dirname(__file__))
        self.assertTrue(isinstance(value, six.string_types))

        with self.assertRaises(ParameterError):
            self.sd.image_path_from_directory('not-existing-directory')

        with self.assertRaises(NotChoicesFound):
            self.sd.image_path_from_directory(os.path.dirname(__file__), ['.not-valid-extension'])

    def test_image_stream(self):
        value = self.sd.image_stream(100, 100)
        self.assertTrue(isinstance(value, io.BytesIO))

        value = self.sd.image_stream(100, 100, typ="simple")
        self.assertTrue(isinstance(value, io.BytesIO))

        value = self.sd.image_stream(100, 100, typ="plasma")
        self.assertTrue(isinstance(value, io.BytesIO))

        value = self.sd.image_stream(100, 100, typ="mandelbrot")
        self.assertTrue(isinstance(value, io.BytesIO))

        value = self.sd.image_stream(100, 100, typ="ifs")
        self.assertTrue(isinstance(value, io.BytesIO))

        value = self.sd.image_stream(100, 100, typ="random")
        self.assertTrue(isinstance(value, io.BytesIO))

        image_mixin.PIL_INSTALLED = False
        with self.assertRaises(ImportError):
            value = self.sd.image_stream(100, 100, typ="random")
        image_mixin.PIL_INSTALLED = True

        with self.assertRaises(ParameterError):
            value = self.sd.image_stream(100, 100, typ="not-valid-type")

        with self.assertRaises(ParameterError):
            value = self.sd.image_stream(0, 100)

        with self.assertRaises(ParameterError):
            value = self.sd.image_stream(100, 0)


class TestOtherHelpers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sd = SampleData()

    def test_boolean(self):
        self.assertTrue(isinstance(self.sd.boolean(), bool))

    def test_ipv4(self):
        value = self.sd.ipv4()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value.split('.')), 4)

    def test_ipv6(self):
        value = self.sd.ipv6()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value.split(':')), 8)

    def test_mac_address(self):
        value = self.sd.mac_address()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertEqual(len(value.split(':')), 6)

    def test_path(self):
        value = self.sd.path()
        self.assertTrue(isinstance(value, six.string_types))

        value = self.sd.path(absolute=False, min_levels=5, max_levels=5)
        self.assertEqual(len(value.split('/')), 5)

        value = self.sd.path(absolute=True, min_levels=5, max_levels=5)
        self.assertEqual(len(value.split('/')), 6)

        value = self.sd.path(extension=".jpg")
        self.assertEqual(value[-4:], ".jpg")

        with self.assertRaises(ParameterError):
            self.sd.path(absolute=True, min_levels=10, max_levels=5)

    def test_hex_chars(self):
        value = self.sd.hex_chars()
        self.assertTrue(isinstance(value, six.string_types))
        self.assertTrue(len(value) >= 1)
        self.assertTrue(len(value) <= 5)

        value = self.sd.hex_chars(5, 5)
        self.assertTrue(len(value) == 5)

        self.assertEqual(self.sd.hex_chars(0, 0), '')

        with self.assertRaises(ParameterError):
            value = self.sd.hex_chars(10, 5)

    def test_choice(self):
        self.assertEqual(self.sd.choice([10]), 10)

        with self.assertRaises(ParameterError):
            self.sd.choice([])

        with self.assertRaises(ParameterError):
            self.sd.choice(7)
