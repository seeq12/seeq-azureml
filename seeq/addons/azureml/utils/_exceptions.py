class AzureMLException(Exception):
    """Exception raised for errors connecting to the Azure ML service.

    Attributes
    ----------
        code: str, int
            HTTP response status code
        reason: str
            reason for the code
        message: str
            explanation of the error
    """

    def __init__(self, code=501, reason='Unknown', message="Internal Error"):
        self.code = '' if code is None else f'({code})'
        self.reason = '' if reason is None else f'Reason: {reason}'
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{str(self.code)}\n{self.reason}\n{self.message}'
