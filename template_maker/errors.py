class TemplateMakerException(Exception):
    pass


class PrerequsitesNotFoundException(TemplateMakerException):
    def __init__(self, inkscape_found: bool, xtouch_fs2020_found: bool) -> None:
        self.inkscape_found = inkscape_found
        self.xtouch_fs2020_found = xtouch_fs2020_found
        super(PrerequsitesNotFoundException, self).__init__(self._construct_message())

    def _construct_message(self) -> str:
        memo = "Inkscape and Xtouch-FS2020 are required on c:\n"

        if not self.inkscape_found:
            memo += "\ninkscape.exe was not found."

        if not self.xtouch_fs2020_found:
            memo += "\nX-Touch-Mini-FS2020.exe was not found."

        return memo
