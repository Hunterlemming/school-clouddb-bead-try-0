-- SCHEMA: try_0

-- DROP SCHEMA try_0 ;

CREATE SCHEMA try_0
    AUTHORIZATION krisz;



-- ============= SEQUENCES ============

create sequence try_0."seq_orders" start 1 increment 1;
create sequence try_0."seq_shippings" start 1 increment 1;



-- ============== TABLES ==============

-- Products
CREATE TABLE try_0."Products"(
	ProductID int NOT NULL,
	ProductName varchar(40) NOT NULL,
	PublisherID int NULL,
	PublisherName varchar(40) NULL,
	UnitPrice money NULL,
	UnitsInStock smallint NULL check(UnitsInStock >= 0),
 CONSTRAINT PK_Products PRIMARY KEY  
(
	ProductID 
));

-- 5 termék
INSERT INTO  try_0."Products" (ProductID, ProductName, PublisherID, PublisherName, UnitPrice, UnitsInStock) 
VALUES (1, 'Gaia Pro 2021', 2, 'Procedural Worlds', 258.17, 5);
INSERT INTO  try_0."Products" (ProductID, ProductName, PublisherID, PublisherName, UnitPrice, UnitsInStock) 
VALUES (2, 'POLYGON Fantasy Kingdom', 1, 'Synty Studios', 250.13, 12);
INSERT INTO  try_0."Products" (ProductID, ProductName, PublisherID, PublisherName, UnitPrice, UnitsInStock) 
VALUES (3, 'POLYGON Dungeon Realms', 1, 'Synty Studios', 133.99, 15);
INSERT INTO  try_0."Products" (ProductID, ProductName, PublisherID, PublisherName, UnitPrice, UnitsInStock) 
VALUES (4, 'Mega Animations Pack', 3, 'Keving Iglesias', 80.40, 20);
INSERT INTO  try_0."Products" (ProductID, ProductName, PublisherID, PublisherName, UnitPrice, UnitsInStock) 
VALUES (5, 'Polyquest Worlds Full Pack Vol.1', 4, 'POLYBOX', 267.99, 1);


------------------------------------

-- Customers
CREATE TABLE try_0."Customers"(
	CustomerID nchar(5) NOT NULL,
	FirstName varchar(40) NOT NULL,
	LastName varchar(40) NOT NULL,
	Country varchar(15) NOT NULL,
	Balance money null check(Balance >= '0.00'),
 CONSTRAINT PK_Customer PRIMARY KEY  
(
	CustomerID 
));

-- 2 vásárló
INSERT INTO try_0."Customers"  (CustomerID, FirstName, LastName, Country, Balance) VALUES ('PEBE0', 'Béla', 'Példa', 'Hungary', 200.00);
INSERT INTO try_0."Customers"  (CustomerID, FirstName, LastName, Country, Balance) VALUES ('JEBE0', 'Jeff', 'Bezos', 'America', 90000000000000000.00);


---------------------------------------

-- Orders
CREATE TABLE try_0."Orders"(
	OrderID integer NOT NULL,
	CustomerID nchar(5) NOT NULL references try_0."Customers"(customerid),
	OrderDate timestamp without time zone DEFAULT now()::timestamp NULL,
	ShippingID int NOT NULL references try_0."ShippingInfo"(ShippingID),
 CONSTRAINT PK_Orders PRIMARY KEY  
(
	OrderID 
));

-- nincs rendelésünk (üres a tábla)


---------------------------------------

-- OrderDetails
CREATE TABLE try_0."OrderDetails"(
	OrderID int NOT NULL references try_0."Orders"(OrderID),
	ProductID int NOT NULL references try_0."Products"(ProductID),
	UnitPrice money NOT NULL,
	Quantity smallint NOT NULL check(Quantity >= 0),
 CONSTRAINT PK_Order_Details PRIMARY KEY  
(
	orderid ,    
	productid 
));

-- nincs rendelésünk (üres a tábla)


---------------------------------------

