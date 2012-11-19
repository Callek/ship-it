# Regex that matches all possible versions and milestones
ANY_VERSION_REGEX =\
    ('\d+\.\d[\d\.]*'    # A version number
    '([a-zA-Z]+\d+)?'    # Might be a project branch
    '((a|b)\d+)?'        # Might be an alpha or beta
    '(esr)?'             # Might be an esr
    '(pre)?')            # Might be a 'pre' (nightly) version
