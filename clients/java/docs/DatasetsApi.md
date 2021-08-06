# DatasetsApi

All URIs are relative to *http://127.0.0.1:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**datasetsList**](DatasetsApi.md#datasetsList) | **GET** /api/v1/datasets | 
[**datasetsRetrieve**](DatasetsApi.md#datasetsRetrieve) | **GET** /api/v1/datasets/{id} | 


<a name="datasetsList"></a>
# **datasetsList**
> List&lt;Dataset&gt; datasetsList()



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.DatasetsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    DatasetsApi apiInstance = new DatasetsApi(defaultClient);
    try {
      List<Dataset> result = apiInstance.datasetsList();
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling DatasetsApi#datasetsList");
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

[**List&lt;Dataset&gt;**](Dataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

<a name="datasetsRetrieve"></a>
# **datasetsRetrieve**
> Dataset datasetsRetrieve(id)



### Example
```java
// Import classes:
import org.apache.fineract.credit.scorecard.ApiClient;
import org.apache.fineract.credit.scorecard.ApiException;
import org.apache.fineract.credit.scorecard.Configuration;
import org.apache.fineract.credit.scorecard.models.*;
import org.apache.fineract.credit.scorecard.services.DatasetsApi;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://127.0.0.1:8000");

    DatasetsApi apiInstance = new DatasetsApi(defaultClient);
    Integer id = 56; // Integer | A unique integer value identifying this dataset.
    try {
      Dataset result = apiInstance.datasetsRetrieve(id);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling DatasetsApi#datasetsRetrieve");
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
 **id** | **Integer**| A unique integer value identifying this dataset. |

### Return type

[**Dataset**](Dataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

