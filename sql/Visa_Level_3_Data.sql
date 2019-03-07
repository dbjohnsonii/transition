sqlplus/nolog
connect djohnson/KirkyRhi9860!@ODSPEU1.ams
set echo off
set feedback off
set colsep ';'
set sqlprompt ''
set headsep off
set serveroutput on size unlimited
set linesize 30000
set trimspool on
set pagesize 0
set heading on
set trimout on
set wrap off
set termout off
spo U:\level_3_data.txt
select 
--data
CC.MERCHANTID
--calculation
,COUNT(CC.ORDERID) AS VOLUME
--data
,CC.IIN,CC.CREDITCARDCOMPANY,CC.PAYMENTPROCESSOR,CC.CURRENCY AS TRXN_CURRENCY
--calculation
,SUM(CC.AMOUNT/100) AS FLOW_AMOUNT_TRXN_CURRENCY
--data
,ER.EUR_EX_RATE
--calculation
,SUM((CC.AMOUNT/100)/ER.EUR_EX_RATE) AS FLOW_AMOUNT_EUR
--data
--,O.MERCHANTID,O.ORDERID
--calculation 
,count(O.LINEAMOUNTTOTAL/100) AS Line_item_total
,count(O.DISCOUNTAMOUNT/100) AS Discount
,count(O.QUANTITY) AS Quantity
,count(O.PRODUCTPRICE/100) AS Unit_Cost
,count(O.UNIT) AS Unit_of_measure
,count(O.PRODUCTCODE) AS Product_Code
,count(O.ITEMID) AS Item_Commodity_Code
,count(O.PRODUCTNAME) AS Item_Descriptor
,count(O.PRODUCTTYPE) AS Product_Type
--data
,SA.SERVICEACCOUNTNAME,MM.CLIENT_NAME,MM.CLIENT_ID,MM.SALES_REGION,MM.MCC
,PP.INTERCHANGE_REGION,pd.TRANSACTION_TYPE,pd.PRODUCT_CODE,MM.INVOICE_RELATION_ID
,BT.CONS_COMM,BT.ISSUER_COUNTRY
--joins and criteria
from EPS.PCO_CREDITCARDONLINE cc
left join eps.OPR_ORDERLINE o
on CC.MERCHANTID=O.MERCHANTID
and CC.ORDERID=O.ORDERID
left join FDWO.MB_PAYMENTPROCESSOR pp
on cc.PAYMENTPROCESSOR=pp.paymentprocessor_id
left join EPS.GPM_SERVICEACCOUNT sa
on CC.PAYMENTPROCESSOR=SA.PAYMENTPROCESSORNUMBER
left join FDWO.MB_MERCHANTS mm
on CAST(CC.MERCHANTID AS VARCHAR2(10))=MM.CONTRACT_ID
left join 
(select PT.ORDERID,PT.ATTEMPTID,PT.EFFORTID,PT.TRANSACTION_TYPE,PT.PRODUCT_CODE 
from fdwo.cc_processing_data_pt pt
where PT.TRANSACTION_DATE between to_date('9/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')) pd
on CC.ORDERID = pd.ORDERID
and CC.ATTEMPTID = pd.ATTEMPTID
and CC.EFFORTID=pd.ATTEMPTID
left join fdwo.MB_BIN_TABLE_FULL BT
on CC.IIN=BT.BIN
left join
(select ex.CURRENCY,AVG(EX.AVERAGE_RATE_EUR) AS EUR_EX_RATE 
from FDWO.MB_EXCHANGE_RATES ex
where EX.DAY between to_date('9/1/2018','MM/DD/YYYY') and to_date('9/30/2018','MM/DD/YYYY')
group by EX.CURRENCY ) er
on CC.CURRENCY=er.CURRENCY
left join 
(select pl.merchantid,pl.orderid,pl.attemptid,pl.statusid 
from EPS.OPR_PAYMENTATTEMPT pl 
where pl.receiveddate between to_date('09/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')
group by pl.merchantid,pl.orderid,pl.attemptid,pl.statusid) pa
ON cc.MERCHANTID=pa.MERCHANTID
AND cc.ORDERID=pa.ORDERID
AND cc.ATTEMPTID=PA.ATTEMPTID
where CC.AUTHORISATIONDATETIME between to_date('09/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')
and PA.STATUSID=1050
and pp.interchange_region IN('NorthAm') --only looks at interchange in Northam
and CC.CREDITCARDCOMPANY='VISA' --only looks at Visa cards, MasterCard not subject to this fee
and SA.SERVICEACCOUNTNAME NOT in ('RetailDecisions HS','PagoCC') --excludes fraud account names
and PD.TRANSACTION_TYPE='TRANSACTION' --only looks at sales transactions
and BT.CONS_COMM='COMMERCIAL' --only looks at commercial cards
and BT.ISSUER_COUNTRY='UNITED STATES OF AMERICA'
and CC.CURRENCY='USD'
and CC.PAYMENTPROCESSOR IN(223,346,250,281,283,302,372) --excludes elavon since airlines are not subject to this fee
--and (O.MERCHANTID is not null or O.ORDERID is not null) --if credit card online doesnt match the orderline time then don't include the information
group by
CC.MERCHANTID,CC.IIN,CC.CREDITCARDCOMPANY,CC.PAYMENTPROCESSOR,CC.CURRENCY,O.MERCHANTID
,SA.SERVICEACCOUNTNAME,MM.CLIENT_NAME,MM.CLIENT_ID,MM.SALES_REGION,MM.MCC
,PP.INTERCHANGE_REGION,pd.TRANSACTION_TYPE,pd.PRODUCT_CODE,MM.INVOICE_RELATION_ID,ER.EUR_EX_RATE
,BT.CONS_COMM,BT.ISSUER_COUNTRY,O.ORDERID;
spo end