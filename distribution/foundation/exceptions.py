class DomainException(Exception):
    pass

class DomainIdError(DomainException):
    pass

class DomainNotFoundError(DomainException):
    pass

def domain_id_error(domainname, id):
    if (id == None):
        return get_id_error(domainname, "None", "ID is missing!")
    else:
        return get_id_error(domainname, id, "ID could not be found!")

def get_id_error(domainname, id, message):
    message = domainname + "ID-" + str(id) + ": " + message
    return DomainIdError(message)

def domain_not_found_error(domain):
    domaintype = type(domain)
    return get_domain_error(domaintype, " not found!")

def get_domain_error(domaintype, message):
    message = str(domaintype.__name__) + message
    return DomainNotFoundError(message)