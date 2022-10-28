from logic.normalizer.config import observations_config, observation_collection_config


class ObservationConfig:
    def get_observation_collection(self):
        config = observation_collection_config.get()
        return config

    def get_data_type_observation(self, data_type):
        config = observations_config.get()
        for item in config:
            if item['data_type'] != data_type:
                continue
            return item['observations']

        return None
