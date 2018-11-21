#!/bin/bash

curl -X POST --data-binary '{"jsonrpc":"2.0","id":"curltext","method":"get-user-profile","params":{"email":"", "auth_token":""}}' -H 'content-type:text/plain;' https://demo.*.com/api/login

