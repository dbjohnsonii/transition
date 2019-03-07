select Acquirer,TRANSACTION_TYPE,CARD_BRAND,CARD_TYPE_GROUP,CARD_TYPE_CODE,CARD_TYPE,PRODUCT_NAME,SUM(TRANSACTION_FLOW_EUR) AS TRANSACTION_FLOW_EUR,CARD_CATEGORY
from
(
select Acquirer,AB.TRANSACTION_TYPE,AB.CARD_BRAND,AB.CARD_TYPE_GROUP,AB.CARD_TYPE_CODE,AB.CARD_TYPE
,case 
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='GBP' and ab.CARD_BRAND='Visa' and ab.CARD_TYPE like '%Debit%' then 'Visa Debit-GBP'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='GBP' and ab.CARD_BRAND='Visa' and ab.CARD_TYPE not like '%Debit%' then 'Visa-GBP'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='GBP' and ab.CARD_BRAND='MasterCard' and ab.CARD_TYPE not like '%Debit%' then 'MasterCard-GBP'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='GBP' and ab.CARD_BRAND='MasterCard' and ab.CARD_TYPE like '%Debit%' then 'MasterCard Debit-GBP'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='EUR' and ab.CARD_BRAND='Visa' and ab.CARD_TYPE like '%Debit%' then 'Visa Debit-EUR'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='EUR' and ab.CARD_BRAND='Visa' and ab.CARD_TYPE not like '%Debit%' then 'Visa-EUR'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='EUR' and ab.CARD_BRAND='MasterCard' and ab.CARD_TYPE not like '%Debit%' then 'MasterCard-EUR'
when PC.PRODUCT_NAME is null and ab.transaction_type='Sale' and AB.TRANSACTION_CURRENCY='EUR' and ab.CARD_BRAND='MasterCard' and ab.CARD_TYPE like '%Debit%' then 'MasterCard Debit-EUR'
else PC.PRODUCT_NAME
end as PRODUCT_NAME
,AB.TRANSACTION_CURRENCY,SUM(AB.TRANSACTION_FLOW_EUR) as TRANSACTION_FLOW_EUR
,case when CARD_TYPE in ('Mastercard Black') then 'Black'
when CARD_TYPE in ('MasterCard B2B Product','Visa Business') then 'Business'  
when CARD_TYPE in ('Mastercard Or Eurocard Standard','Mastercard Or Eurocard Card - Standard','Visa Classic','MasterCard Standard Deferred','MasterCard standard - unspecified detail','Visa Standard - unspecified detail') then 'Consumer'
when CARD_TYPE in ('Eurocard-Mastercard Corporate Card','Visa Corporate T and E','Mastercard Or Eurocard Corporate-Businesscard') then 'Corporate'
when CARD_TYPE in ('Mastercard Or Eurocard Corporate-Businesscard','Visa Classic Debit','Visa Gold Debit','Mastercard Debit Standard Card','Visa Platinum Debit','Visa Business Debit'
                    ,'Gold Mastercard Card-Immediate Debit','Mastercard Standard Card-Immediate Debit','Visa Purchasing Deferred Debit','Visa Classic Deferred Debit','MasterCard World Signia Card Immediate Debit'
                    ,'Visa Corporate T and E Debit','Visa Electron Debit','Visa Business Deferred Debit','Mastercard Debit Platinum','Mastercard Debit Other 2 Embossed','MasterCard Debit Unembossed','Visa Corporate T and E Deferred Debit'
                    ,'MasterCard Immediate Debit ICIS Student') then 'Debit'
when CARD_TYPE in ('Mastercard Or Eurocard Corporate Fleet Card') then 'Fleet'
when CARD_TYPE in ('Visa Gold','Mastercard Or Eurocard Gold Card') then 'Gold'
when CARD_TYPE in ('Visa High Net Worth HNW Consumer - Canada only') then 'HNW'  
when CARD_TYPE in ('Visa Infinite','Visa Infinite Prepaid') then 'Infinite'  
when CARD_TYPE in ('Mastercard New World Card') then 'New World'
when CARD_TYPE in ('Visa Platinum','Mastercard Or Eurocard Platinum Card') then 'Platinum'
when CARD_TYPE in ('Visa Electron Prepaid','Mastercard Prepaid Non-US','MasterCard Prepaid business card','Mastercard Prepaid General Spend'
                    ,'Visa Platinum Prepaid','Visa Classic Prepaid','Mastercard Prepaid Unembossed') then 'Prepaid'
when CARD_TYPE in ('Visa Purchasing') then 'Purchasing'
when CARD_TYPE in ('Mastercard Rewards Only') then 'Rewards'
when CARD_TYPE in ('Visa Select') then 'Select'  
when CARD_TYPE in ('Visa Signature Preferred','Visa Signature') then 'Signature'  
when CARD_TYPE in ('Titanium Mastercard') then 'Titanium'
when CARD_TYPE in ('Visa Traditional') then 'Traditional'
when CARD_TYPE in ('Visa Traditional Rewards') then 'Traditional rewards'
when CARD_TYPE in ('Mastercard World Elite Card') then 'World Elite'
when CARD_TYPE in ('Mastercard Or Eurocard World Signia Card') then 'World Signia'
end as CARD_CATEGORY
,AB.PRODUCT_CODE
from FDWO.ACQUIRER_AIB_NEWGEN_FILES ab
cross join
(select 'AIB' as Acquirer from dual)
left join
(select PRODUCT_NAME,PRODUCT_CODE from FDWO.MB_PRODUCT_CODE) pc
on AB.PRODUCT_CODE=PC.PRODUCT_CODE
where AB.TRADING_MERCHANT_NAME like '%Air Trans%'
and AB.TRANSACTION_DATE between to_date('7/1/2018','MM/DD/YYYY') and to_date('9/30/2018','MM/DD/YYYY')
and AB.PROCESSING_STATUS not in ('Suspended')
--and AB.PRODUCT_CODE is not null
group by Acquirer,AB.TRANSACTION_TYPE,AB.CARD_BRAND,AB.CARD_TYPE_GROUP,AB.CARD_TYPE_CODE,AB.CARD_TYPE
,PC.PRODUCT_NAME,AB.PRODUCT_CODE,AB.TRANSACTION_CURRENCY
order by TRANSACTION_FLOW_EUR desc
)
group by Acquirer,TRANSACTION_TYPE,CARD_BRAND,CARD_TYPE_GROUP,CARD_TYPE_CODE,CARD_TYPE,PRODUCT_NAME,CARD_CATEGORY
order by TRANSACTION_FLOW_EUR desc
