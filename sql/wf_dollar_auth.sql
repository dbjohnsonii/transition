select COUNT(pa.orderid) AS orderid_count,PA.MERCHANTID,MM.MERCHANTNAME,
extract(month from CAST(pa.statusdate AS DATE)),
CASE WHEN SP.PROVIDERNAME ='CommWeb' then 'Commonwealth'
WHEN SP.PROVIDERNAME ='MerchantSolutions' then 'Merchant Solutions'
    WHEN SP.PROVIDERNAME ='Wells Fargo MC' then 'Wells Fargo'
    WHEN SP.PROVIDERNAME LIKE '%Litle%' then 'Vantiv'
    WHEN SP.PROVIDERNAME LIKE '%Vantiv%' then 'Vantiv'
    WHEN SP.PROVIDERNAME LIKE '%First Data%' then 'First Data'
    WHEN SP.PROVIDERNAME LIKE '%Firstdata%' then 'First Data'
    WHEN SP.PROVIDERNAME LIKE '%Wells Fargo MC TNS2%' then 'Wells Fargo'
    ELSE SP.PROVIDERNAME
    END AS "PROVIDERNAME" 
from eps.OPR_PAYMENTATTEMPT pa
left join EPS.MRM_MERCHANT mm
on PA.MERCHANTID=MM.MERCHANTID
left join EPS.GPM_PAYMENTPRODUCT pp
on PA.PAYMENTPRODUCTID=PP.PAYMENTPRODUCTID
left join EPS.PCO_CREDITCARDONLINE cc
on PA.ORDERID=CC.ORDERID
and PA.AMOUNT=CC.AMOUNT
and PA.MERCHANTID=CC.MERCHANTID
left join EPS.GPM_SERVICEPROVIDER sp
on CC.SERVICEPROVIDERID=SP.SERVICEPROVIDERID
left join FDWO.MB_PAYMENTPROCESSOR pp
ON cc.PAYMENTPROCESSOR=pp.paymentprocessor_id
left join EPS.MRM_MERCHANT mm
on PA.MERCHANTID=MM.MERCHANTID
where pa.statusid in(99999)
and PA.AMOUNT=100
and PA.STATUSDATE>=to_date('1/1/2018','MM/DD/YYYY')
and PA.PAYMENTPRODUCTID=1
and pp.interchange_region IN('NorthAm')
group by pa.statusid,PA.AMOUNT,PA.MERCHANTID,PP.PAYMENTPRODUCTNAME,SP.PROVIDERNAME
,extract(month from CAST(pa.statusdate AS DATE)),MM.MERCHANTNAME