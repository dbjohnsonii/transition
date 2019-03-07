sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
set serveroutput on size unlimited
set linesize 300
set trim on
set pagesize 0
set heading on
spo d:\djohnson\Desktop\aib_comp_pull_data.csv
SELECT 
MAX(ab.transaction_date)
||';'||ab.contract_id
||';'||ab.issuer_country
||';'||ab.card_brand
||';'||ab.clearing_country_name
||';'||ab.transaction_type
||';'||ROUND(ab.transaction_flow_eur)
||';'||AVG((ABS(ab.scheme_fee_eur)))
||';'||AVG(ABS(INTERCHANGE_EUR))
||';'||INTERCHANGE_RATE_AMOUNT
||';'||INTERCHANGE_RATE_PERC
||';'||AVG(ABS(SCHEME_FEE_EUR))
||';'||SF_RATE_AMOUNT, SF_RATE_PERC
||';'||CASE WHEN ROUND(ab.transaction_flow_eur)=0 THEN 0
WHEN ROUND(ab.transaction_flow_eur)>0 THEN AVG(ABS(INTERCHANGE_EUR))/ROUND(ab.transaction_flow_eur)
END
||';'||CASE WHEN ab.card_type_group LIKE '%Debit%' THEN 'Debit'
WHEN ab.card_type_group LIKE '%Credit%' THEN 'Credit'
WHEN ab.card_type_group LIKE '%Prepaid%' THEN 'Prepaid'
END
||';'||CASE WHEN ab.card_type_group LIKE '%Consumer%' THEN 'Consumer'
WHEN ab.card_type_group LIKE '%Commercial%' THEN 'Commercial'
END
FROM fdwo.acquirer_aib_newgen_files ab
WHERE ab.transaction_date BETWEEN TO_DATE('01-01-2018','MM-DD-YYYY') AND TO_DATE('02-22-2018','MM-DD-YYYY')
AND ab.scheme_fee_eur!=0
AND (ab.transaction_type ='Sale')
AND (ab.interchange_region='Intra-region' OR ab.interchange_region='Inter-region' OR ab.interchange_region='Domestic')
AND ab.contract_id IN(SELECT bb.CONTRACT_ID FROM fdwo.acquirer_bambora_cost bb WHERE bb.TRANSACTION_TYPE='TRANSACTION')
--AND rownum<10
GROUP BY ab.issuer_country, ab.card_brand, ab.clearing_country_name,ab.transaction_type,ab.transaction_flow_eur,ab.card_type_group
,INTERCHANGE_RATE_AMOUNT,INTERCHANGE_RATE_PERC,SF_RATE_AMOUNT, SF_RATE_PERC,ab.contract_id;
spo end
