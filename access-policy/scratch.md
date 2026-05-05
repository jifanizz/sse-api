# URL:

[https://developer.cisco.com/docs/cloud-security/secure-access-api-oauth-scopes/#policies-scopes-and-endpoints](https://developer.cisco.com/docs/cloud-security/secure-access-api-oauth-scopes/#policies-scopes-and-endpoints)

# Private Resources

## policies.privateresources:read

View the private resources.	GET /policies/v2/privateResources
GET /policies/v2/privateResources/{id}

## policies.privateresources:write

Create, update, and delete the private resources.	POST /policies/v2/privateResources
PUT /policies/v2/privateResources/{id}
DELETE /policies/v2/privateResources/{id}

# UdeM Access-Policy:

```python
url = "https://api.sse.cisco.com/policies/v2/rules/2587073"
params = {
    "limit": 10,
    # Filter to AD groups only. Remove this line first run to discover
    # what `type.type` strings your org actually returns.
    #"identitytypes": "ad_groups",
    # Optional: narrow by name
    # "search": "UdeM",
}
```

Access-policy id id `2587073`

# UdeM Resource Group:

```python
url = "https://api.sse.cisco.com/policies/v2/privateResources/523153"
params = {
    "limit": 1000,
    # Filter to AD groups only. Remove this line first run to discover
    # what `type.type` strings your org actually returns.
    #"identitytypes": "ad_groups",
    # Optional: narrow by name
    # "search": "UdeM",
}
```

Private-Resource-ID is `523153`

# Retrieve AD-Groups

```python
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
}

url = "https://api.sse.cisco.com/reports/v2/identities"
params = {
    "limit": 1000,
    "offset": 1 
    # Filter to AD groups only. Remove this line first run to discover
    # what `type.type` strings your org actually returns.
    #"identitytypes": "ad_groups",
    # Optional: narrow by name
    # "search": "UdeM",
}
response = requests.get(url, headers=headers, params=params)
print("Status:", response.status_code)
print(response.text.encode('utf8'))
#data = response.json()
```

