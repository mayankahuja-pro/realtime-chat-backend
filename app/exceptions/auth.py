class AuthenticationException(Exception):
    pass


class InvalidCredentialsException(AuthenticationException):
    pass


class EmailAlreadyExistsException(AuthenticationException):
    pass


class InvalidTokenException(AuthenticationException):
    pass