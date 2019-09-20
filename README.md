# revolut-client

A simple class to handle authentication when access your own or another user's Revolut account. 

Can be used to [exchange authorisation code for access token](https://revolutdev.github.io/business-api/#exchange-authorisation-code-to-access-your-own-account) 
and to [refresh access tokens](https://revolutdev.github.io/business-api/#refresh-access-token-to-access-your-own-account).

The JWT generation is easy to get wrong - note that an OrderedDict is used for the token args.

### Environment variables:

* _REVOLUT_URL_: `https://b2b.revolut.com/api/1.0` or `https://sandbox-b2b.revolut.com/api/1.0`
* _REVOLUT_JWT_ISSUER_: derived from your redirect URI when you register your app
* _REVOLUT_CLIENT_ID_: client ID generated when you register your app
* _REVOLUT_PRIVATE_KEY_PATH_: location of your `privatekey.pem` file

### Example
```
client = RevolutClient()

authorisation_code = "oa_sand_gg-_wDV66wYfKKpnF4RIrpOZs2oPTwNp4TXOra5pS0g"
client.get_access_token(authorisation_code)
>> {"access_token": "oa_sand_rPo9OmbMAuguhQffR6RLR4nvmzpx4NJtpdyvGKkrS3U", "token_type": "bearer", "expires_in": 604800, "refresh_token": "oa_prod_hQacSGnwx-luIfj3dlVByrytVV9rWAnyHkpJTwG_Tr8"}

refresh_token = "oa_prod_hQacSGnwx-luIfj3dlVByrytVV9rWAnyHkpJTwG_Tr8"
client.refresh_access_token(refresh_token)
>> {"access_token" : "oa_prod_rPo9OmbMAuguhQffR6RLR4nvmzpx4NJtpdyvGKkrS3U", "token_type" : "bearer", "expires_in" : 604800}
```
