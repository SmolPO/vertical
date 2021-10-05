import psycopg2

conn = psycopg2.connect("host=95.163.249.246 dbname=Vertical_db user=office password=9024EgrGvz#m87Y1")
print("OK conn")
db = conn.cursor()
try:
    db.execute("CREATE TABLE auto (model text, brand text, gov_number text, track_number text)")
    print("add table auto")
    db.execute("CREATE TABLE drivers (family text, name text, surname text, birthday text, passport text, adr text)")
    print("add table drivers")
    db.execute("CREATE TABLE contracts (name text, customer text, number text, date text, object text, type_work text, "
               "place text)"),
    print("add table contracts")
    db.execute("CREATE TABLE bosses (family text, name text, surname text, post text, email text, phone text, sex text)")
    print("add table bosses")
    db.execute("CREATE TABLE musics (name text, link text)")
    print("add table materials")
    db.execute("CREATE TABLE materials (name text, measure text, value text, provider text)")
    print("add table materials")
    db.execute("CREATE TABLE company (company text, adr text, ogrn text, inn text, kpp text, bik text, korbill text, "
               "rbill text, bank text, family text, name text, surname text, post text, count_attorney text, "
               "date_attorney text)")
    print("add table company")
    db.execute("CREATE TABLE workers (family text, name text, surname text, birthday text, post text, phone text, "
               "passport text, passport_got text, adr text, live_adr text, inn text, snils text, numb_contract text, "
               "date_contract text, numb_h text, numb_group_h text, date_h text, numb_study text, numb_study_card text, "
               "d_study text, numb_protocol text, numb_card text, d_protocol text)")
    print("add table workers")
    db.execute("CREATE TABLE itrs (family text, name text, surname text, post text, passport text, passport_date text, "
               "passport_got text, adr text, live_adr text, auto text, inn text, "
               "snils text, n_employment_contract text, date_employment_contract text, "
               "ot_protocol text, ot_date text, ot_card text, "
               "PTM_protocol text, PTM_date text, PTM_card text, "
               "es_protocol text, es_group text, es_card text, es_date text, "
               "h_protocol text, h_date text, h_group text, h_card text, "
               "industrial_save text, "
               "st_protocol text, st_card text, st_date text, birthday text)")
    print("add table itrs")
except:
    print("error")
conn.commit()
db.execute("SELECT * FROM auto")
row = db.fetchall()
print(row)