"""Actual local counts of author-written paired strings; no inference or billable API call."""
from pathlib import Path
import sys,os,json,hashlib
from datetime import datetime,timezone
B=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'tokenizer-runtime'))
os.environ['TIKTOKEN_CACHE_DIR']=str(B/'tokenizer-cache')
import tiktoken
samples={
'English':'The customer returned two unopened items within 30 days. Refund 48 dollars to the original payment method and keep the order number in the record.',
'Mandarin':'客户在30天内退回了两件未拆封的商品。请将48美元退回原支付方式，并在记录中保留订单号。',
'Spanish':'El cliente devolvió dos artículos sin abrir dentro de los 30 días. Reembolsa 48 dólares al método de pago original y conserva el número de pedido en el registro.',
'Arabic':'أعاد العميل سلعتين غير مفتوحتين خلال 30 يومًا. أعد 48 دولارًا إلى وسيلة الدفع الأصلية واحتفظ برقم الطلب في السجل.',
'JSON':'{"returned_items":2,"unopened":true,"within_days":30,"refund_usd":48,"payment_method":"original","retain_order_number":true}',
'Python':'def refund(order):\n    if order.days <= 30 and order.unopened_items == 2:\n        return {"refund_usd": 48, "payment_method": "original", "order_id": order.id}\n'}
rows=[]
for label,s in samples.items():
 row={'sample':label,'text':s,'unicode_codepoints':len(s),'utf8_bytes':len(s.encode()),'sha256':hashlib.sha256(s.encode()).hexdigest()}
 for enc in ['cl100k_base','o200k_base']:row[enc]=len(tiktoken.get_encoding(enc).encode(s))
 rows.append(row)
result={'author':'/root/ttc_research','measured_at':datetime.now(timezone.utc).isoformat(),'tiktoken_version':tiktoken.__version__,'scope':'raw text only; translations are author-composed approximate semantic counterparts, code/JSON distinct representations; no chat/tool framing or billed-token claim','rows':rows,'rank_file_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (B/'tokenizer-cache').glob('*')}}
(B/'tokenizer-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in x.items() if k not in ['text','sha256']} for x in rows],ensure_ascii=False))
