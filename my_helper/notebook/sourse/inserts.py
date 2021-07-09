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
    result = "('"
    result += company[0]
    result += "', '" + company[1]
    result += "', " + str(company[2])
    result += ", " + str(company[3])
    result += ", " + str(company[4])
    result += ", " + str(company[5])
    result += ", " + str(company[6])
    result += ", " + str(company[7])
    result += ", '" + company[8]
    result += "', '" + company[9]
    result += "', '" + company[10]
    result += "', '" + company[11]
    result += "', '" + company[12]
    result += "', '" + company[13]
    result += "', '" + company[14] + "')"
    names_colomn = "(company, adr, ogrn, inn, kpp, bik, korbill, rbill, bank, family, " \
                   "name, surname, post, count_dovr, date_dovr)"
    print("INSERT INTO company {0} VALUES {1}".format(names_colomn, result))
    return "INSERT INTO company {0} VALUES {1}".format(names_colomn, result)


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
