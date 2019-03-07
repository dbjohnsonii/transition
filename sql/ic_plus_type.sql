select CP.CONTRACT_ID,CP.PRODUCT_CODE,CP.TRANSACTION_CURRENCY,CP.ICPLUS_TYPE,CP.TRANSACTION_TYPE,CP.TRANSACTION_TYPE_SPECIFIC
from FDWO.CC_PROCESSING_DATA_PT cp
where CP.PAYMENT_PROCESSOR='AIB'
and CP.MATCH_DATE between to_date('4/1/2018','MM/DD/YYYY') and to_date('6/30/2018','MM/DD/YYYY')
--and CP.CONTRACT_ID=1067
--and CP.PRODUCT_CODE=100450
and CP.TRANSACTION_TYPE_SPECIFIC='TRANSACTION'
--and CP.ICPLUS_TYPE='-'
group by CP.CONTRACT_ID,CP.PRODUCT_CODE,CP.TRANSACTION_CURRENCY,CP.ICPLUS_TYPE,CP.TRANSACTION_TYPE,CP.TRANSACTION_TYPE_SPECIFIC
