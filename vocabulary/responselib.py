import json

__version__ = '0.0.1'
__author__ = "Chizzy Alaedu"


class Response(object):
    """
    |  Private methods       | Public methods   |
    |:----------------------:|------------------|
    | __respond_with_dict()  | respond()        |
    | __respond_with_list()  |                  |
    |                        |                  |
    """

    def __respond_with_dict(self, data):
        """
        Builds a python dictionary from a json object

        :param data: the json object
        :returns: a nested dictionary
        """
        response = {}
        if isinstance(data, list):
            temp_data, data = data, {}
            for key, value in enumerate(temp_data):
                data[key] = value

        data.pop('seq', None)
        for index, item in data.items():
            values = item
            if isinstance(item, list) or isinstance(item, dict):
                values = self.__respond_with_dict(item)

            if isinstance(values, dict) and len(values) == 1:
                (key, values), = values.items()
            response[index] = values

        return response

    def __respond_with_list(self, data):
        """
        Builds a python list from a json object

        :param data: the json object
        :returns: a nested list
        """
        response = []
        if isinstance(data, dict):
            data.pop('seq', None)
            data = list(data.values())

        for item in data:
            values = item
            if isinstance(item, list) or isinstance(item, dict):
                values = self.__respond_with_list(item)

            if isinstance(values, list) and len(values) == 1:
                response.extend(values)
            else:
                response.append(values)

        return response

    def respond(self, data, format='json'):
        """
        Converts a json object to a python datastructure based on
        specified format

        :param data: the json object
        :param format: python datastructure type. Defaults to: "json"
        :returns: a python specified object
        """
        dispatchers = {
            "dict": self.__respond_with_dict,
            "list": self.__respond_with_list
        }

        if not dispatchers.get(format, False):
            return json.dumps(data)

        return dispatchers[format](data)
