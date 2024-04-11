import json
import os
import types


import jaraco.collections


class IdentifierDict(jaraco.collections.KeyTransformingDict):
    @staticmethod
    def transform_key(key):
        return key.replace(' ', '_')


def load():
    return types.SimpleNamespace(
        **IdentifierDict(json.loads(os.environ['CONTACT_INFO']))
    )
