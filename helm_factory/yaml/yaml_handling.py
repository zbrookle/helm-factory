from copy import deepcopy
from typing import Union

from yaml import dump


class HelmYaml:
    def __clean_nested(self, dictionary_or_list: Union[dict, list]):
        if isinstance(dictionary_or_list, list):
            cleaned_list = []
            for value in dictionary_or_list:
                # If value is None, [], {}, '' do not include value
                if not value:
                    continue

                if isinstance(value, (dict, list)):
                    cleaned_dict_or_list = self.__clean_nested(value)

                    if cleaned_dict_or_list:
                        cleaned_list.append(self.__clean_nested(value))

                elif isinstance(value, HelmYaml):
                    cleaned_dict_or_list = value.to_dict()

                    if cleaned_dict_or_list:
                        cleaned_list.append(cleaned_dict_or_list)

                else:
                    cleaned_list.append(value)
            return cleaned_list

        elif isinstance(dictionary_or_list, dict):
            cleaned_dict = {}
            for key, value in dictionary_or_list.items():
                # If value is None, [] or {}, '' do not include key
                if not value:
                    continue

                elif isinstance(value, (dict, list)):
                    cleaned_dict_or_list = self.__clean_nested(value)

                    if cleaned_dict_or_list:
                        cleaned_dict[key] = cleaned_dict_or_list

                elif isinstance(value, HelmYaml):
                    cleaned_dict_or_list = value.to_dict()

                    if cleaned_dict_or_list:
                        cleaned_dict[key] = cleaned_dict_or_list
                else:
                    cleaned_dict[key] = value
            return cleaned_dict

    def __str__(self):
        return dump(self.to_dict())

    def to_dict(self):
        dictionary = deepcopy(self.__dict__)
        return self.__clean_nested(dictionary)