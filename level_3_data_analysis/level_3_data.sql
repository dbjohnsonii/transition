select 
O.MERCHANTID
,O.ORDERID
,O.CURRENCYCODE AS currency
,O.LINEAMOUNTTOTAL/100 AS Line_item_total
,O.DISCOUNTAMOUNT/100 AS Discount
,O.QUANTITY as Quantity
,O.PRODUCTPRICE/100 AS Unit_Cost
,O.UNIT as Unit_of_measure
,O.PRODUCTCODE as Product_Code
,O.ITEMID as Item_Commodity_Code
,O.PRODUCTNAME as Item_Descriptor
,O.PRODUCTTYPE as Product_Type
,O.INVOICELINEDATA
from eps.OPR_ORDERLINE o
where o.QUANTITY>0
and O.PRODUCTPRICE>0
and O.PRODUCTCODE is not null