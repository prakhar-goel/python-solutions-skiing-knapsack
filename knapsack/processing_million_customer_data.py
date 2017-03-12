with open("millionth_customer_products.csv") as f, open("millionth_customer_products_processed.csv", "w") as wr:
	for line in f:
		product_id, price, length, width, height, weight = map(int,line.split(","))
		volume = length * width * height
		wr.write("%s, %s, %s, %s\n"%(product_id, price, volume, weight))