-- ShippingInfo
CREATE TABLE try_0."ShippingInfo"(
	ShippingID integer NOT NULL,
	CustomerID nchar(5) NOT NULL references try_0."Customers"(customerid),
	ShipName varchar(40) NULL,
	ShipAddress varchar(60) NULL,
	ShipCity varchar(15) NULL,
	ShipRegion varchar(15) NULL,
	ShipPostalCode varchar(10) NULL,
	ShipCountry varchar(15) NULL,
 CONSTRAINT PK_Shipping_Info PRIMARY KEY
(
	ShippingID
));

-- nincs rendelésünk (üres a tábla)



-- ============== VIEWS ===============

-- Last 5 Orders
create or replace view try_0."last_orders" as
select o.orderdate::timestamp(0) without time zone AS orderdate, c.firstname, c.lastname, c.country, c.balance, p.productname, od.quantity, od.quantity * od.unitprice AS value, p.unitsinstock
from try_0."Products" p join try_0."OrderDetails" od on p.productid=od.productid
	join try_0."Orders" o on o.orderid=od.orderid
	join try_0."Customers" c on c.customerid=o.customerid
order by orderdate desc limit 5;



-- ============ FUNCTIONS =============

-- Get Shipping ID
create or replace function try_0."get_shipping_id" (var_custid char(5)) returns integer as
$$
declare var_stored_id integer;
begin
	select shippingid into var_stored_id from try_0."ShippingInfo" where customerid = var_custid;
	if var_stored_id IS NULL then
		return nextval('try_0."seq_shippings"');
	else
		return var_stored_id;
	end if;
end;
$$
language 'plpgsql';


-- Check order possibility
create or replace function try_0."check_order_possibility" (var_productid integer, var_quantity integer, var_custid char(5)) returns integer as
$$
declare var_stock integer; var_unitprice money; var_balance money;
begin
	select unitsinstock, unitprice into var_stock, var_unitprice from try_0."Products" where productid = var_productid;
	select balance into var_balance from try_0."Customers" where customerid = var_custid;
	if var_quantity * var_unitprice > var_balance or var_stock < var_quantity then
		raise notice 'Készlet vagy egyenleg hiba';
		return 1;
	else
		return 0;
	end if;
end;
$$
language 'plpgsql';


-- New Order
create or replace function try_0."new_order" (var_productid integer, var_quantity integer, var_custid char(5), var_shipping_id integer, var_ship_name varchar(40), var_ship_address varchar(60), var_ship_city varchar(15), var_ship_region varchar(15), var_ship_postal_code varchar(10), var_ship_country varchar(15)) returns integer as
$$
declare var_stock integer; var_unitprice money; var_balance money; var_orderid int; var_stored_shipping_id integer;
begin
	select unitsinstock, unitprice into var_stock, var_unitprice from try_0."Products" where productid = var_productid;
	select balance into var_balance from try_0."Customers" where customerid = var_custid;

	update try_0."Customers" set balance = balance - var_quantity * var_unitprice where customerid = var_custid;
	update try_0."Products" set unitsinstock = unitsinstock - var_quantity where productid = var_productid;

	select shippingid into var_stored_shipping_id from try_0."ShippingInfo" where customerid = var_custid;
	if var_stored_shipping_id IS NULL then
		insert into try_0."ShippingInfo" (shippingid, customerid, shipname, shipaddress, shipcity, shipregion, shippostalcode, shipcountry)
		values (var_shipping_id, var_custid, var_ship_name, var_ship_address, var_ship_city, var_ship_region, var_ship_postal_code, var_ship_country);
	else
		update try_0."ShippingInfo"
		set (shipname, shipaddress, shipcity, shipregion, shippostalcode, shipcountry)
			= (var_ship_name, var_ship_address, var_ship_city, var_ship_region, var_ship_postal_code, var_ship_country)
		where customerid = var_custid;
	end if;

	var_orderid := nextval('try_0."seq_orders"');
	insert into try_0."Orders" (orderid, customerid, shippingid) values (var_orderid, var_custid, var_shipping_id);
	insert into try_0."OrderDetails" (orderid, productid, unitprice, quantity) values (var_orderid, var_productid, var_unitprice, var_quantity);

	return 0;
end;
$$
language 'plpgsql';
