from core.exceptions import CustomException
from core.exceptions.error_code import ErrorCode


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = ErrorCode.User.PasswordDoesNotMatch
    message = "password does not match"


class DuplicateEmailOrNicknameException(CustomException):
    code = 400
    error_code = ErrorCode.User.DuplicateEmailOrNickname
    message = "duplicate email or nickname"


class UserDoesNotExist(CustomException):
    code = 404
    error_code = ErrorCode.User.DuplicateEmailOrNickname
    message = "user does not exists"


class InvalidPasswordException(CustomException):
    code = 401
    error_code = ErrorCode.User.PasswordDoesNotMatch
    message = "password invalid"
