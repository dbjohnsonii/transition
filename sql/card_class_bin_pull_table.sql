sqlplus/nolog
connect djohnson/RhiBoo02!@ODSPEU1.ams
set echo off
set feedback off
set colsep ';'
set sqlprompt ''
set headsep off
set serveroutput on size unlimited
set linesize 30000
set trimspool on
set pagesize 0
set heading on
set trimout on
set wrap off
set termout off
spo \\amscifs01\homefolders$\djohnson\Desktop\card_class_bin.csv
select 
BIN,CARD_CLASS_BIN
from fdwo.cc_processing_data_pt
group by BIN, CARD_CLASS_BIN;
spo end