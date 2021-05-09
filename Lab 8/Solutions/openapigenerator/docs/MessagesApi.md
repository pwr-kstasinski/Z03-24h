# MessengerifyApi.MessagesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**messageSenderUuidRecipientUuidGet**](MessagesApi.md#messageSenderUuidRecipientUuidGet) | **GET** /message/{sender_uuid}/{recipient_uuid} | Lists all messages between 2 users
[**messageSenderUuidRecipientUuidPost**](MessagesApi.md#messageSenderUuidRecipientUuidPost) | **POST** /message/{sender_uuid}/{recipient_uuid} | Sends message to provided user



## messageSenderUuidRecipientUuidGet

> [InlineResponse200] messageSenderUuidRecipientUuidGet(senderUuid, recipientUuid)

Lists all messages between 2 users

### Example

```javascript
import MessengerifyApi from 'messengerify_api';

let apiInstance = new MessengerifyApi.MessagesApi();
let senderUuid = "senderUuid_example"; // String | Sender's uuid
let recipientUuid = "recipientUuid_example"; // String | Recipient's uuid
apiInstance.messageSenderUuidRecipientUuidGet(senderUuid, recipientUuid, (error, data, response) => {
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
 **senderUuid** | **String**| Sender&#39;s uuid | 
 **recipientUuid** | **String**| Recipient&#39;s uuid | 

### Return type

[**[InlineResponse200]**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: */*


## messageSenderUuidRecipientUuidPost

> messageSenderUuidRecipientUuidPost(senderUuid, recipientUuid, body)

Sends message to provided user

### Example

```javascript
import MessengerifyApi from 'messengerify_api';

let apiInstance = new MessengerifyApi.MessagesApi();
let senderUuid = "senderUuid_example"; // String | Sender's uuid
let recipientUuid = "recipientUuid_example"; // String | Recipient's uuid
let body = new MessengerifyApi.InlineObject(); // InlineObject | 
apiInstance.messageSenderUuidRecipientUuidPost(senderUuid, recipientUuid, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **senderUuid** | **String**| Sender&#39;s uuid | 
 **recipientUuid** | **String**| Recipient&#39;s uuid | 
 **body** | [**InlineObject**](InlineObject.md)|  | 

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

