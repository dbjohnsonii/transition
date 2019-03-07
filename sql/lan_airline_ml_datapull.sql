sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
set echo off
set feedback off
set colsep ';'
set sqlprompt ''
set headsep off
set serveroutput on size unlimited
set linesize 32767
set trimspool on
set pagesize 0
set heading on
set trimout on
set wrap off
set termout off
set long 1000000000
spo \\amscifs01\homefolders$\djohnson\Desktop\latam.csv
SELECT
  t1.mid_name,t1.roc_text,t1.paymentreference,t1.orderid,t1.trans_date
 ,t1.receiveddate,t2.AUTHORISATIONDATETIME,t2.DATEAUTHORISATION,t1.statusdate,t1.transaction_type 
 ,t1.interchange_desc,t1.card_scheme,t2.iin,t1.card_type,t1.card_desc,t1.charge_type
 ,t1.issuing_ctry,t1.issuing_region  
 ,t1.interch_perc,t1.interch_fixed,t2.CREDITDEBITINDICATOR
 ,t1.CURRENCYCODE,t1.flow_usd,t2.AUTHORISEDAMOUNT,t2.AMOUNT,t2.AMOUNT2
 ,t2.terminalid,t2.CREDITCARDNUMBER,t2.EXPIRYDATE,t2.ISSUENUMBER,t2.AUTHORISATIONCODE
 ,t2.CVVINDICATOR,t2.CVVRESULT,t2.CVVSERVICEINDICATOR
 ,t2.AVS,t2.AVSINDICATOR,t2.AVSRESULT
 ,t2.FRAUDCODE,t2.FRAUDINDICATOR,t2.FRAUDRESULT
 ,t2.name,t2.street,t2.housenumber,t2.additionaladdressinfo,t2.zip,t2.city,t2.state
 ,t3.MERCHANTID,t3.ORDERID,t3.LEGDATE,t3.ORIGINAIRPORT,t3.ARRIVALAIRPORT,t3.AIRLINECLASS,t3.CARRIERCODE,t3.FLIGHTNUMBER,t3.DEPARTURETIME
 ,t4.merchantid,t4.orderid,t4.receiveddate,t4.ITINERARYTYPE,t4.AIRLINECODE,t4.AIRLINENAME,t4.AIRLINEINVOICENUMBER,t4.TICKETNUMBER,t4.PASSENGERNAME,t4.POINTOFSALE
 ,
CASE WHEN t2.CVVINDICATOR = 1 then 'CVV Checked'
WHEN t2.CVVINDICATOR <> 1 then 'CVV Not Checked'
END AS "CVVINDICATOR",
CASE WHEN t2.CVVRESULT = 'M' THEN 'CVV Match'
WHEN t2.CVVRESULT = 'N' THEN 'CVV NoMatch'
WHEN t2.CVVRESULT not in ('N','M') THEN 'CVV Unknown'
END AS "CVVRESULT",
CASE WHEN t2.AVSRESULT in ('Z','A','W','D') THEN 'Partial AVS'
WHEN t2.AVSRESULT in ('X','Y','M','F','P') THEN 'Full AVS'
WHEN t2.AVSRESULT in ('N') THEN 'Neither ZIP nor address match'
WHEN t2.AVSRESULT in ('I') THEN 'Information not verified for international transaction'
WHEN t2.AVSRESULT in ('G') THEN 'Non-US. Issuer does not participate'
WHEN t2.AVSRESULT IS NULL THEN 'No Result'
WHEN t2.AVSRESULT in ('U','\','R','0','S') THEN 'Unsupp/Inconc AVS'
END AS "AVSRESULT"  
FROM
(  
  select 
  ev.roc_text,ev.mid_name,ev.card_scheme,ev.card_type,ev.card_desc,ev.charge_type,ev.interchange_desc
  ,ev.issuing_ctry,ev.issuing_region,ev.volume,ev.flow,ev.interch_perc,ev.interch_fixed,ev.trans_date
  ,pa.receiveddate,pa.statusdate,ev.transaction_type,ev.TRANS_CURR,pa.CURRENCYCODE,pa.paymentamount
  ,ev.flow_usd,pa.orderid,pa.paymentreference,pa.statusid
  ,ev.contract_id
  from 
  fdwo.acquirer_elavon_usa_cost ev  
  left join
  eps.opr_paymentattempt pa 
  on 
  CAST(ev.roc_text AS VARCHAR2(20))=pa.paymentreference 
  WHERE ev.transaction_type='TRANSACTION'
  AND ev.roc_text IS NOT NULL
  AND ev.trans_date BETWEEN TO_DATE('04/01/2017','MM/DD/YYYY') AND TO_DATE('05/31/2018','MM/DD/YYYY')
  AND ev.CONTRACT_ID=3875
  AND pa.STATUSID=1050
  )t1
  LEFT JOIN
  (
  SELECT 
   co.merchantid,co.orderid,co.AUTHORISATIONDATETIME,co.DATEAUTHORISATION,co.CREDITCARDCOMPANY
  ,co.CREDITDEBITINDICATOR,co.CVVINDICATOR,co.CVVRESULT,co.CVVSERVICEINDICATOR  
  ,co.avs,co.TERMINALID,co.CREDITCARDNUMBER,co.EXPIRYDATE,co.ISSUENUMBER,co.AUTHORISATIONCODE
  ,co.AVSINDICATOR,co.AVSRESULT,co.FRAUDCODE,co.FRAUDINDICATOR,co.FRAUDRESULT
  ,co.AUTHORISEDCURRENCYCODE,co.AUTHORISEDAMOUNT,co.Amount AS AMOUNT,co.Amount AS AMOUNT2
  ,co.name,co.street,co.housenumber,co.additionaladdressinfo,co.zip,co.city,co.state,co.iin
  FROM EPS.PCO_CREDITCARDONLINE co
  where merchantid=3875
  and authorisationdatetime BETWEEN TO_DATE('04/01/2017','MM/DD/YYYY') AND TO_DATE('05/31/2018','MM/DD/YYYY') --Go back two weeks for this one difference in status and auth and trans date
  )t2
  ON t1.orderid=t2.orderid
  LEFT JOIN
  (
  select idd.MERCHANTID,idd.ORDERID,idd.LEGDATE,idd.ORIGINAIRPORT,idd.ARRIVALAIRPORT,idd.AIRLINECLASS,idd.CARRIERCODE,idd.FLIGHTNUMBER,idd.DEPARTURETIME
  from EPS.OPR_ITINERARYDETAIL idd
  where merchantid=3875
  and idd.SEQUENCENUMBER=1
  )t3
  ON t1.orderid=t3.orderid
  and t1.contract_id=t3.merchantid
  LEFT JOIN
  (
  select it.merchantid,it.orderid,it.RECEIVEDDATE,it.ITINERARYTYPE,it.AIRLINECODE,it.AIRLINENAME,it.AIRLINEINVOICENUMBER,it.TICKETNUMBER,it.PASSENGERNAME,it.POINTOFSALE
  from EPS.OPR_ITINERARY it
  where merchantid=3875
  )t4
  ON t1.orderid=t4.orderid
  and t1.contract_id=t4.merchantid
  where issuing_ctry='US';
spo end