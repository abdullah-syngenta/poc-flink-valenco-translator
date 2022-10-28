import json
import uuid

from logic.normalizer import Normalizer
from logic.normalizer.config import observations_common_config, observation_common_codecomponent
from logic.normalizer.config.observation_config import ObservationConfig
from logic.normalizer.normalizer_tokens import NormalizerTokens


class ObservationNormalizer(Normalizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__data_type = kwargs['data_type']
        self.normalizer_tokens = NormalizerTokens(**kwargs)
        self.__observation_config = ObservationConfig()

    def normalize(self, timeseries_record):
        obs_coll_common_data = timeseries_record['obs_coll_common_data']
        obs_common_code_component = timeseries_record['obs_common_code_component']
        obs_common_data = timeseries_record['obs_common_data']

        obs_collection_id = str(uuid.uuid1())
        observations_config = self.__observation_config.get_data_type_observation(self.__data_type)
        if not observations_config:
            return None, None

        obs_ids, observations = self.normalize_obs(obs_collection_id, obs_common_code_component,
                                                   obs_common_data, observations_config, timeseries_record)

        observation_collection = self.normalize_obs_coll(obs_coll_common_data, obs_collection_id, obs_ids,
                                                         observations, timeseries_record)

        return observations, observation_collection

    def translate_common_data(self, raw_data):
        asset_id = self.generate_asset_id_from_alias(
            id=f"{raw_data['device']['name']}",
            model_scope='ASSET',
            system_type='VALENCO',
            instance_system_id=''
        )
        raw_data['integration_account'] = self.account_id
        raw_data['asset_id'] = asset_id

        obs_common_data_string = self.normalizer_tokens.replace_config_tokens(
            raw_data,
            observations_common_config.get()
        )
        obs_coll_common_data_string = self.normalizer_tokens.replace_config_tokens(
            raw_data,
            observations_common_config.get()
        )
        obs_common_code_component_string = self.normalizer_tokens.replace_config_tokens(
            raw_data,
            observation_common_codecomponent.get()
        )

        obs_common_data = json.loads(obs_common_data_string)
        obs_coll_common_data = json.loads(obs_coll_common_data_string)
        obs_common_code_component = json.loads(obs_common_code_component_string)
        obs_common_code_component = [code_component for code_component in obs_common_code_component
                                     if code_component['value'] != '']

        return obs_coll_common_data, obs_common_code_component, obs_common_data

    def normalize_obs(self, obs_collection_id, obs_common_code_component, obs_common_data, observations_config,
                      raw_object):
        obs_ids = []
        observations_list = []

        observations_string = self.normalizer_tokens.replace_config_tokens(
            raw_object,
            observations_config
        )
        observations = json.loads(observations_string)

        for observation in observations:
            observation['codeComponents'].extend(obs_common_code_component)
            observation['id'] = str(uuid.uuid4())
            observation['parentCollectionRef'] = obs_collection_id
            self.handle_location(obs_common_data)
            observation.update(obs_common_data)

            observations_list.append(observation)
            obs_ids.append(observation['id'])

        observations = {'Obs': observations_list}

        return obs_ids, observations

    def normalize_obs_coll(self, obs_coll_common_data, obs_collection_id, obs_ids, observations, raw_object):
        observation_coll_config = self.__observation_config.get_observation_collection()
        observation_collection_string = self.normalizer_tokens.replace_config_tokens(
            raw_object,
            observation_coll_config
        )
        observation_collection = json.loads(observation_collection_string)

        observation_collection['ObsCollection'][0]['id'] = obs_collection_id
        observation_collection['ObsCollection'][0]['phenTime'] = observations['Obs'][0]['phenTime']
        observation_collection['ObsCollection'][0]['obsRefs'] = obs_ids
        self.handle_location(obs_coll_common_data)
        observation_collection['ObsCollection'][0].update(obs_coll_common_data)

        return observation_collection

    def convert_to_float(self, value):
        converted_value = None
        try:
            if value is not None:
                converted_value = float(value)
        except ValueError:
            pass
        return converted_value

    def handle_location(self, common_data):
        common_data['xMin'] = self.convert_to_float(common_data['xMin'])
        common_data['yMin'] = self.convert_to_float(common_data['yMin'])
        common_data['xMax'] = self.convert_to_float(common_data['xMax'])
        common_data['yMax'] = self.convert_to_float(common_data['yMax'])

        if common_data['xMin'] is None or common_data['yMin'] is None:
            common_data['spatialExtent'] = '{"type": "Point", "coordinates": [null, null]}'
