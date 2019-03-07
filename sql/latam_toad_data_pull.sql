sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
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
spo \\amscifs01\homefolders$\djohnson\Desktop\latam.csv
select 
ev.roc_text,ev.mid_name,ev.card_scheme,ev.card_type,ev.card_desc,ev.charge_type,ev.interchange_desc
,ev.issuing_ctry,ev.issuing_region,ev.volume,ev.flow,ev.interch_perc,ev.interch_fixed,ev.trans_date
,pa.receiveddate,pa.statusdate,ev.transaction_type,ev.TRANS_CURR,pa.CURRENCYCODE,pa.paymentamount
,ev.flow_usd,pa.orderid,pa.paymentreference,pa.statusid
,ev.contract_id,cco.merchantid,cco.orderid,cco.AUTHORISATIONDATETIME,cco.DATEAUTHORISATION
,cco.CREDITCARDCOMPANY,cco.CREDITDEBITINDICATOR,cco.CVVINDICATOR,cco.CVVRESULT,cco.CVVSERVICEINDICATOR
,cco.avs,cco.TERMINALID,cco.CREDITCARDNUMBER,cco.EXPIRYDATE,cco.ISSUENUMBER,cco.AUTHORISATIONCODE
,cco.AVSINDICATOR,cco.AVSRESULT,cco.FRAUDCODE,cco.FRAUDINDICATOR,cco.FRAUDRESULT
,cco.AUTHORISEDCURRENCYCODE,cco.AUTHORISEDAMOUNT,cco.Amount AS AMOUNT
,cco.name,cco.street,cco.housenumber,cco.additionaladdressinfo,cco.zip,cco.city,cco.state,cco.iin
,CVVINDICATOR_DESC,CVVRESULT_DESC,AVSRESULT_DESC
,ap.MERCHANTID,ap.ORDERID,ap.LEGDATE,ap.ORIGINAIRPORT,ap.ARRIVALAIRPORT
,ap.AIRLINECLASS,ap.CARRIERCODE,ap.FLIGHTNUMBER,ap.DEPARTURETIME
,itn.merchantid,itn.orderid,itn.RECEIVEDDATE,itn.ITINERARYTYPE,itn.AIRLINECODE
,itn.AIRLINENAME,itn.AIRLINEINVOICENUMBER,itn.TICKETNUMBER,itn.PASSENGERNAME,itn.POINTOFSALE
from fdwo.acquirer_elavon_usa_cost ev  
left join eps.opr_paymentattempt pa 
on 
CAST(ev.roc_text AS VARCHAR2(20))=pa.paymentreference 
left join
(
select co.merchantid,co.orderid,co.AUTHORISATIONDATETIME,co.DATEAUTHORISATION,co.CREDITCARDCOMPANY
,co.CREDITDEBITINDICATOR,co.CVVINDICATOR,co.CVVRESULT,co.CVVSERVICEINDICATOR
,co.avs,co.TERMINALID,co.CREDITCARDNUMBER,co.EXPIRYDATE,co.ISSUENUMBER,co.AUTHORISATIONCODE
,co.AVSINDICATOR,co.AVSRESULT,co.FRAUDCODE,co.FRAUDINDICATOR,co.FRAUDRESULT
,co.AUTHORISEDCURRENCYCODE,co.AUTHORISEDAMOUNT,co.Amount AS AMOUNT
,co.name,co.street,co.housenumber,co.additionaladdressinfo,co.zip,co.city,co.state,co.iin
,CASE WHEN co.CVVINDICATOR = 1 then 'CVV Checked'
WHEN co.CVVINDICATOR <> 1 then 'CVV Not Checked'
END AS "CVVINDICATOR_DESC"
,CASE WHEN co.CVVRESULT = 'M' THEN 'CVV Match'
WHEN co.CVVRESULT = 'N' THEN 'CVV NoMatch'
WHEN co.CVVRESULT not in ('N','M') THEN 'CVV Unknown'
END AS "CVVRESULT_DESC"
,CASE WHEN co.AVSRESULT in ('Z','A','W','D') THEN 'Partial AVS'
WHEN co.AVSRESULT in ('X','Y','M','F','P') THEN 'Full AVS'
WHEN co.AVSRESULT in ('N') THEN 'Neither ZIP nor address match'
WHEN co.AVSRESULT in ('I') THEN 'AVS not performed'
WHEN co.AVSRESULT in ('G') THEN 'Non-US. Issuer does not participate'
WHEN co.AVSRESULT IS NULL THEN 'No Result'
WHEN co.AVSRESULT in ('U','\','R','0','S') THEN 'Unsupp/Inconc AVS'
END AS "AVSRESULT_DESC"
from eps.PCO_CREDITCARDONLINE co
where co.merchantid in(3875,7965)
) cco
on pa.orderid=cco.orderid
left join
(
select idd.MERCHANTID,idd.ORDERID,idd.LEGDATE,idd.ORIGINAIRPORT,idd.ARRIVALAIRPORT,idd.AIRLINECLASS,idd.CARRIERCODE,idd.FLIGHTNUMBER,idd.DEPARTURETIME
from EPS.OPR_ITINERARYDETAIL idd
where idd.merchantid in(3875,7965)
and idd.SEQUENCENUMBER=1
)ap
on pa.orderid=ap.orderid
and ev.contract_id=ap.merchantid
left join
(
select it.merchantid,it.orderid,it.RECEIVEDDATE,it.ITINERARYTYPE,it.AIRLINECODE,it.AIRLINENAME,it.AIRLINEINVOICENUMBER,it.TICKETNUMBER,it.PASSENGERNAME,it.POINTOFSALE
from EPS.OPR_ITINERARY it
where it.merchantid in(3875,7965)
)itn
on pa.orderid=itn.orderid
and ev.contract_id=itn.merchantid
WHERE ev.transaction_type='TRANSACTION'
AND ev.roc_text IS NOT NULL
AND pa.receiveddate BETWEEN TO_DATE('01/01/2017','MM/DD/YYYY') AND TO_DATE('06/12/2018','MM/DD/YYYY')
AND ev.CONTRACT_ID in(3875,7965)
AND pa.STATUSID=1050
AND ev.issuing_ctry='US'
AND cco.CREDITDEBITINDICATOR='C';
spo end