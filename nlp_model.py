
def check_for_confidential_info(message):
    confidential_keywords = ["password", "ssn", "credit card", "bank account", "private", "confidential"]
    for keyword in confidential_keywords:
        if keyword.lower() in message.lower():
            return True
    return False