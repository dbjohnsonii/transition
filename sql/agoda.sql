sqlplus/nolog
connect djohnson/RhiBae01!@ODSPEU1.ams
set serveroutput on size unlimited
set linesize 300
set trim on
set pagesize 0
set heading on
spo d:\djohnson\Desktop\agoda_raw_data.csv
select mm.merchantname ||';'||co.merchantid ||';'|| co.orderid ||';'|| pa.statusid
||';'|| co.dateauthorisation ||';'|| pa.statusdate ||';'|| co.merchantnumber ||';'|| co.paymentprocessor ||';'|| sa.serviceaccountname
||';'|| co.creditcardcompany ||';'|| co.amount ||';'|| co.currency ||';'|| co.authorisationcode ||';'|| co.avsindicator
||';'|| co.name ||';'|| co.street ||';'|| co.additionaladdressinfo ||';'|| co.zip ||';'|| co.city 
||';'|| co.countrycode ||';'|| co.state ||';'||co.IIN||';'||pp.card_class_bin||';'||pp.cons_corp_bin||';'||pp.issuer_country_bin ||';'||
CASE WHEN CVVINDICATOR = 1 then 'CVV Checked'
WHEN CVVINDICATOR <> 1 then 'CVV Not Checked'
END ||';'||
CASE WHEN co.CVVRESULT = 'M' THEN 'CVV Match'
WHEN co.CVVRESULT = 'N' THEN 'CVV NoMatch'
WHEN co.CVVRESULT not in ('N','M') THEN 'CVV Unknown'
END ||';'||
CASE WHEN AVSRESULT in ('Z','A','W','D') THEN 'Partial AVS'
WHEN AVSRESULT in ('X','Y','M','F','P') THEN 'Full AVS'
WHEN AVSRESULT in ('N') THEN 'Neither ZIP nor address match'
WHEN AVSRESULT in ('I') THEN 'Not verified for Intl trxn'
WHEN AVSRESULT in ('U','G','R','0','S') THEN 'Unsupp/Inconc AVS'
END
from eps.pco_creditcardonline co
left join eps.mrm_merchant mm
on co.merchantid=mm.merchantid
left join eps.opr_paymentattempt pa
on co.merchantid=pa.merchantid
and co.orderid=pa.orderid
and co.effortid=pa.effortid
and co.attemptid=pa.attemptid
and co.amount=pa.amount
and co.currency=pa.currencycode
left join eps.gpm_serviceaccount sa
on co.paymentprocessor=sa.paymentprocessornumber
left join fdwo.cc_processing_data_pt pp
on co.IIN=pp.bin
and co.orderid=pp.orderid
and co.merchantid=pp.contract_id
where dateauthorisation between to_date('1/1/2018','MM/DD/YYYY') and to_date('2/26/2018','MM/DD/YYYY') 
and co.merchantid=6485
and co.paymentprocessor=223
and pa.statusid=1050
group by mm.merchantname,co.merchantid,co.orderid,pa.statusid
,co.dateauthorisation,pa.statusdate,co.merchantnumber,co.paymentprocessor,sa.serviceaccountname
,co.creditcardcompany,co.amount,co.currency,co.authorisationcode,co.avsindicator
,co.name,co.street,co.additionaladdressinfo,co.zip,co.city 
,co.countrycode,co.state,co.IIN,pp.card_class_bin,pp.cons_corp_bin,pp.issuer_country_bin
,co.CVVINDICATOR,co.CVVRESULT,co.AVSRESULT;
spo end

