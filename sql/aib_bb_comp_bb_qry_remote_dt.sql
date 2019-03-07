sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
set serveroutput on size unlimited
set linesize 300
set trim on
set pagesize 0
set heading on
spo \\amscifs01\homefolders$\djohnson\Desktop\aib_comp_pull_bb_data.csv
SELECT 
bb.BAMBORA_REF
||';'||bb.TRANSACTION_REF
||';'||TO_CHAR(bb.SETTLEMENT_DATE,'MM')
||';'||TO_CHAR(bb.SETTLEMENT_DATE,'DD')
||';'||TO_CHAR(bb.SETTLEMENT_DATE,'YYYY')
||';'||TO_CHAR(bb.SETTLEMENT_DATE,'YYYY-MM')
||';'||bb.CONTRACT_ID
||';'||bb.ISSUER_COUNTRY_NAME
||';'||bb.MERCHANT_COUNTRY_NAME
||';'||bb.TRANSACTION_TYPE
||';'||bb.CARD_SCHEME
||';'||bb.CREDIT_DEBIT
||';'||bb.CONSUMER_CORPORATE
||';'||bb.ECOM_SECURITY_LEVEL
||';'||bb.REGIONALITY
||';'||bb.PRODUCT_CODE
||';'||bb.SF_FIXED_FEE
||';'||bb.SF_PERC_FEE
||';'||bb.TRANSACTION_TYPE
||';'||bb.CONSUMER_CORPORATE
||';'||bb.VOLUME
||';'||ROUND(bb.TRANSACTION_AMOUNT_EUR)
||';'||bb.SCHEME_TOTAL_FEE_EUR
||';'||bb.TRANSACTION_AMOUNT_EUR
||';'||bb.INTERCHANGE_TOTAL_FEE_EUR
||';'||bb.INTERCHANGE_TOTAL_FEE_EUR/bb.TRANSACTION_AMOUNT_EUR
||';'||bb.SCHEME_TOTAL_FEE_EUR/bb.TRANSACTION_AMOUNT_EUR
FROM fdwo.acquirer_bambora_cost bb
WHERE bb.BAMBORA_TRANSACTION_TYPE='Sale'
AND bb.TRANSACTION_TYPE='TRANSACTION'
AND bb.SETTLEMENT_DATE BETWEEN TO_DATE('01-01-2018','MM-DD-YYYY') AND TO_DATE('03-31-2018','MM-DD-YYYY');
spo end