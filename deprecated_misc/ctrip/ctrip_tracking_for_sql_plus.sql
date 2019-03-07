sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
set serveroutput on size unlimited
set linesize 300
set trim on
set pagesize 0
set heading on
spo d:\djohnson\Desktop\ctriptracking.csv
SELECT 
         pa.STATUSID
        ||';'||PA.RECEIVEDDATE
	||';'||CO.DATEAUTHORISATION
	||';'||PA.SENDDATE
	||';'||PA.PAYMENTDATE
	||';'||PA.STATUSDATE
        ||';'||co.MERCHANTID
	||';'||mm.MERCHANTNAME
	||';'||co.ORDERID
	||';'||co.CREDITCARDCOMPANY
        ||';'||co.CREDITDEBITINDICATOR
	||';'||co.CVVINDICATOR
	||';'||co.CVVRESULT
	||';'||co.CVVSERVICEINDICATOR
	||';'||co.AVSINDICATOR
	||';'||co.AVSRESULT
	||';'||co.FRAUDCODE
	||';'||co.FRAUDINDICATOR
	||';'||co.FRAUDRESULT
        ||';'||co.STTINDICATOR
        ||';'||co.MERCHANTREFERENCE
	||';'|| pa.PAYMENTREFERENCE
        ||';'||co.CUSTOMERID
	||';'||co.COUNTRYCODE
        ||';'||co.AUTHORISEDCURRENCYCODE
	||';'||co.AUTHORISEDAMOUNT
	||';'||co.AMOUNT
        ||';'||o.SURNAME
	||';'||o.CITY
	||';'||o.PREFIXSURNAME
	||';'||o.STREET
	||';'||o.ZIP
	||';'||o.STATE
        ||';'||sp.PROVIDERNAME
	||';'||co.PAYMENTPROCESSOR
	||';'||co.SERVICEPROVIDERID
	||';'||pa.PAYMENTMETHODID
	||';'||pa.PAYMENTPRODUCTID
	||';'||co.IIN
	||';'||
        CASE WHEN co.CVVINDICATOR = 1 then 'CVV Checked'
        WHEN co.CVVINDICATOR <> 1 then 'CVV Not Checked'
        END
	||';'||
        CASE WHEN co.CVVRESULT = 'M' THEN 'CVV Match'
        WHEN co.CVVRESULT = 'N' THEN 'CVV NoMatch'
        WHEN co.CVVRESULT not in ('N'||';'||'M') THEN 'CVV Unknown'
        END
	||';'||
        CASE WHEN co.AVSRESULT in ('Z','A','W','D') THEN 'Partial AVS'
        WHEN co.AVSRESULT in ('X','Y','M','F','P') THEN 'Full AVS'
        WHEN co.AVSRESULT in ('N') THEN 'Neither ZIP nor address match'
        WHEN co.AVSRESULT in ('I') THEN 'Not verified for Intl trxn'
        WHEN co.AVSRESULT in ('U','G','R','0','S') THEN 'Unsupp/Inconc AVS'
        END
        ||';'||v.AVS_RESPONSE_MESSAGE
	||';'||v.CONS_CORP_BIN
	||';'||V.INTERCHANGE_RATE
	||';'||v.INTERCHANGE_PERCENT_RATE
	||';'||v.INTERCHANGE_FLAT_RATE
        ||';'||v.TRANSACTION_FLOW
	||';'||v.ISSUING_BANK
	||';'||V.CARD_SCHEME_BIN
	||';'||V.CRED_DEB_BIN
FROM EPS.PCO_CREDITCARDONLINE co
LEFT JOIN 
EPS.OPR_ORDER o
ON co.ORDERID=o.ORDERID
AND co.AMOUNT=o.AMOUNT
AND co.MERCHANTID=o.MERCHANTID
AND  co.AUTHORISEDCURRENCYCODE=o.CURRENCYCODE
LEFT JOIN EPS.GPM_SERVICEPROVIDER sp
ON co.SERVICEPROVIDERID=sp.SERVICEPROVIDERID
LEFT JOIN EPS.OPR_PAYMENTATTEMPT pa
ON co.MERCHANTID=pa.MERCHANTID
AND co.AMOUNT=pa.AMOUNT
AND co.ORDERID=pa.ORDERID
AND co.AUTHORISEDCURRENCYCODE=pa.CURRENCYCODE
AND co.ATTEMPTID=pa.ATTEMPTID
AND co.EFFORTID=pa.EFFORTID
LEFT JOIN FDWO.ACQUIRER_VANTIV_COST v
ON co.ORDERID=v.ORDER_ID
AND co.MERCHANTID=v.CONTRACT_ID
AND co.AMOUNT=v.TRANSACTION_FLOW*100
LEFT JOIN EPS.MRM_MERCHANT mm
ON CO.MERCHANTID=mm.MERCHANTID
WHERE co.AUTHORISATIONDATETIME>=TO_DATE('2018-01-01','YYYY-MM-DD')
AND sp.PROVIDERDESCRIPTION LIKE '%Litle%'
AND co.MERCHANTID=4856
AND PA.STATUSID=1050;
spo end