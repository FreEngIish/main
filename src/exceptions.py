class RoomCreationException(Exception):
    def __init__(self, message='Failed to create room'):
        self.message = message
        super().__init__(self.message)

class RoomGetException(Exception):
    def __init__(self, message='Failed to get room'):
        self.message = message
        super().__init__(self.message)

class RoomUpdateException(Exception):
    def __init__(self, message='Failed to upadte room'):
        self.message = message
        super().__init__(self.message)

class RoomNotFoundException(Exception):
    def __init__(self, message='Room not found'):
        self.message = message
        super().__init__(self.message)

class PermissionDeniedException(Exception):
    def __init__(self, message='Permission denied'):
        self.message = message
        super().__init__(self.message)
