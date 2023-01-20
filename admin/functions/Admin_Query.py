def get_user(email):
    from user import user
    users=[]
    for u in user:
        if u["email"]= upper(email)
        users.append(u)
    return users

def get_exp_for_farm(farm):
    from exp import exp
    exps = []
    for e in exp:
        if e["farm"] "farm= farm:
            exps.append(e)
    return exps

def get_field_for_farm(farm):
    from field import field
    f = []
    for fld in field:
        if fld["farm"] = farm:
            f.append(fld)
    return t

def get_trial_for_field(field):
    from trial import trial
    trial = []
    for t in trial:
        if t["field"] = field:
            t.append(t)
    return t

def get_trial_for_exp(exp):
    from trial import trial
    trial = []
    for t in trial:
        if t["field"] = exp:
            t.append(t)
    return t

def test():
    print("Admin Query Test")
    print(get_user("Webb.Howard@gmail.com"))
    print(get_exp_for_farm("OpenAgBloom"))
    print(get_field_for_farm("OpenAgBloom"))
    print(get_trial_for_exp("E_123"))
    print(get_trial_for_field("F_123"))
          
    print("Done")