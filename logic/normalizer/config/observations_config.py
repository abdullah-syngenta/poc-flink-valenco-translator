def get():

    return [
        {
            'data_type': 'waterPotOffBoard',
            'observations':
                [
                    {
                        'obsCode': 'E_SOIL_WATER_POTENTIAL',
                        'codeComponents': [
                            {
                                "componentCode": "CC_METADATA_DEVICE_FIRMWARE_VER",
                                "componentType": "METADATA_DEVICE",
                                "selector": "FIRMWARE_VERSION",
                                "value": "#$.firmware#"
                            }
                        ],
                        'phenTime': '&convert_to_date_time(#$.ts#)&',
                        'valueUoM': 'kPa',
                        'value': '#$.value#'
                    },
                    {
                        'obsCode': 'E_SOIL_WATER_TENSION',
                        'codeComponents': [
                            {
                                "componentCode": "CC_METADATA_DEVICE_FIRMWARE_VER",
                                "componentType": "METADATA_DEVICE",
                                "selector": "FIRMWARE_VERSION",
                                "value": "#$.firmware#"
                            }
                        ],
                        'phenTime': '&convert_to_date_time(#$.ts#)&',
                        'valueUoM': 'kPa',
                        'value': '&change_sign(#$.value#)&'
                    }
                ]
        },
        {
            'data_type': 'tempOffBoard',
            'observations':
                [
                    {
                        'obsCode': 'E_SOIL_TEMPERATURE',
                        'codeComponents': [
                            {
                                "componentCode": "CC_METADATA_DEVICE_FIRMWARE_VER",
                                "componentType": "METADATA_DEVICE",
                                "selector": "FIRMWARE_VERSION",
                                "value": "#$.firmware#"
                            }
                        ],
                        'phenTime': '&convert_to_date_time(#$.ts#)&',
                        'valueUoM': 'C',
                        'value': '#$.value#'
                    }
                ]
        },
        {
            'data_type': 'batteryCharge',
            'observations':
                [
                    {
                        'obsCode': 'M_BATTERY_CHARGE',
                        'codeComponents': [
                            {
                                "componentCode": "CC_METADATA_DEVICE_FIRMWARE_VER",
                                "componentType": "METADATA_DEVICE",
                                "selector": "FIRMWARE_VERSION",
                                "value": "#$.firmware#"
                            }
                        ],
                        'phenTime': '&convert_to_date_time(#$.ts#)&',
                        'valueUoM': 'prcnt',
                        'value': '#$.value#'
                    }
                ]
        }
    ]
