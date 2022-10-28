def get():
    return [
        {
            "componentCode": "CC_AGG_TIME_DURATION",
            "componentType": "AGG_TIME_WINDOW",
            "selector": "DURATION",
            "value": "0",
            "valueUoM": "sec"
        },
        {
            "componentCode": "CC_METADATA_DEVICE_SENSOR_LENGTH",
            "componentType": "METADATA_DEVICE",
            "selector": "SENSOR_LENGTH",
            "value": "&convert_cm_to_mm(#$.attributes.sensor_length#)&",
            "valueUoM": "mm"
        },
        {
            "componentCode": "CC_METADATA_HAS_IRRIGATION",
            "componentType": "METADATA",
            "selector": "HAS_IRRIGATION",
            "value": "&get_boolean_value(#$.attributes.has_irrigation#)&"
        },
        {
            "componentCode": "CC_PARAM_SOIL_DEPTH_RANGE",
            "componentType": "PARAMETER",
            "selector": "SOIL_DEPTH_RANGE",
            "value": "[&convert_cm_to_mm(#$.attributes.install_depth#)&,"
                     "&get_max_lenght(#$.attributes.install_depth#,#$.attributes.sensor_length#)&]",
            "valueUoM": "mm"
        },
        {
            "componentCode": "CC_METADATA_PLOT_NUMBER",
            "componentType": "METADATA",
            "selector": "PLOT_NUMBER",
            "value": "#$.attributes.plot_number#"
        },
        {
            "componentCode": "CC_METADATA_SOIL_PREPARATION",
            "componentType": "METADATA",
            "selector": "SOIL_PREPARATION",
            "value": "&map_soil_preparation(#$.attributes.soil_preparation#)&"
        },
        {
            "componentCode": "CC_FOI_CROP_VARIETY_NAME",
            "componentType": "FEATURE_OF_INTEREST",
            "selector": "CROP_VARIETY_NAME",
            "value": "#$.attributes.variety#"
        },
        {
            "componentCode": "CC_METADATA_TRIAL_EXPERIMENTAL_DESIGN",
            "componentType": "METADATA",
            "selector": "TRIAL_EXPERIMENTAL_DESIGN",
            "value": "&map_experimental_design(#$.attributes.trial_attributes.experimental_design#)&"
        },
        {
            "componentCode": "CC_METADATA_USER_UOM_SYSTEM",
            "componentType": "METADATA",
            "selector": "USER_UOM_SYSTEM",
            "value": "&map_is_unit_presentation_metric(#$.attributes.trial_attributes.is_unit_presentation_metric#)&"
        },
        {
            "componentCode": "CC_METADATA_TRIAL_NAME",
            "componentType": "METADATA",
            "selector": "TRIAL_NAME",
            "value": "#$.attributes.trial_attributes.name#"
        },
        {
            "componentCode": "CC_PARAMETER_ORGANIC_MATTER",
            "componentType": "PARAMETER",
            "selector": "ORGANIC_MATTER",
            "value": "#$.attributes.trial_attributes.organic_matter#",
            "valueUoM": "prcnt"
        },
        {
            "componentCode": "CC_PARAMETER_PLANTING_DATE",
            "componentType": "PARAMETER",
            "selector": "PLANTING_DATE",
            "value": "#$.attributes.trial_attributes.sowing_date#"
        },
        {
            "componentCode": "CC_PARAMETER_TRIAL_END_DATE",
            "componentType": "PARAMETER",
            "selector": "TRIAL_END_DATE",
            "value": "#$.attributes.trial_attributes.end_date#"
        },
        {
            "componentCode": "CC_METADATA_TRIAL_TRIALIST_EMAIL_ADDRESS",
            "componentType": "METADATA",
            "selector": "TRIAL_TRIALIST_EMAIL",
            "value": "#$.attributes.trial_attributes.trialist_email_address#"
        },
        {
            "componentCode": "CC_METADATA_TRIAL_TRIALIST_NAME",
            "componentType": "METADATA",
            "selector": "TRIAL_TRIALIST_NAME",
            "value": "#$.attributes.trial_attributes.trialist_name#"
        },
        {
            "componentCode": "CC_METADATA_PLOT_SIZE",
            "componentType": "METADATA",
            "selector": "PLOT_SIZE",
            "value": "#$.attributes.trial_attributes.plot_size#",
            "valueUoM": "m2"
        }
    ]
