class ClientConfigError(Exception):
    def __init__(self, message=None):
        super(ClientConfigError, self).__init__(message)


class NoPipelinesError(Exception):
    pass


class ChannelNotFoundException(Exception):
    pass


class PlaylistException(Exception):
    def __init__(self, message):
        super(PlaylistException, self).__init__(message)