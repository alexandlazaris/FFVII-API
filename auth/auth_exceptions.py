class EmailExistsError(Exception):
    pass

class EmailRateLimitExceededError(Exception):
    pass

class EmailNotConfirmedError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class SessionNotFound(Exception):
    pass

class AuthConfigurationError(Exception):
    pass