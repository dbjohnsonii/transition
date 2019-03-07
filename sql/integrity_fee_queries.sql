sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
set serveroutput on size unlimited
set linesize 300
SET TRIM ON
set pagesize 0
SET HEADING ON
spo d:\djohnson\Desktop\vantiv_integrity_fee.csv
SELECT MERCHANT||';'||TRANSACTION_TYPE||';'||INTERCHANGE_RATE||';'||INTERCHANGE_FLAT_RATE
||';'||INTERCHANGE_PERCENT_RATE||';'||SUM(TRANSACTION_FLOW_EUR)||';'||SUM(INTERCHANGE_EUR)||';'||COUNT(ORDER_ID) 
FROM fdwo.acquirer_vantiv_cost
WHERE TRANSACTION_TYPE='TRANSACTION'
AND TRANSACTION_DATE BETWEEN TO_DATE('3/01/2017','MM/DD/YYYY')AND TO_DATE('2/28/2018','MM/DD/YYYY')
GROUP BY MERCHANT, TRANSACTION_TYPE, INTERCHANGE_RATE,INTERCHANGE_FLAT_RATE,INTERCHANGE_PERCENT_RATE;
spo off;

select fd_merch_name,line_description,debit_credit,card_scheme,,sum(volume),sum(flow_eur),sum(interchange_eur)
from fdwo.acquirer_firstdata_cost
where month BETWEEN TO_DATE('3/01/2017','MM/DD/YYYY')AND TO_DATE('2/28/2018','MM/DD/YYYY')
and transaction_type='TRANSACTION'
and volume is not null
group by fd_merch_name,line_description,debit_credit,card_scheme;

select mid_name,interchange_desc,card_scheme,card_type,card_desc,issuing_ctry,interch_perc,interch_fixed,SUM(flow_eur),SUM(interchange_eur),SUM(volume)
from fdwo.acquirer_elavon_usa_cost
where card_scheme is not null
and trans_date between TO_DATE('3/01/2017','MM/DD/YYYY')AND TO_DATE('2/28/2018','MM/DD/YYYY')
group by mid_name,card_scheme,card_type,card_desc,issuing_ctry,interch_perc,interch_fixed,interchange_desc;

select mid_name,line_description,interchange_rate,sum(volume),sum(flow_eur),sum(interchange_eur)
from fdwo.acquirer_wellsfargo_cost
where month between TO_DATE('3/01/2017','MM/DD/YYYY')AND TO_DATE('2/28/2018','MM/DD/YYYY')
and transaction_type ='TRANSACTION'
and mid_name is not null
and cost_type='INTERCHANGE'
group by  mid_name,line_description,interchange_rate;



