"""
Weather_api_class.py written by Henry Chacon (henrychacon@gmail.com)

Purpose:
Gathering weather information from the API: https://openweathermap.org
It is divided in two classes. In the first the city information such as: CITY ID, Name and Location is downloaded from the server.
The second one, the weather information available for the free account is downloaded. To use all the methods implemented in this class,
a valid API-KEY should be used during the class instantiation. That key is provided by the API after registration.

Special libraries:
None

Notes:
Not any special notes
"""


import json
import pandas as pd
import re
import numpy as np
import os
import requests
import wget
import gzip
import io


class CitiesInformation:
    """
    Class defined to download the ID, Country and location of all cities included in the Weather API data base. That list
    is included in the city.list.json.gz file posted in the server. The file is downloaded and unziped to get the information
    """
    def __init__(self):
        # Checking if the city file list form the server is included in the folder ./city_list
        try:
            if not os.path.isfile('./city_list/city.list.json'):
                print('Downloading the cities data file, please wait...')
                os.makedirs('./city_list', exist_ok=True)
                wget.download('http://bulk.openweathermap.org/sample/city.list.json.gz', './city_list/city.list.json.gz')
                fout = open('./city_list/city.list.json', 'w')
                with gzip.open('./city_list/city.list.json.gz', 'rb') as input_file:
                    with io.TextIOWrapper(input_file, encoding='utf-8') as dec:
                        # print(dec.read())
                        fout.write(dec.read())
                fout.close()
                print('\t**Process completed.')

            # Opening the cities file for analysis
            with open('./city_list/city.list.json') as data_file:
                cities_info_json = json.load(data_file)

            self.cities = pd.DataFrame(cities_info_json)
            self.cities.columns = ['city_coordinates', 'city_country', 'city_id', 'city_name']
            print("City's name and location for {} places were downloaded".format(len(self.cities)))
        except ValueError as e:
            print("Downloading cities' file has failed..., error: ", e)

    def __str__(self):
        return 'Total number of cities in the API: {}'.format(len(self.cities))

    def country_list(self):
        """
        :return: It returns the list of all countries ID's included in the source file
        """
        return self.cities['city_country'].sort_values().unique()

    def select_city_information(self, label_name, country=''):
        """
        :param label_name: any label used to identify the city. Caps is ignore
        :param country: Two capital letters define in the database to identify the country. The function country_list
        can be used to get all the possible values
        :return: a Dataframe with the list of all cities that satisfy the input label used as input
        """
        r = re.compile(label_name, re.IGNORECASE)
        regmatch = np.vectorize(lambda x: bool(r.match(x)))
        temp_cities = self.cities[regmatch(self.cities['city_name'])]
        if country == '':
            return temp_cities
        else:
            return temp_cities[temp_cities['city_country'] == country]


