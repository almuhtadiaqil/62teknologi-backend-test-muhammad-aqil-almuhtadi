class BaseResponseSingle(object):
    data = None
    status = 200
    message = None

    def __init__(self, data, exception, status):
        self.data = data
        self.message = str(exception) if exception is not None else None
        self.status = status

    def serialize(self):
        return {
            # message / status/ data
            "data": self.data,
            "status": self.status,
            "message": self.message,
        }


class BaseResponse(object):
    data = None
    status = 200
    message = None
    page = 1
    limit = 5

    def __init__(self, data, message, page, limit, total, status):
        self.total = total
        self.page = page
        self.limit = limit
        self.data = data
        self.message = str(message) if message is not None else None
        self.status = status

    def serialize(self):
        return {
            # message / status/ data
            "data": self.data,
            "total": self.total,
            "page": self.page,
            "limit": self.limit,
            "status": self.status,
            "message": self.message,
        }
