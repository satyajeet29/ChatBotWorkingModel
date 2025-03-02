def projectAccessRules():
    projectAccessGuidelines = """
    ### Project Access Rules:
    1. User project roles:
        * Users gain access to projects via the user_project_role_access table
        * Access permissions are controlled by the read_only flag
        * Inactive roles are managed using the is_inactive flag
    2. Project ownership and management is based on following:
        * Projects are created independently of groups but are tied to specific users for management
        * Project status is determined by field project_status and is used for determining the lifecycle state
    3. Utility billing: Utility bills (e.g., electricity, gas, water, solar) are associated with properties through respective utility tables (e.g., property_electricity)
    """
    return projectAccessGuidelines