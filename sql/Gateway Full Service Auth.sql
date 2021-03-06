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
spo U:\gwfs_auth.txt
select*
from(
select t1.*,t2.NULLCOUNT,t3.NOTNULLCOUNT
from
(
select SERVICEACCOUNTNAME,CREDITCARDCOMPANY,IIN,VERTICAL,CURRENCY,CLIENT_NAME,COUNT(*) AS TOTAL_COUNT
from
(
select CC.SERVICEPROVIDERID,CC.AUTHORISATIONCODE,CC.PAYMENTPROCESSOR,SA.SERVICEACCOUNTNAME
,CC.CREDITCARDCOMPANY,CC.IIN,MM.VERTICAL,CC.CURRENCY,MM.CLIENT_NAME
from EPS.PCO_CREDITCARDONLINE cc
left join EPS.GPM_SERVICEACCOUNT sa
on CC.SERVICEPROVIDERID=SA.SERVICEPROVIDERID
and CC.PAYMENTPROCESSOR=SA.PAYMENTPROCESSORNUMBER
left join FDWO.MB_MERCHANTS mm
on CAST(CC.MERCHANTID as VARCHAR(25))=MM.CONTRACT_ID
where CC.SERVICEPROVIDERID is not null
and CC.DATEAUTHORISATION between to_date('11/1/2018','MM/DD/YYYY') and to_date('11/30/2018','MM/DD/YYYY')
)
GROUP BY SERVICEACCOUNTNAME,CREDITCARDCOMPANY,IIN,VERTICAL,CURRENCY,CLIENT_NAME
)t1
left join
(
select SERVICEACCOUNTNAME,CREDITCARDCOMPANY,IIN,VERTICAL,CURRENCY,CLIENT_NAME,COUNT(*) AS NULLCOUNT
from
(
select CC.SERVICEPROVIDERID,CC.AUTHORISATIONCODE,CC.PAYMENTPROCESSOR,SA.SERVICEACCOUNTNAME,CC.CREDITCARDCOMPANY,CC.IIN,MM.VERTICAL,cc.CURRENCY,
MM.CLIENT_NAME
from EPS.PCO_CREDITCARDONLINE cc
left join EPS.GPM_SERVICEACCOUNT sa
on CC.SERVICEPROVIDERID=SA.SERVICEPROVIDERID
and CC.PAYMENTPROCESSOR=SA.PAYMENTPROCESSORNUMBER
left join FDWO.MB_MERCHANTS mm
on CAST(CC.MERCHANTID as VARCHAR(25))=MM.CONTRACT_ID
where CC.SERVICEPROVIDERID is not null
and CC.DATEAUTHORISATION between to_date('11/1/2018','MM/DD/YYYY') and to_date('11/30/2018','MM/DD/YYYY')
and AUTHORISATIONCODE is null
)
GROUP BY SERVICEACCOUNTNAME,CREDITCARDCOMPANY,IIN,VERTICAL,CURRENCY,CLIENT_NAME
)t2
on t1.SERVICEACCOUNTNAME=t2.SERVICEACCOUNTNAME
and t1.CREDITCARDCOMPANY=t2.CREDITCARDCOMPANY
and t1.VERTICAL=t2.VERTICAL
and t1.CURRENCY=t2.CURRENCY
and t1.CLIENT_NAME=t2.CLIENT_NAME
and t1.IIN=t2.IIN
left join
(
select SERVICEACCOUNTNAME,CREDITCARDCOMPANY,IIN,VERTICAL,CURRENCY,CLIENT_NAME,COUNT(*) AS NOTNULLCOUNT
from
(
select CC.SERVICEPROVIDERID,CC.AUTHORISATIONCODE,CC.PAYMENTPROCESSOR,SA.SERVICEACCOUNTNAME,CC.CREDITCARDCOMPANY,CC.IIN,MM.VERTICAL,CC.CURRENCY,MM.CLIENT_NAME
from EPS.PCO_CREDITCARDONLINE cc
left join EPS.GPM_SERVICEACCOUNT sa
on CC.SERVICEPROVIDERID=SA.SERVICEPROVIDERID
and CC.PAYMENTPROCESSOR=SA.PAYMENTPROCESSORNUMBER
left join FDWO.MB_MERCHANTS mm
on CAST(CC.MERCHANTID as VARCHAR(25))=MM.CONTRACT_ID
where CC.SERVICEPROVIDERID is not null
and CC.DATEAUTHORISATION between to_date('11/1/2018','MM/DD/YYYY') and to_date('11/30/2018','MM/DD/YYYY')
and AUTHORISATIONCODE is not null
)
GROUP BY SERVICEACCOUNTNAME,CREDITCARDCOMPANY,IIN,VERTICAL,CURRENCY,CLIENT_NAME      
)t3
on t1.SERVICEACCOUNTNAME=t3.SERVICEACCOUNTNAME
and t1.CREDITCARDCOMPANY=t3.CREDITCARDCOMPANY
and t1.VERTICAL=t3.VERTICAL
and t1.CURRENCY=t3.CURRENCY
and t1.CLIENT_NAME=t3.CLIENT_NAME
and t1.IIN=t3.IIN
);
spo end