workers_with_adr = "SELECT family, name, surname, post, address, post FROM workers"
full_workers_data = "SELECT name, family, surname, post, birthdate, passport_series, passport_number, address, live_address " + \
                 "FROM workers"
workers = "SELECT family, name, surname FROM workers"
auto = "SELECT model, number, family, name, surname, passport_series, passport_number, address " + \
                 "FROM auto"


def new_contract(contract):
    result = "('" + "', '".join(contract) + "')"
    names_colomn = "(name, customer, number, date, object, work, part)"
    return "INSERT INTO contract {0} VALUES {1}".format(names_colomn, result)


def new_company(company):
    result = "('" + "', '".join(company) + "')"
    names_colomn = "(company, adr, ogrn, inn, kpp, bik, korbill, rbill, bank, family, " \
                   "name, surname, post, count_dovr, date_dovr)"
    print("INSERT INTO company {0} VALUES {1}".format(names_colomn, result))
    return "INSERT INTO company {0} VALUES {1}".format(names_colomn, result)

def add_ITR(itr):
    result = "('" + "', '".join(itr) + "')"
    names_tables = "(family, name, surname, post, passport, passport_date, passport_got, adr, live_adr, auto, inn, " \
                   "snils, n_td, td_date, " \
                   "ot_prot, ot_date, ot_card, " \
                   "PTM_prot, PTM_date, PTM_card, " \
                   "es_prot, es_group, es_card, es_date, "\
                   "h_prot, h_date, h_group, h_card, " \
                   "promsave, " \
                   "st_prot, st_card, st_date, birthday)"
    print("INSERT INTO itr {0} VALUES {1}".format(names_tables, result))
    return "INSERT INTO itr {0} VALUES {1}".format(names_tables, result)


def add_worker(worker):
    result = "('" + "', '".join(worker) + "')"

    names_tables = "(family, name, surname, bithday, post, phone, pasport, pasport_got, adr, live_adr, inn, snils" \
                   ", numb_contract, date_contract, numb_h, numb_group_h, date_h, numb_study, numb_study_card, " \
                   "d_study, numb_prot, numb_card, d_prot)"
    print("INSERT INTO workers {0} VALUES {1}".format(names_tables, result))
    return "INSERT INTO workers {0} VALUES {1}".format(names_tables, result)


def get_workers():
    return "SELECT family FROM workers"


def get_worker(family):
    return "SELECT * FROM workers WHERE inn = '123123'"


def add_boss(boss):
    result = "('"
    result += boss[0] + "', '"
    result += boss[1] + "', '"
    result += boss[2] + "', '"
    result += boss[3] + "', '"
    result += boss[4] + "', '"
    result += boss[5] + "')"
    names_colomn = "(name, family, surname, post, email, phone)"
    return "INSERT INTO bosses {0} VALUES {1}".format(names_colomn, result)


def get_person(person):
    return "SELECT * FROM workers WHERE family={0}".format(person)


def get_builds():
    return "SELECT name FROM contract"


def pass_week(build):
    return "SELECT name, family, surname, post, birthdate, passport_series, passport_number, address,  live_address " + \
                 "FROM workers WHERE build = '" + build + "'"
