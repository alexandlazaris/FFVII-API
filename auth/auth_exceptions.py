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

class SignUpInviteExpiredError(Exception):
    pass

class SignUpInviteDisabledError(Exception):
    pass