# MessengerifyApi.UsersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**loginPost**](UsersApi.md#loginPost) | **POST** /login | Authenticates user
[**registerPost**](UsersApi.md#registerPost) | **POST** /register | Add a new user



## loginPost

> UserData loginPost(body)

Authenticates user

### Example

```javascript
import MessengerifyApi from 'messengerify_api';

let apiInstance = new MessengerifyApi.UsersApi();
let body = new MessengerifyApi.UserAuth(); // UserAuth | User's login and password in JSON
apiInstance.loginPost(body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserAuth**](UserAuth.md)| User&#39;s login and password in JSON | 

### Return type

[**UserData**](UserData.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## registerPost

> UserData registerPost(body)

Add a new user

### Example

```javascript
import MessengerifyApi from 'messengerify_api';

let apiInstance = new MessengerifyApi.UsersApi();
let body = new MessengerifyApi.UserAuth(); // UserAuth | User's login and password in JSON
apiInstance.registerPost(body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserAuth**](UserAuth.md)| User&#39;s login and password in JSON | 

### Return type

[**UserData**](UserData.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*

