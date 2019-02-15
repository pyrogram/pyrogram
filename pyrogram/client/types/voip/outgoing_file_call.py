from . import OutgoingCall, FileCallMixin


class OutgoingFileCall(FileCallMixin, OutgoingCall):
    pass
