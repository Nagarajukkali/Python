import pytest
import requests
import yaml
from yaml import SafeLoader
import os
#import requests_mock

import logging

logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# print(ROOT_DIR)
config_file = os.path.join(ROOT_DIR, "config.yaml")
endpoint = "http://mock.com/api/json/v1/1/random.php"
mocked_server = True


@pytest.fixture(scope='session')
def get_data():
    global endpoint
    global mocked_server
    with open(config_file, 'r') as f:
        data = yaml.load(f, Loader=SafeLoader)
    if not data.get('server').get('mock').get('enabled'):
        endpoint = data.get('server').get('real').get('url')
        mocked_server = False


class TestMeals:
    def get_call(self, endpoint, payload={}, headers={}):
        url = 'https://www.themealdb.com/api/json/v1/1/random.php'
        response = requests.request("GET", endpoint, headers=headers, data=payload, verify=False)
        if response.status_code != 200:
            logger.error("response is not 200 for endpoint {} ,  ".format(endpoint), response)
            return None
        return response.json()


def test_get_call(get_data):
    if mocked_server:
        with requests_mock.Mocker() as m:
            m.get("http://mock.com/api/json/v1/1/random.php", json={"meals": [
                {"idMeal": "52966", "strMeal": "Chocolate Caramel Crispy", "strDrinkAlternate": "null",
                 "strCategory": "Dessert", "strArea": "British",
                 "strInstructions": "Grease and line a 20 x 20cm\/8\" x 8\" baking tin with parchment paper.\r\nPut the mars bars and butter in a heat proof bowl and place over a pan of barely simmering water. Mixing with a whisk, melt until the mixture is smooth.\r\nPour over the rice krispies in a mixing bowl and mix until all the ingredients are evenly combined. Press evenly into the prepare baking tin and set aside.\r\nMelt the milk chocolate in the microwave or over a pan of barely simmering water.\r\nSpread the melted chocolate over the rice krispie mixture and leave to set in a cool place. Once set slice into squares and serve!",
                 "strMealThumb": "https:\/\/www.themealdb.com\/images\/media\/meals\/1550442508.jpg",
                 "strTags": "Sweet,Snack,Treat,Tart,Alcoholic,BBQ",
                 "strYoutube": "https:\/\/www.youtube.com\/watch?v=qsk_At_gjv0", "strIngredient1": "Mars Bar",
                 "strIngredient2": "Butter", "strIngredient3": "Rice Krispies", "strIngredient4": "Milk Chocolate",
                 "strIngredient5": "", "strIngredient6": "", "strIngredient7": "", "strIngredient8": "",
                 "strIngredient9": "", "strIngredient10": "", "strIngredient11": "", "strIngredient12": "",
                 "strIngredient13": "", "strIngredient14": "", "strIngredient15": "", "strIngredient16": "",
                 "strIngredient17": "", "strIngredient18": "", "strIngredient19": "", "strIngredient20": "",
                 "strMeasure1": "6 chopped", "strMeasure2": "150g", "strMeasure3": "120g", "strMeasure4": "150g",
                 "strMeasure5": " ", "strMeasure6": " ", "strMeasure7": " ", "strMeasure8": " ", "strMeasure9": " ",
                 "strMeasure10": " ", "strMeasure11": " ", "strMeasure12": " ", "strMeasure13": " ",
                 "strMeasure14": " ", "strMeasure15": " ", "strMeasure16": " ", "strMeasure17": " ",
                 "strMeasure18": " ", "strMeasure19": " ", "strMeasure20": " ",
                 "strSource": "http:\/\/www.donalskehan.com\/recipes\/chocolate-caramel-rice-crispy-treats\/",
                 "strImageSource": "null", "strCreativeCommonsConfirmed": "null", "dateModified": "null"}]})
            testmeals = TestMeals()
            for i in range(0,10):
                response = testmeals.get_call(endpoint)
                for meal in response['meals']:
                    for ing_range in range(1,21):
                        ingredient = meal['strIngredient{}'.format(ing_range)]
                        assert 'garlic' not in ingredient.lower()

    else:
        testmeals = TestMeals()
        for i in range(0, 10):
            response = testmeals.get_call(endpoint)
            print(response)
            for meal in response['meals']:
                for ing_range in range(1, 21):
                    ingredient = meal['strIngredient{}'.format(ing_range)]
                    assert 'garlic' not in ingredient.lower()

# if __name__ == '__main__':
#     obj = TestMeals()
#     r = obj.get_call('https://www.themealdb.com/api/json/v1/1/random.php')
#     print(r)
