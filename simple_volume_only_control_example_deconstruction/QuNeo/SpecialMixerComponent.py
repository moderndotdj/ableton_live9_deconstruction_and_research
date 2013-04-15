import Live

from _Framework.MixerComponent import MixerComponent

class SpecialMixerComponent(MixerComponent):
    ' Subclass of the _Framework mixer class. Key for mixer functionality '
    __module__ = __name__

    def __init__(self, num_tracks, parent):
        MixerComponent.__init__(self, num_tracks)
        self._parent = parent
