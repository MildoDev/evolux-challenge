def public_endpoint(function):
    function.is_public = True

    return function


def refresh_token_endpoint(function):
    function.is_refresh_token = True

    return function
