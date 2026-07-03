class Intent:
    def __init__(self, tool, target):
        self.tool = tool
        self.target = target


def parse_intent(text):
    text = text.lower().strip()
    words = text.split()

    if len(words) < 2:
        return None

    if words[0] == "nmap":
        return Intent("nmap", words[1])

    if words[0] == "whois":
        return Intent("whois", words[1])

    return None
