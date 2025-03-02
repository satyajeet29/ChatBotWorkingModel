def energyConsumptionRules():
    energyConsumptionProperties = """
    ### Energy Consumption Data Rules:
    1. Property Energy Setup is based on following guidelines:
        * Each property has its energy setup defined in property_energy_setup table
        * Determines connection to external accounts like Energy Star or Energy Direct
    2. Utility Provider Data is based on following rules:
        * Energy consumption data is linked to properties using the property_id
        * Aggregation levels include daily (daily_aggregated_utility_provider_data) and monthly (monthly_aggregated_utility_provider_data)
    3. Utility Billing for utility bills (e.g., electricity, gas, water, solar) are associated with properties through respective utility tables (e.g., property_electricity, property_gas, property_water, property_solar).
    """