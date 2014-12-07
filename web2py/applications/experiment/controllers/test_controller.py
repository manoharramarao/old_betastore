def test():
	print "inside test controller"
    
def test_record_representation():
    product = "solar water heater"
    price_type = "default"
    user_group = "user_1 (1)"
    id = "1"
    row = db(db.price.id == "1").select().first()
    #record1 = rows.render(0)
    record1 = db.price.code.represent(row.id, row)
    print db.price.code.represent(row.id, row)
    return dict(msg=str(record1))
