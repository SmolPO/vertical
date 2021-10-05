db_keys = {"auto": "(model, brand, gov_number, track_number)",
           "drivers": "(family, name, surname, birthday, passport, adr)",
           "workers": "(family, name, surname, birthday, post, phone, passport, passport_got, adr, live_adr, inn, "
                      "snils, numb_contract, date_contract, numb_h, numb_group_h, date_h, numb_study, numb_study_card, "
                      "d_study, numb_protocol, numb_card, d_protocol)",
           "itrs": "(family, name, surname, post, passport, passport_date, passport_got, adr, live_adr, auto, inn, "
                   "snils, n_td, td_date, "
                   "ot_protocol, ot_date, ot_card, "
                   "PTM_protocol, PTM_date, PTM_card, "
                   "es_protocol, es_group, es_card, es_date, "
                   "h_protocol, h_date, h_group, h_card, "
                   "industrial_save, "
                   "st_protocol, st_card, st_date, birthday)",
           "contracts": "(name, customer, number, date, object, work, part)",
           "company": "(company, adr, ogrn, inn, kpp, bik, korbill, rbill, bank, family, "
                   "name, surname, post, count_attorney, date_attorney)",
           "bosses": "(family, name, surname, post, email, phone, sex)",
           "materials": "(name, measure, value, provider)",
           "musics": "(name, link)"}


def get_person(person):
    return "SELECT * FROM workers WHERE family={0}".format(person)


def get_from_db(fields, db):
    insert = "SELECT " + fields + " FROM " + db
    return insert


def add_to_db(data, table):
    result = "('" + "', '".join(data) + "')"
    names_colomn = db_keys[table]
    return "INSERT INTO {0} {1} VALUES {2}".format(table, names_colomn, result)


def update_mat(material, fields, data, table):
    return "UPDATE {0} SET {1} = {2} where name = '{3}'".format(table, fields, data, material)