class OpenWeatherApi:
    """
    Class defined to download all the data available in the free account.
    Query list contains all the queries available per category. It is recommended to update those values in case of
    upcoming actualization in the API server over those.
    The data parameters follow the structure:
        'Query name': ["Query root, where {PARAM1} is the first parameter", "string addition if more than parameter is included"]
        IMPORTANT: Each PARAM label MUST be included in braces to identify the parameter
    """

    def query_list(self, query_id):
        LIST_CURRENT_WEATHER = {'by_city_name':     ["api.openweathermap.org/data/2.5/weather?q={PARAM1}", ",{PARAM2}"],
                                'by_city_ID':       ["api.openweathermap.org/data/2.5/weather?id={PARAM1}"],
                                'by_geog_coord':    ["api.openweathermap.org/data/2.5/weather?lat={PARAM1}&lon={PARAM2}"],
                                'by_zip_code':      ["api.openweathermap.org/data/2.5/weather?zip={PARAM1}", ",{PARAM2}"],
                                'by_circle':        ["http://api.openweathermap.org/data/2.5/find?lat={PARAM1}&lon={PARAM2}&cnt={PARAM3}"]}

        LIST_5_DAYS_FORCASTS = {'by_city_name':     ["api.openweathermap.org/data/2.5/forecast?q={PARAM1}", ",{PARAM2}"],
                                'by_city_ID':       ["api.openweathermap.org/data/2.5/forecast?id={PARAM1}"],
                                'by_geog_coord':    ["api.openweathermap.org/data/2.5/forecast?lat={PARAM1}&lon={PARAM2}"],
                                'by_zip_code':      ["api.openweathermap.org/data/2.5/forecast?zip={PARAM1}", ",{PARAM2}"]}

        LIST_UV_INDEX = {'for_one_location':        ["api.openweathermap.org/data/2.5/uvi?lat={PARAM1}&lon={PARAM2}"],
                         'forecast_one_location':   ["api.openweathermap.org/data/2.5/uvi/forecast?lat={PARAM1}&lon={PARAM2}&cnt={PARAM3}"],
                         'hystorical_uv_location':  ["api.openweathermap.org/data/2.5/uvi/history?lat={PARAM1}&lon={PARAM2}&cnt={PARAM3}&start={PARAM4}&end={PARAM5}"]}

        if query_id == 0:
            return LIST_CURRENT_WEATHER
        elif query_id == 1:
            return LIST_5_DAYS_FORCASTS
        elif query_id == 2:
            return LIST_UV_INDEX
        else:
            return {'-1': "No valid query ID"}

    def __init__(self, api_key):
        self.api_key = api_key

    def query_preprocessing(self, query_type, query_name, parameters):
        """
        Function defined to return the desired query updated with the list of parameters.
        :param query_type: Integer value that represents the family of queries to be executed.
            0: Current weather queries
            1: 5 days forecast
            2: UV index
        :param query_name: Name of the query as it was defined in the LIST_QUERY to be executed
        :param parameters: List with the set of parameters to be included in the query
        :return: a string with the query replacing the param label with the values included in the parameter list
        """
        query = ""
        query_list_values = self.query_list(query_id=query_type)
        if "-1" in query_list_values:
            print("Not a valid list ID was entered")
            return {'error': -1}
        else:
            if query_name in query_list_values:
                list_qnr = query_list_values[query_name]
                num_param = len(re.findall("PARAM\d", list_qnr[0]))
                if num_param > len(parameters):
                    return "Number of parameters: {}, required by the query: {}. Update the list of parameters".format(len(parameters), num_param)
                query = list_qnr[0]

                # Bucle to update the list of parameters for the query
                for i in range(num_param):
                    cad = "{PARAM" + str(i + 1) + "}"
                    query = re.sub(cad, str(parameters[i]), query)

                # Bucle to add the optional set of parameters in the query
                j = 1
                for i in range(num_param, len(parameters)):
                    if j < len(list_qnr):
                        cad = "{PARAM" + str(i + 1) + "}"
                        query = query + re.sub(cad, str(parameters[i]), list_qnr[j])
                        j += 1
                return query
            else:
                print("No valid query was entered")
                return {'error': -1}

    def query_execution(self, query_type, query_name, parameters):
        """
         Function implemented to execute queries in the API database
        :param query_type: Integer value that represents the family of queries to be executed.
            0: Current weather queries
            1: 5 days forecast
            2: UV index
        :param query_name: Name of the query as it was defined in the LIST_QUERY to be executed
        :param parameters: List with the set of parameters to be included in the query
        :return: a dictionary with the query output
        """
        query = self.query_preprocessing(query_type, query_name, parameters)
        if 'error' in query:
            return {'error': -1}
        else:
            url = "https://" + query + '&appid=' + self.api_key
            api_request = requests.get(url)
            if api_request.status_code != 200:
                print("Not possible to execute the query. Error reported by the API: {}, {}".format(api_request.json()['message'], api_request.json()['cod']))
                return {'error': -1}
            else:
                return api_request.json()


# Examples:
# cities_info = CitiesInformation()
# print(cities_info)
# cities_info.country_list()
# cities_name = cities_info.select_city_information('Houst')
# cities_name[['city_country', 'city_name', 'city_id', 'city_coordinates']]
#
#
# query_class = OpenWeatherApi(api_key)
# query_class.query_preprocessing(1, "by_city_name", ["London"])
# query_class.query_execution(0, 'by_city_ID', [4699066])
# query_class.query_execution(1, 'by_city_name', ["San Antonio", "US"])
# query_class.query_preprocessing(2, 'by_city_name', ["London"])
