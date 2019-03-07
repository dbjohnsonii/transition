  SELECT 
  ev.roc_text,ev.mid_name,ev.card_scheme,ev.card_type,ev.card_desc,ev.charge_type,ev.interchange_desc
  ,ev.issuing_ctry,ev.issuing_region,ev.volume,ev.flow,ev.interch_perc,ev.interch_fixed,ev.trans_date
  ,pa.receiveddate,pa.statusdate,ev.transaction_type,ev.TRANS_CURR,pa.CURRENCYCODE,pa.paymentamount
  ,ev.flow_usd,pa.orderid,pa.paymentreference,pa.statusid
  ,ev.contract_id
  FROM 
  DATA.ACQUIRER_ELAVON_USA_COST AS ev
  LEFT JOIN 
  EPS.OPR_PAYMENTATTEMPT AS pa
  ON
  CAST(ev.roc_text AS nchar(18))=pa.paymentreference 
  WHERE ev.transaction_type='TRANSACTION'
  AND ev.roc_text IS NOT NULL
  AND ev.trans_date BETWEEN TO_DATE('01/01/2017','MM/DD/YYYY') AND TO_DATE('12/31/2017','MM/DD/YYYY')
  AND ev.CONTRACT_ID=3875
  AND pa.STATUSID=1050;