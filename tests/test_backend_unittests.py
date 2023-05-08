
import unittest

class TestAggregate(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_belgium(self):
        from utils import get_belgium
        BE = get_belgium()
        self.assertEqual(len(BE), 12)

    def test_dynamodb_query1(self):
        from utils import run_dynamo_query
        response = run_dynamo_query('co', 0)
        self.assertEqual(len(response["Items"]), 0)

    def test_aggregations(self):
        from decimal import Decimal
        from utils import aggregate_response
        items = [{'parameter': 'pm10',
          'unit': 'µg/m³',
          'location': 'BETN067',
          'sourceName': 'EEA Belgium',
          'country': 'BE',
          'city': 'Liege',
          'date_utc': '2023-05-07T01:00:00.000Z',
          'epoch': Decimal('1683428400'),
          'value': '6.771',
          'sourceType': 'government',
          'longitude': '5.99275271918705',
          'parameter_location': 'pm10_BETN067',
          'date_local': '2023-05-07T03:00:00+02:00',
          'latitude': '50.6122775285323'},
         {'parameter': 'pm10',
          'unit': 'µg/m³',
          'location': 'BETN067',
          'sourceName': 'EEA Belgium',
          'country': 'BE',
          'city': 'Liege',
          'date_utc': '2023-05-07T02:00:00.000Z',
          'epoch': Decimal('1683432000'),
          'value': '6.271',
          'sourceType': 'government',
          'longitude': '5.99275271918705',
          'parameter_location': 'pm10_BETN067',
          'date_local': '2023-05-07T04:00:00+02:00',
          'latitude': '50.6122775285323'},
         {'parameter': 'pm10',
          'unit': 'µg/m³',
          'location': 'BETN067',
          'sourceName': 'EEA Belgium',
          'country': 'BE',
          'city': 'Liege',
          'date_utc': '2023-05-08T01:00:00.000Z',
          'epoch': Decimal('1683514800'),
          'value': '18.771',
          'sourceType': 'government',
          'longitude': '5.99275271918705',
          'parameter_location': 'pm10_BETN067',
          'date_local': '2023-05-08T03:00:00+02:00',
          'latitude': '50.6122775285323'}]
        response = {"Items":items}
        result_test = aggregate_response(response)
        result = ({'pm10_BETN067': {'longitude': 5.99275271918705,
           'latitude': 50.6122775285323,
           'values': [6.771, 6.271, 18.771],
           'avg': 10.604333333333335}},
         {'unit': 'µg/m³', 'n': 3})
        self.assertEqual(result, result_test)




if __name__ == '__main__':
    unittest.main()
