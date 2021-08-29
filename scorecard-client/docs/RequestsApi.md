# RequestsApi

All URIs are relative to *http://127.0.0.1:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**requestsCreate**](RequestsApi.md#requestsCreate) | **POST** /api/v1/requests | 
[**requestsDestroy**](RequestsApi.md#requestsDestroy) | **DELETE** /api/v1/requests/{id} | 
[**requestsList**](RequestsApi.md#requestsList) | **GET** /api/v1/requests | 
[**requestsPartialUpdate**](RequestsApi.md#requestsPartialUpdate) | **PATCH** /api/v1/requests/{id} | 
[**requestsRetrieve**](RequestsApi.md#requestsRetrieve) | **GET** /api/v1/requests/{id} | 
[**requestsUpdate**](RequestsApi.md#requestsUpdate) | **PUT** /api/v1/requests/{id} | 


<a name="requestsCreate"></a>
# **requestsCreate**
> PredictionRequest requestsCreate(predictionRequest)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.RequestsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    RequestsApi apiInstance = new RequestsApi(defaultClient);
    PredictionRequest predictionRequest = new PredictionRequest(); // PredictionRequest | 
    try {
      PredictionRequest result = apiInstance.requestsCreate(predictionRequest);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RequestsApi#requestsCreate");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **predictionRequest** | [**PredictionRequest**](PredictionRequest.md)|  |

### Return type

[**PredictionRequest**](PredictionRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

<a name="requestsDestroy"></a>
# **requestsDestroy**
> requestsDestroy(id)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.RequestsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    RequestsApi apiInstance = new RequestsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this prediction request.
    try {
      apiInstance.requestsDestroy(id);
    } catch (ApiException e) {
      System.err.println("Exception when calling RequestsApi#requestsDestroy");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Integer**| A unique integer value identifying this prediction request. |

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

<a name="requestsList"></a>
# **requestsList**
> java.util.List&lt;PredictionRequest&gt; requestsList()



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.RequestsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    RequestsApi apiInstance = new RequestsApi(defaultClient);
    try {
      java.util.List<PredictionRequest> result = apiInstance.requestsList();
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RequestsApi#requestsList");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**java.util.List&lt;PredictionRequest&gt;**](PredictionRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="requestsPartialUpdate"></a>
# **requestsPartialUpdate**
> PredictionRequest requestsPartialUpdate(id, predictionRequest)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.RequestsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    RequestsApi apiInstance = new RequestsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this prediction request.
    PredictionRequest predictionRequest = new PredictionRequest(); // PredictionRequest | 
    try {
      PredictionRequest result = apiInstance.requestsPartialUpdate(id, predictionRequest);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RequestsApi#requestsPartialUpdate");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Integer**| A unique integer value identifying this prediction request. |
 **predictionRequest** | [**PredictionRequest**](PredictionRequest.md)|  |

### Return type

[**PredictionRequest**](PredictionRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="requestsRetrieve"></a>
# **requestsRetrieve**
> PredictionRequest requestsRetrieve(id)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.RequestsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    RequestsApi apiInstance = new RequestsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this prediction request.
    try {
      PredictionRequest result = apiInstance.requestsRetrieve(id);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RequestsApi#requestsRetrieve");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Integer**| A unique integer value identifying this prediction request. |

### Return type

[**PredictionRequest**](PredictionRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="requestsUpdate"></a>
# **requestsUpdate**
> PredictionRequest requestsUpdate(id, predictionRequest)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.RequestsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    RequestsApi apiInstance = new RequestsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this prediction request.
    PredictionRequest predictionRequest = new PredictionRequest(); // PredictionRequest | 
    try {
      PredictionRequest result = apiInstance.requestsUpdate(id, predictionRequest);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RequestsApi#requestsUpdate");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Integer**| A unique integer value identifying this prediction request. |
 **predictionRequest** | [**PredictionRequest**](PredictionRequest.md)|  |

### Return type

[**PredictionRequest**](PredictionRequest.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

