def mask_email(email) -> str:
    name, domain = email.split("@")
    return name[0] + "****" + name[-1:] + "@" + domain

def mask_phone(phone) -> str:
    return "*****" + phone[-4:]
