#!/bin/sh
#curl -X POST https://demo.*.com/api/login -H  'content-type: multipart/form-data' \
#	 -F login=apiusertest@*.com \
#	 -F 'password=* '

curl -X POST https://demo.*.com/api/companies/S2P33AZQ0/rates/midmarket_spot -H  'content-type: multipart/form-data' \
	 -F login=apiusertest@*.com \
	 -F 'token=*'

curl -X POST --data-binary '{"email":"apiusertest@kantox.com", "token":""}'\
 -H 'content-type:text/plain;' https://demo.*.com/api/companies/*/orders/create


curl -X POST https://demo.*.com/api/companies/*/orders/create  -H 'content-type: multipart/form-data' -H 'X-ACCESS-TOKEN: *'

{"status":"error","reason":8,"errorDetails":"market_direction: Market Direction is required / currency: Currency is required / amount: Amount is required / counter_currency: Counter Currency is required / value_date: Value Date is required"}

