select AB.TRADING_MERCHANT_NAME,AB.CONTRACT_ID,AB.ISSUER_COUNTRY,AB.CLEARING_COUNTRY_NAME AS "MERCHANT_COUNTRY",AB.ISSUER_COUNTRY_VISA_EUR_REL,AB.ISSUER_COUNTRY_MC_SEPA_REL,AB.INTERCHANGE_RATE_DESCRIPTION,
AB.CARD_BRAND,AB.SECURITY_LEVEL,SUM(AB.TRANSACTION_FLOW_EUR) AS FLOW,SUM(AB.VOLUME) AS VOL,ABS(SUM(AB.SCHEME_FEE_EUR)) AS SF,AB.SF_RATE_AMOUNT
,AB.SF_RATE_PERC,AB.SF_RATE_DESCRIPTION,AB.CARD_TYPE_GROUP,AB.CARD_TYPE,
CASE WHEN AB.SECURITY_LEVEL LIKE '%Channel%' THEN 'Nonsecure'
WHEN AB.SECURITY_LEVEL NOT LIKE '%Channel%' THEN 'Secure'
END AS "Security Level",

CASE WHEN AB.SF_RATE_DESCRIPTION LIKE '%Intra%' THEN 'Intra-Region'
WHEN AB.SF_RATE_DESCRIPTION LIKE '%Domestic%' THEN 'Domestic'
WHEN AB.SF_RATE_DESCRIPTION LIKE '%Inter%' THEN 'Inter-Region'
END AS "Regionality",

CASE WHEN AB.CARD_BRAND LIKE '%Visa%' THEN 'Visa'
WHEN AB.CARD_BRAND LIKE '%Maestro%' THEN 'Maestro'
WHEN AB.CARD_BRAND LIKE '%MasterCard%' THEN 'MasterCard'
END AS "BRAND",

CASE WHEN AB.CARD_TYPE_GROUP LIKE '%Credit%' THEN ''
WHEN AB.CARD_TYPE_GROUP LIKE '%Debit%' THEN 'Debit'
WHEN AB.CARD_TYPE_GROUP LIKE '%Prepaid%' THEN 'Debit'
WHEN AB.CARD_TYPE_GROUP ='Commercial' THEN ''
END AS "CARD_TYPES"

from FDWO.ACQUIRER_AIB_NEWGEN_FILES ab
where AB.PROCESSING_STATUS not in ('Suspended')
and AB.TRANSACTION_TYPE in ('Sale')
and AB.TRANSACTION_DATE Between to_date('4/1/2018','MM/DD/YYYY') and to_date('6/30/2018','MM/DD/YYYY')
--and AB.ISSUER_REGION='EUROPE'
group by AB.TRADING_MERCHANT_NAME,AB.CONTRACT_ID,AB.ISSUER_COUNTRY,AB.CLEARING_COUNTRY_NAME,AB.CARD_BRAND,AB.SECURITY_LEVEL,AB.SF_RATE_AMOUNT
,AB.SF_RATE_PERC,AB.SF_RATE_DESCRIPTION,AB.CARD_TYPE_GROUP,AB.CARD_TYPE,AB.ISSUER_COUNTRY_VISA_EUR_REL,AB.ISSUER_COUNTRY_MC_SEPA_REL,AB.INTERCHANGE_RATE_DESCRIPTION,
AB.TRADING_MERCHANT_NAME,AB.CONTRACT_ID