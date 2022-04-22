import mariadb_sqlbuilder

mariadb_sqlbuilder.builder.echo_sql = True

connection = mariadb_sqlbuilder.Connect(
    host="192.168.2.230",
    user="root",
    password="superpassword",
    database="kaguya"
)


# result = connection.table("guilds").select("created_at").where("id", 495573880598167562).where("logging", 0).fetchone()
# result = connection.table("guilds").select("created_at").fetchall()

# result = connection.table("guilds").upsert().set("id", 737738997173846037).set("mod_role", 200).execute()
# result = connection.table("guilds").insert().set("id", 737738997173846037).ignore().execute()
# result = connection.table("guilds").insert().set("id", 495573880598167562).ignore().execute()
result = connection.table("guilds").delete().where("id", 1).execute()
result = connection.table("guilds").delete().where("id", 2).execute()

#connection.execute_script("INSERT IGNORE INTO guilds(id) VALUES (1); INSERT IGNORE INTO guilds(id) VALUES (2);")

#print(result)
