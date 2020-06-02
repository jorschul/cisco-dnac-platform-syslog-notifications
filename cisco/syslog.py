import logging
import logging.handlers


class remote():
    def __init__(self, format="", settings=""):
        self.data = {}

        try:
            self.data["content"] = format["content"]
            self.data["category"] = format["category"]
        except Exception:
            self.status = format["status"]
            return
        self.data["settings"] = settings
        if self.data["content"] == "":
            print("error")
            self.status = "Error: Syslog content missing"
            return
        if self.data["settings"] == "":
            print("error")
            self.status = "Error: Syslog settings missing"
            return

        self.dnac_logger = logging.getLogger("dnac_logger")
        self.send()
        self.status = "success"
        return

    def send(self):
        self.dnac_logger.setLevel(logging.INFO)
        if "tcp" in self.data["settings"]["syslog-protocol"]:
            handler = logging.handlers.SysLogHandler(
                socktype=logging.handlers.socket.SOCK_STREAM,
                address=(
                    str(self.data["settings"]["syslog-host"]),
                    int(self.data["settings"]["syslog-port"])
                )
            )
        else:
            handler = logging.handlers.SysLogHandler(
                socktype=logging.handlers.socket.SOCK_DGRAM,
                address=(
                    str(self.data["settings"]["syslog-host"]),
                    int(self.data["settings"]["syslog-port"])
                )
            )
        self.dnac_logger.addHandler(handler)

        if "ALERT" in self.data["category"]:
            self.dnac_logger.critical(self.data["content"])
        elif "ERROR" in self.data["category"]:
            self.dnac_logger.error(self.data["content"])
        elif "WARN" in self.data["category"]:
            self.dnac_logger.warning(self.data["content"])
        else:
            self.dnac_logger.info(self.data["content"])

        self.dnac_logger.removeHandler(handler)
        return
