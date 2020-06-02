from datetime import datetime


class events():
    def __init__(self):
        pass

    @staticmethod
    def parse(payload):
        results = {}
        parsed_data = {}

        try:
            parsed_data["category"] = payload["category"]
            parsed_data["severity"] = payload["severity"]
            parsed_data["timestamp"] = payload["timestamp"]
            parsed_data["timestamp"] = datetime.utcfromtimestamp(parsed_data["timestamp"]/1000)
            parsed_data["timestamp"] = parsed_data["timestamp"].strftime('%Y-%m-%d %H:%M:%S')
            parsed_data["status"] = payload["details"]["Assurance Issue Status"]
            parsed_data["device"] = payload["details"]["Device"]
            parsed_data["eventId"] = payload["eventId"]
            parsed_data["details"] = payload["details"]["Assurance Issue Details"]
            parsed_data["url"] = payload["ciscoDnaEventLink"]
        except Exception:
            results["status"] = "Error: parsing payload"
            return results

        results["content"] = events.format(parsed_data)
        results["category"] = parsed_data["category"]
        return results

    @staticmethod
    def format(data):
        syslog_format = ("[{}] [{}] {} {} {} [{}] {} {} {}".format(
            data["timestamp"],
            "Cisco DNA Center",
            data["severity"],
            data["category"],
            data["status"],
            data["eventId"],
            data["device"],
            data["details"],
            data["url"]
        ))
        return syslog_format
