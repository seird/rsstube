from PyQt6 import QtGui


class PlayResolutionAction(QtGui.QAction):
    def __init__(self, resolution: str):
        self.resolution = resolution
        super(PlayResolutionAction, self).__init__(resolution)


class PlayAudioOnlyAction(PlayResolutionAction):
    def __init__(self):
        super(PlayAudioOnlyAction, self).__init__("Audio only")


class SaveThumbnailAction(QtGui.QAction):
    def __init__(self):
        super(SaveThumbnailAction, self).__init__("Save thumbnail")
