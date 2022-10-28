import json
import re
import datetime
import pytz

from jsonpath_ng.ext import parser
import logging

from logic.normalizer.config import soil_preparation_mapping_config, experimental_design_mapping_config
from logic.shared import Shared


class NormalizerTokens:
    def __init__(self, **kwargs):
        self.__shared = Shared()
        self.__device = kwargs['device']

    def convert_to_float(self, value):
        converted_value = None
        try:
            if value is not None:
                converted_value = float(value)
        except ValueError:
            pass
        return converted_value

    def replace_config_tokens(self, raw, config_dict):
        config_json = json.dumps(config_dict)
        config_json = self.replace_tokens(config_json, raw)
        config_json = self.replace_function_tokens(config_json, raw)

        return config_json

    def replace_tokens(self, config_file_string, raw):
        all_tokens = self.find_all_tokens(config_file_string)
        for token in all_tokens:
            config_file_string = self.replace_token(config_file_string, raw, token)

        return config_file_string

    def replace_token(self, config_file_string, raw, token):
        expression = token.replace('#', '')
        try:
            results = [match.value for match in parser.parse(expression).find(raw)]
            if len(results) > 0 and results[0] is not None:
                expression_translated = results[0]
            else:
                logging.warning({
                        'replace_tokens_error': f'no matched data or null value for the token {token}',
                        'expression': expression,
                        'raw': raw
                    })
                expression_translated = ''

            config_file_string = config_file_string.replace(token, str(expression_translated))
        except Exception as e:
            logging.warning({'replace_tokens_error': e, 'expression': expression, 'raw': raw})
        return config_file_string

    def replace_function_tokens(self, config_file_string, raw):
        all_tokens = self.find_all_function_tokens(config_file_string)
        for token in all_tokens:
            expression = token.replace('&', '')
            try:
                function, params_list = self.extract_function_info(expression)
                expression_translated = function(params_list)
            except Exception as e:
                logging.warning({
                    'replace_function_tokens_error': e,
                    'expression': expression,
                    'raw': raw
                })
                expression_translated = ''

            config_file_string = config_file_string.replace(token, str(expression_translated))

        return config_file_string

    def extract_function_info(self, expression):
        index = expression.index('(')
        index2 = expression.index(')')
        function_name = expression[:index]
        function = getattr(self, function_name)
        params = expression[index + 1: index2]
        return function, params.split(',')

    def find_all_tokens(self, string):
        return self.unique(re.findall('#.' + '*' + '?#', string))

    def unique(self, ls):
        list_set = set(ls)
        return list(list_set)

    def find_all_function_tokens(self, string):
        return self.unique(re.findall('&.' + '*' + '?&', string))

    def change_sign(self, params):
        return (-1) * float(params[0])

    def get_boolean_value(self, params):
        return True if int(params[0]) == 1 else False

    def convert_to_date_time(self, params):
        try:
            date_time = datetime.datetime.fromtimestamp(int(params[0]) / 1000)
            date_time_utc = self.__shared.convert_to_timezone(date_time, pytz.utc)
            return date_time_utc.isoformat().replace('+00:00', 'Z')
        except Exception as e:
            logging.info({
                'date': params[0],
                'device': self.__device,
                'convert_to_utc_error': e
            })

            return params[0]

    def map_soil_preparation(self, params):
        soil_preparation_mapping = soil_preparation_mapping_config.get()

        for soil_preparation_obj in soil_preparation_mapping:
            if soil_preparation_obj['name'] == params[0]:
                return soil_preparation_obj['value']

        logging.info({
            'soil_preparation_mapping_error': f'Failed to find a mapping for soil_preparation: {params[0]}',
            'device': self.__device
        })

        return ''

    def map_experimental_design(self, params):
        experimental_design_mapping = experimental_design_mapping_config.get()

        for experimental_design_obj in experimental_design_mapping:
            if experimental_design_obj['name'] == params[0]:
                return experimental_design_obj['value']

        logging.info({
            'experimental_design_mapping_error': f'Failed to find a mapping for soil_preparation: {params[0]}',
            'device': self.__device
        })

        return ''

    def get_max_lenght(self, params):
        return (float(params[0])+float(params[1]))*10

    def convert_cm_to_mm(self, params):
        return (float(params[0]))*10

    def map_is_unit_presentation_metric(self, params):
        return 'METRIC' if int(params[0]) == 1 else 'IMPERIAL'
