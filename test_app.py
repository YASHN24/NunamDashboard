import unittest
import requests


class TestAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:5000/api/data'
    AUTH = ('yash', '7388957687')  # Authentication credentials

    def test_get_data(self):
        cell_id = '5308'
        sheet_name = 'Cycle_67_3_5'
        response = requests.get(f'{self.BASE_URL}/{cell_id}/{sheet_name}', auth=self.AUTH)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access(self):
        cell_id = '5308'
        sheet_name = 'Cycle_67_3_5'
        response = requests.get(f'{self.BASE_URL}/{cell_id}/{sheet_name}')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        self.assertEqual(response.status_code, 401)

    def test_invalid_endpoint(self):
        cell_id = '5308'
        sheet_name = 'InvalidSheet'
        response = requests.get(f'{self.BASE_URL}/{cell_id}/{sheet_name}', auth=self.AUTH)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        self.assertEqual(response.status_code, 404)

    def test_pagination(self):
        cell_id = '5308'
        sheet_name = 'Cycle_67_3_5'
        response = requests.get(f'{self.BASE_URL}/{cell_id}/{sheet_name}?page=1&per_page=5', auth=self.AUTH)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in response.json())
        self.assertTrue(len(response.json()['data']) <= 5)

    def test_multiple_sheets(self):
        datasets = {
            '5308': ['Cycle_67_3_5', 'Detail_67_3_5', 'Statis_67_3_5', 'DetailVol_67_3_5', 'DetailTemp_67_3_5'],
            '5329': ['Cycle_67_3_1', 'Detail_67_3_1', 'Statis_67_3_1', 'DetailVol_67_3_1', 'DetailTemp_67_3_1']
        }
        for dataset, sheets in datasets.items():
            for sheet in sheets:
                response = requests.get(f'{self.BASE_URL}/{dataset}/{sheet}', auth=self.AUTH)
                print(f"Response for {dataset}/{sheet}:")
                print(f"Status code: {response.status_code}")
                print(f"Content: {response.text}")
                self.assertEqual(response.status_code, 200)
                # Additional assertions can be added here


if __name__ == '__main__':
    unittest.main()
