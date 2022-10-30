import json

from pyflink.common import Types
from pyflink.datastream import ProcessFunction, OutputTag

from logic.normalizer.asset_normalizer import AssetNormalizer
from logic.normalizer.observation_normalizer import ObservationNormalizer

observations_output_tag = OutputTag("translated-observations", Types.STRING())
obsCollections_output_tag = OutputTag("translated-obsCollections", Types.STRING())


class ValencoTranslator(ProcessFunction):

    def process_element(self, value, ctx: ProcessFunction.Context):
        data_type = 'tempOffBoard'
        raw_data = json.loads(value)

        if data_type == 'device':
            return raw_data
        else:
            observation_normalizer = ObservationNormalizer(account_id='account_1', data_type='tempOffBoard',
                                                           device='xyz')
            obs_coll_common_data, obs_common_code_component, obs_common_data = observation_normalizer.translate_common_data(
                raw_data)

            for item in raw_data[data_type]:
                data_point = {
                    'ts': item['ts'],
                    'value': item['value'],
                    'firmware': [obj['value'] for obj in raw_data['firmware'] if item['ts'] == obj['ts']][0],
                    'obs_coll_common_data': obs_coll_common_data,
                    'obs_common_code_component': obs_common_code_component,
                    'obs_common_data': obs_common_data
                }

                observations, observation_collection = self.translate(data_point)
                yield observations_output_tag, json.dumps(observations)
                yield obsCollections_output_tag, json.dumps(observation_collection)

    def translate(self, timeseries):
        try:
            data_type = 'tempOffBoard'

            if data_type == 'device':
                normalizer = AssetNormalizer(account_id='account_1')
            else:
                normalizer = ObservationNormalizer(account_id='account_1', data_type='tempOffBoard', device='xyz')

            return normalizer.normalize(timeseries)
        except Exception as ex:
            print('arranged_raw_data', timeseries)
            print(ex)
