# AlgorithmsApi

All URIs are relative to *http://127.0.0.1:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**algorithmsCreate**](AlgorithmsApi.md#algorithmsCreate) | **POST** /api/v1/algorithms | 
[**algorithmsDestroy**](AlgorithmsApi.md#algorithmsDestroy) | **DELETE** /api/v1/algorithms/{id} | 
[**algorithmsList**](AlgorithmsApi.md#algorithmsList) | **GET** /api/v1/algorithms | 
[**algorithmsPartialUpdate**](AlgorithmsApi.md#algorithmsPartialUpdate) | **PATCH** /api/v1/algorithms/{id} | 
[**algorithmsPredict**](AlgorithmsApi.md#algorithmsPredict) | **POST** /api/v1/algorithms/predict | 
[**algorithmsRetrieve**](AlgorithmsApi.md#algorithmsRetrieve) | **GET** /api/v1/algorithms/{id} | 
[**algorithmsUpdate**](AlgorithmsApi.md#algorithmsUpdate) | **PUT** /api/v1/algorithms/{id} | 


<a name="algorithmsCreate"></a>
# **algorithmsCreate**
> Algorithm algorithmsCreate(algorithm)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    Algorithm algorithm = new Algorithm(); // Algorithm | 
    try {
      Algorithm result = apiInstance.algorithmsCreate(algorithm);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsCreate");
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
 **algorithm** | [**Algorithm**](Algorithm.md)|  |

### Return type

[**Algorithm**](Algorithm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

<a name="algorithmsDestroy"></a>
# **algorithmsDestroy**
> algorithmsDestroy(id)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this algorithm.
    try {
      apiInstance.algorithmsDestroy(id);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsDestroy");
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
 **id** | **Integer**| A unique integer value identifying this algorithm. |

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

<a name="algorithmsList"></a>
# **algorithmsList**
> List&lt;Algorithm&gt; algorithmsList()



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    try {
      List<Algorithm> result = apiInstance.algorithmsList();
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsList");
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

[**List&lt;Algorithm&gt;**](Algorithm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="algorithmsPartialUpdate"></a>
# **algorithmsPartialUpdate**
> Algorithm algorithmsPartialUpdate(id, algorithm)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this algorithm.
    Algorithm algorithm = new Algorithm(); // Algorithm | 
    try {
      Algorithm result = apiInstance.algorithmsPartialUpdate(id, algorithm);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsPartialUpdate");
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
 **id** | **Integer**| A unique integer value identifying this algorithm. |
 **algorithm** | [**Algorithm**](Algorithm.md)|  |

### Return type

[**Algorithm**](Algorithm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="algorithmsPredict"></a>
# **algorithmsPredict**
> PredictionResponse algorithmsPredict(classifier, version, dataset, status, requestBody)



Predict credit risk for a loan

### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    String classifier = "RandomForestClassifier"; // String | The algorithm/classifier to use
    String version = "0.0.1"; // String | Algorithm version
    String dataset = "german"; // String | The name of the dataset
    String status = "production"; // String | The status of the algorithm
    Map<String, Object> requestBody = null; // Map<String, Object> | 
    try {
      PredictionResponse result = apiInstance.algorithmsPredict(classifier, version, dataset, status, requestBody);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsPredict");
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
 **classifier** | **String**| The algorithm/classifier to use |
 **version** | **String**| Algorithm version | [default to 0.0.1]
 **dataset** | **String**| The name of the dataset | [optional]
 **status** | **String**| The status of the algorithm | [optional]
 **requestBody** | [**Map&lt;String, Object&gt;**](Object.md)|  | [optional]

### Return type

[**PredictionResponse**](PredictionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="algorithmsRetrieve"></a>
# **algorithmsRetrieve**
> Algorithm algorithmsRetrieve(id)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this algorithm.
    try {
      Algorithm result = apiInstance.algorithmsRetrieve(id);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsRetrieve");
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
 **id** | **Integer**| A unique integer value identifying this algorithm. |

### Return type

[**Algorithm**](Algorithm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="algorithmsUpdate"></a>
# **algorithmsUpdate**
> Algorithm algorithmsUpdate(id, algorithm)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.AlgorithmsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    AlgorithmsApi apiInstance = new AlgorithmsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this algorithm.
    Algorithm algorithm = new Algorithm(); // Algorithm | 
    try {
      Algorithm result = apiInstance.algorithmsUpdate(id, algorithm);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling AlgorithmsApi#algorithmsUpdate");
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
 **id** | **Integer**| A unique integer value identifying this algorithm. |
 **algorithm** | [**Algorithm**](Algorithm.md)|  |

### Return type

[**Algorithm**](Algorithm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

