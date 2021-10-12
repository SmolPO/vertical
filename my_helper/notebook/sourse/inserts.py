db_keys = {"auto": "(gov_number, model, brand, track_number, id)",
           "drivers": "(family, name, surname, passport, adr, birthday, id)",
           "workers": "(family, name, surname, birthday, post, phone, passport, passport_got, adr, live_adr, inn, "
                      "snils, numb_contract, date_contract, numb_h, numb_group_h, date_h, numb_study, numb_study_card, "
                      "d_study, numb_protocol, numb_card, d_protocol, object, id)",
           "itrs": "(family, name, surname, post, passport, passport_date, passport_got, adr, live_adr, auto, inn, "
                   "snils, n_employment_contract,date_employment_contract, "
                   "ot_protocol, ot_date, ot_card, "
                   "PTM_protocol, PTM_date, PTM_card, "
                   "es_protocol, es_group, es_card, es_date, "
                   "h_protocol, h_date, h_group, h_card, "
                   "industrial_save, "
                   "st_protocol, st_card, st_date, birthday, id)",
           "contracts": "(name, customer, number, date, object, type_work, place, id)",
           "company": "(company, adr, ogrn, inn, kpp, bik, korbill, rbill, bank, family, "
                   "name, surname, post, count_attorney, date_attorney, id)",
           "bosses": "(family, name, surname, post, email, phone, sex, id)",
           "materials": "(name, measure, value, provider, contract, id)",
           "musics": "(name, link, id)",
           "finance": "(date, value, recipient, comment, id)"}


def get_person(person):
    return "SELECT * FROM workers WHERE family={0}".format(person)


def get_from_db(fields, db):
    insert = "SELECT " + fields + " FROM " + db
    return insert


def add_to_db(data, table):
    result = "('" + "', '".join(data) + "')"
    names_colomn = db_keys[table]
    print(len(data), len(names_colomn.split(" ")))
    return "INSERT INTO {0} {1} VALUES {2}".format(table, names_colomn, result)


def my_update(data, table):
    fields = db_keys.get(table)
    my_id = data[-1]
    result = "('" + "', '".join(data) + "')"
    print("UPDATE {0} SET {1} = {2} where id = '{3}'".format(table, fields, result, my_id))
    return "UPDATE {0} SET {1} = {2} where id = '{3}'".format(table, fields, result, my_id)


def from_str(date):
    return int(date[0:2]), int(date[2:4]), int(date[4:])