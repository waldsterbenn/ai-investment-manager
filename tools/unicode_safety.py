class UnicodeSafety:
    @staticmethod
    def makeSafe(text: str) -> str:
        return str(text.encode('utf-8'))
