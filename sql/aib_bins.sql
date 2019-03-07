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
spo \\amscifs01\homefolders$\djohnson\Desktop\aib_bins.csv
SELECT 
ab.issuer_bin
,ab.INTERCHANGE_RATE_DESCRIPTION
,ab.INTERCHANGE_RATE_AMOUNT
,ab.INTERCHANGE_RATE_PERC
FROM fdwo.acquirer_aib_newgen_files ab
WHERE ab.transaction_date BETWEEN TO_DATE('01-01-2017','MM-DD-YYYY') AND TO_DATE('04-30-2018','MM-DD-YYYY')
WHERE PROCESSING_STATUS='Processed'
AND ab.scheme_fee_eur!=0
AND (ab.transaction_type='Sale')
AND (ab.interchange_region='Domestic')
GROUP BY
ab.issuer_bin
,ab.INTERCHANGE_RATE_AMOUNT
,ab.INTERCHANGE_RATE_PERC
,ab.INTERCHANGE_RATE_DESCRIPTION; 
spool off end