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
CC.ORDERID AS VOLUME
,CC.CURRENCY,CC.MERCHANTID
,CC.AMOUNT/100 AS FLOW_AMOUNT_TRXN_CURRENCY,ER.EUR_EX_RATE,((CC.AMOUNT/100)/ER.EUR_EX_RATE) AS FLOW_AMOUNT_EUR
,MM.CLIENT_NAME,MM.CLIENT_ID,MM.SALES_REGION,MM.MCC,CC.IIN,MM.INVOICE_RELATION_ID,
CASE 
    WHEN SA.SERVICEACCOUNTNAME LIKE '%Wells%' THEN 'Wells Fargo' 
    WHEN SA.SERVICEACCOUNTNAME LIKE '%Litle%' THEN 'Vantiv'
    WHEN SA.SERVICEACCOUNTNAME LIKE '%Vantiv Visa%' THEN 'Vantiv'
    WHEN SA.SERVICEACCOUNTNAME LIKE '%Firstdata%' THEN 'Firstdata'
    WHEN SA.SERVICEACCOUNTNAME LIKE '%Payvision%' THEN 'Payvision'  
END AS ACQUIRER
,BT.ISSUER_COUNTRY,BT.CONS_COMM,CC.CREDITCARDCOMPANY,PD.PRODUCT_CODE,CC.INVOICENUMBER,
CASE 
    WHEN CC.AVSRESULT in ('Z','A','W','D') THEN 'Partial AVS'
    WHEN CC.AVSRESULT in ('X','Y','M','F','P') THEN 'Full AVS'
    WHEN CC.AVSRESULT in ('N') THEN 'Neither ZIP nor address match'
    WHEN CC.AVSRESULT in ('G') THEN 'Non-US Issuer does not participate'
    WHEN CC.AVSRESULT IS NULL THEN 'No Result'
    WHEN CC.AVSRESULT in ('U','R','0','S','I') THEN 'AVS Not Performed'
END AS AVSRESULT
,oo.Line_item_total,oo.Discount,oo.Quantity,oo.Unit_Cost,oo.Unit_of_measure
,oo.Product_Code,oo.Item_Commodity_Code,oo.Item_Descriptor,oo.Product_Type,oo.Tax
from EPS.PCO_CREDITCARDONLINE cc
left join
(select ex.CURRENCY,AVG(EX.AVERAGE_RATE_EUR) AS EUR_EX_RATE 
from FDWO.MB_EXCHANGE_RATES ex
where EX.DAY between to_date('9/1/2018','MM/DD/YYYY') and to_date('9/30/2018','MM/DD/YYYY')
group by EX.CURRENCY ) er
on CC.CURRENCY=er.CURRENCY
left join fdwo.MB_BIN_TABLE_FULL BT
on CC.IIN=BT.BIN
left join 
(select pl.merchantid,pl.orderid,pl.attemptid,pl.statusid,PL.REQUESTAMOUNT,PL.EFFORTID 
from EPS.OPR_PAYMENTATTEMPT pl
where pl.receiveddate between to_date('09/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')
group by pl.merchantid,pl.orderid,pl.attemptid,pl.statusid,PL.REQUESTAMOUNT,PL.EFFORTID ) pa
ON cc.MERCHANTID=pa.MERCHANTID
AND cc.ORDERID=pa.ORDERID
AND cc.ATTEMPTID=PA.ATTEMPTID
AND CC.EFFORTID=PA.EFFORTID
and CC.AMOUNT=PA.REQUESTAMOUNT
left join FDWO.MB_MERCHANTS mm
on CAST(CC.MERCHANTID AS VARCHAR2(10))=MM.CONTRACT_ID
left join EPS.GPM_SERVICEACCOUNT sa
on CC.PAYMENTPROCESSOR=SA.PAYMENTPROCESSORNUMBER
left join 
(select PT.ORDERID,PT.ATTEMPTID,PT.EFFORTID,PT.TRANSACTION_TYPE,PT.PRODUCT_CODE,PT.CONTRACT_ID
from fdwo.cc_processing_data_pt pt
where PT.TRANSACTION_DATE between to_date('9/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')
group by PT.ORDERID,PT.ATTEMPTID,PT.EFFORTID,PT.TRANSACTION_TYPE,PT.PRODUCT_CODE,pt.contract_ID) pd
on CC.ORDERID = pd.ORDERID
and cc.MERCHANTID=pd.CONTRACT_ID
and CC.ATTEMPTID = pd.ATTEMPTID
and CC.EFFORTID=pd.ATTEMPTID
left join
(select O.ORDERID,O.MERCHANTID,O.AMOUNT,OL.LINEAMOUNTTOTAL/100 AS Line_item_total
,OL.DISCOUNTAMOUNT/100 AS Discount,OL.QUANTITY AS Quantity,OL.PRODUCTPRICE/100 AS Unit_Cost
,OL.UNIT AS Unit_of_measure,OL.PRODUCTCODE AS Product_Code,OL.ITEMID AS Item_Commodity_Code
,OL.PRODUCTNAME AS Item_Descriptor,OL.PRODUCTTYPE AS Product_Type,OL.TAXAMOUNT AS Tax
from EPS.OPR_ORDER o
left join
EPS.OPR_ORDERLINE ol
on O.ORDERID=OL.ORDERID
and O.MERCHANTID=OL.MERCHANTID
where O.RECEIVEDDATE between to_date('09/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')) oo
on cc.ORDERID=oo.ORDERID
and cc.MERCHANTID=oo.MERCHANTID
and cc.AMOUNT=oo.AMOUNT
where CC.PAYMENTPROCESSOR IN(223,346,250,281,283,302,372)
and CC.AUTHORISATIONDATETIME between to_date('09/1/2017','MM/DD/YYYY') and to_date('8/31/2018','MM/DD/YYYY')
and CC.CREDITCARDCOMPANY='VISA'
and CC.CURRENCY='USD'
and BT.CONS_COMM='COMMERCIAL' 
and BT.ISSUER_COUNTRY='UNITED STATES OF AMERICA'
and PA.STATUSID=1050
--and rownum<1000
group by 
CC.ORDERID,CC.CURRENCY,CC.MERCHANTID,cc.AMOUNT/100,ER.EUR_EX_RATE,((CC.AMOUNT/100)/ER.EUR_EX_RATE)
,MM.CLIENT_NAME,MM.CLIENT_ID,MM.SALES_REGION,MM.MCC,CC.IIN,MM.INVOICE_RELATION_ID,SA.SERVICEACCOUNTNAME
,cc.AVSRESULT,BT.ISSUER_COUNTRY,BT.CONS_COMM,CC.CREDITCARDCOMPANY,PD.PRODUCT_CODE,CC.INVOICENUMBER
,oo.Line_item_total,oo.Discount,oo.Quantity,oo.Unit_Cost,oo.Unit_of_measure
,oo.Product_Code,oo.Item_Commodity_Code,oo.Item_Descriptor,oo.Product_Type,oo.Tax;
spo end