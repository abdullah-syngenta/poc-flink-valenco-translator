import logging

from logic.normalizer import Normalizer


class AssetNormalizer(Normalizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def normalize(self, raw_data):
        asset = self.normalize_asset(raw_data)
        normalized_data = [{
            'device_id': '',
            'asset_id': asset[0]['id']
        }]

        logging.info({
            'normalized_data': normalized_data
        })
        return asset

    def normalize_asset(self, raw_data):
        device_name = raw_data['name']
        asset_id = self.generate_asset_id_from_alias(
            id=f'{device_name}',
            model_scope='ASSET',
            system_type='VALENCO',
            instance_system_id=''
        )

        return [{
            'id': asset_id,
            'integrationAccountRef': self.account_id,
            'aliases': [
                {
                    'id': f'{device_name}',
                    'modelScope': 'ASSET',
                    'systemType': 'VALENCO',
                    'instanceSystemId': None
                }
            ]
        }]
