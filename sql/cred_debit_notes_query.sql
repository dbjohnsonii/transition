select M.CLIENT_NAME,M.CLIENT_ID,M.CONTRACT_ID,GM.PRODUCT_CODE,GM.MONTH,GM.INVOICE_PERIOD,PC.PRODUCT_NAME,CC.ICPLUS_TYPE,SUM(GM.INV_VOLUME)
from FDWO.MB_MERCHANTS m
left join FDWO.GM_CALCULATION gm
on M.CONTRACT_ID=GM.CONTRACT_ID
left join FDWO.MB_PRODUCT_CODE pc
on GM.PRODUCT_CODE=PC.PRODUCT_CODE
left join FDWO.CC_PROCESSING_DATA_PT cc
on M.CONTRACT_ID=TO_CHAR(CC.CONTRACT_ID)
where CLIENT_ID=8508
and GM.PRODUCT_CODE=100450
and GM.MONTH>=to_date('1/1/2018','MM/DD/YYYY')
and CC.CARD_SCHEME_BIN IN('VISA','MASTERCARD')
group by M.CLIENT_NAME,M.CLIENT_ID,M.ID,M.CONTRACT_ID,GM.PRODUCT_CODE,GM.MONTH,GM.INVOICE_PERIOD,PC.PRODUCT_NAME,CC.ICPLUS_TYPE
