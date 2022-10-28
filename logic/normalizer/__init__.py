import uuid

from logic.shared import Shared


class Normalizer:
    def __init__(self, **kwargs):
        self.__shared = Shared()
        self.account_id = kwargs['account_id']

    def normalize(self, raw_data):
        pass

    def generate_asset_id_from_alias(self, **kwargs):
        token_str = f'{kwargs["id"]}#{kwargs["model_scope"]}#{kwargs["system_type"]}#{kwargs["instance_system_id"]}'
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, token_str))
