def userPropertyAccessRules():
    userAccessToPorperties = """
    ### User and Property Access Rules:
    1. User Access to properties is based upon following points:
        * A user can have access to multiple properties through the user_property_role table
        * The read_only flag determines if a user has read-only or full access to a property
        * The is_inactive flag removes a user's access without deleting the relationship
    2. Group ownership and property access is determined by following rules:
        * Properties belong to groups (group_id) as defined in the property table
        * Users are associated with groups through the users table.
        * An owner (admin) of a group has access to all properties within that group
    3. Cross-Group data isolation:
        * Users from one group cannot access properties or data from other groups
        * It is enforced by the group_id field in both users and property tables    
    """
    return userAccessToPorperties