"""базовые исключения, можно вынести в файл, оставил так"""


class AppException(Exception):
    """корневое исключение"""
    pass


class DatabaseException(AppException):
    """ошибка базы данных"""
    pass


class CacheException(AppException):
    """ошибка кэша"""
    pass


class ConfigurationException(AppException):
    """ошибка конфигурации"""
    pass


class NotFoundError(AppException):
    """ресурс не найден"""
    pass


class ValidationError(AppException):
    """ошибка валидации"""
    pass
