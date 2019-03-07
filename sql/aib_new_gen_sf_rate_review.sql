sqlplus/nolog
connect djohnson/RhiBae01!@ODSPEU1.ams
set serveroutput on size unlimited
set linesize 9999
set trim on
set pagesize 0
set heading on
prompt transaction_number,clearing_mcc_code,interchange_rate_description,transaction_type,sf_rate_description,sf_rate_perc,sf_rate_amount,transaction_date,issuer_name,issuer_region,issuer_country,issuer_country_visa_eur_rel,issuer_country_mc_sepa_rel,cardholder_country,card_brand,card_type,volume
select 
transaction_number
||';'||clearing_mcc_code
||';'||interchange_rate_description
||';'||transaction_type
||';'||sf_rate_description
||';'||sf_rate_perc
||';'||sf_rate_amount
||';'||transaction_date
||';'||issuer_name
||';'||issuer_region
||';'||issuer_country
||';'||issuer_country_visa_eur_rel
||';'||issuer_country_mc_sepa_rel
||';'||cardholder_country
||';'||card_brand
||';'||card_type
||';'||volume 
from fdwo.acquirer_aib_newgen_files
where transaction_date between to_date('10/1/2017','MM/DD/YYYY') and to_date('01/31/2018','MM/DD/YYYY')
and transaction_type='Sale'
and sf_rate_perc is not null;