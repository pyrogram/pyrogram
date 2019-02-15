from . import IncomingCall, FileCallMixin


class IncomingFileCall(FileCallMixin, IncomingCall):
    pass
