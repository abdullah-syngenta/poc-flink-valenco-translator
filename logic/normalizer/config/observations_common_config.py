def get():
    return {
        'integrationAccountRef': '#$.integration_account#',
        'assetRef': '#$.asset_id#',
        'contextItems': [
            {
                'code': 'SYN_SYSTEM',
                'value': 'VALENCO'
            }
        ],
        'status': 'ACTIVE',
        'xMin': '#$.attributes.user_long#',
        'xMax': '#$.attributes.user_long#',
        'yMin': '#$.attributes.user_lat#',
        'yMax': '#$.attributes.user_lat#',
        'spatialExtent': '{"type": "Point", "coordinates": [#$.attributes.user_long#,'
                         ' #$.attributes.user_lat#]}'
    }
