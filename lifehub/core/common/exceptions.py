class ServiceException(Exception):
    def __init__(self, module: str, status_code: int, message: str) -> None:
        self.module = module
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.module}: {self.message}"

    def __repr__(self) -> str:
        return f"<ServiceException({self.module}): {self.message}>"
