workers_with_adr = "SELECT family, name, surname, post, address, post FROM workers"
full_worker_date = "SELECT name, family, surname, post, birthdate, passport_seria, passport_number, address,  live_address " + \
                 "FROM workers"
workers = "SELECT family, name, surname FROM workers"
add_worker = "INSERT INTO workers * VALUES {0}"
auto = "SELECT model, number, family, name, surname, passport_serial, passport_number, address " + \
                 "FROM auto"

def pass_week(build):
    return "SELECT name, family, surname, post, birthdate, passport_seria, passport_number, address,  live_address " + \
                 "FROM workers WHERE build = '" + build + "'"
