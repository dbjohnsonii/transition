SELECT 
MAX(ab.transaction_date) AS TRXN_DATE
,ab.contract_id
,ab.issuer_country
,ab.issuer_bin
,ab.card_brand
,ab.clearing_country_name
,ab.transaction_type
,ab.SECURITY_LEVEL
,ab.CARD_TYPE
,ab.INTERCHANGE_RATE_DESCRIPTION
,ROUND(ab.transaction_flow_eur) AS TRXN_FLOW
,SF_RATE_AMOUNT
,SF_RATE_PERC
,AVG((ABS(ab.scheme_fee_eur))) AS TRXN_SF
,INTERCHANGE_RATE_AMOUNT
,INTERCHANGE_RATE_PERC
,AVG(ABS(INTERCHANGE_EUR)) AS TRXN_IC_COST
,CASE WHEN ROUND(ab.transaction_flow_eur)=0 THEN 0 WHEN ROUND(ab.transaction_flow_eur)>0 THEN AVG(ABS(INTERCHANGE_EUR))/ROUND(ab.transaction_flow_eur)END AS IC_BPS
,CASE WHEN ab.card_type_group LIKE '%Debit%' THEN 'Debit' WHEN ab.card_type_group LIKE '%Credit%' THEN 'Credit' WHEN ab.card_type_group LIKE '%Prepaid%' THEN 'Prepaid' END AS DEBIT_CREDIT_BIN
,CASE WHEN ab.card_type_group LIKE '%Consumer%' THEN 'Consumer' WHEN ab.card_type_group LIKE '%Commercial%' THEN 'Commercial' END AS CON_COMM_BIN
FROM fdwo.acquirer_aib_newgen_files ab
WHERE ab.transaction_date BETWEEN TO_DATE('11-01-2017','MM-DD-YYYY') AND TO_DATE('03-31-2018','MM-DD-YYYY')
AND PROCESSING_STATUS='Processed'
AND ab.scheme_fee_eur!=0
AND (ab.transaction_type='Sale')
AND (ab.interchange_region='Intra-region' OR ab.interchange_region='Inter-region' OR ab.interchange_region='Domestic')
AND ab.contract_id IN(SELECT bb.CONTRACT_ID FROM fdwo.acquirer_bambora_cost bb WHERE bb.TRANSACTION_TYPE='TRANSACTION')
GROUP BY ab.issuer_country,ab.issuer_bin,ab.card_brand, ab.clearing_country_name,ab.transaction_type,ab.transaction_flow_eur,ab.card_type_group
,INTERCHANGE_RATE_AMOUNT,INTERCHANGE_RATE_PERC,SF_RATE_AMOUNT, SF_RATE_PERC,ab.contract_id,ab.SECURITY_LEVEL,ab.CARD_TYPE,ab.INTERCHANGE_RATE_DESCRIPTION
