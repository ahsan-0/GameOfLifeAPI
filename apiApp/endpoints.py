endpoints = { "endpoints" : [
    {
        "GET /api/patterns": {
            "description": "Responds with list of all patterns."
        } 
    },
    {
        "POST /api/patterns": {
            "description": "Allows user to add a pattern to the database and returns the new pattern.",
            "example_request": {
                "pattern_body": "0101001101 1011001010 0011011010 1000101010 0100101000 1101100000 1010000011 1111000000 0100101010 0000101010",
                "pattern_name": "The Snake",
                "username": "Paprika69"
            }
        }
    }, 
    {
        "GET /api/patterns/:pattern_id": {
            "description": "Returns the pattern specified by the id."
        } 
    },
    {
        "PUT /api/patterns/:pattern_id": {
            "description": "Allows user to update a pattern and returns the updated pattern.",
            "example_request": { "pattern_name": "new name"}
        }
    }, 
    {
        "GET /api/users": {
            "description": "Responds with list of all registered users."
        }
    },
    {
        "POST /api/users": {
            "description": "Allows new user to be added to database and returns the new user.",
            "example_request": {
                "account_owner": "Jules877",
                "username": "ElectricJoule",
                "email": "Julia@autumn.co.uk",
                "avatar_url": "www.avatars.psy/avatars/color/DFF4?query=true%ptts"
            }
        }
    },
    {
        "GET /api/users/:user_id": {
            "description": "Returns the user specified by the id"
        }
    },
    {
        "PUT /api/users/:user_id": {
            "description": "Allows user to update their details and returns the updated user.",
            "example_request": {
                "account_owner": "John Joseph",
                "username": "Superstar445",
                "email": "newemail@emailprovider.com",
                "avatar_url": "www.avatars.psy/avatars/color/DFF4?query=true%ptts"
            }
        }
    },
    {
        "GET /api/users/:username/patterns": {
            "description": "Returns all patterns belonging to specified user"
        }
    },
    {
        "DELETE /api/patterns/:pattern_id": {
            "description": "Deletes the specified pattern from the database."
        }
    },
    {
        "DELETE /api/users/:user_id": {
            "description": "Deletes specified user from the database"
        }
    }
]}