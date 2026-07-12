# CEI_AZURE_Task4
This project demonstrates the implementation of an end-to-end data pipeline using Microsoft Azure services. The pipeline reads a CSV dataset from Azure Blob Storage, validates file metadata using Azure Data Factory (ADF), and copies the data to a destination container.

## Objectives

* Understand Azure cloud fundamentals and resource management.
* Create and configure Azure Storage Accounts and Blob Containers.
* Build and manage data pipelines using Azure Data Factory.
* Implement metadata validation using the Get Metadata activity.
* Transfer data between storage locations using the Copy Data activity.
* Monitor and validate successful pipeline execution.

## Architecture

```text
Azure Blob Storage (Source Container)
        │
        ▼
Sample - Superstore.csv
        │
        ▼
Azure Data Factory
 ├── Linked Service
 ├── Source Dataset
 ├── Get Metadata Activity
 ├── Copy Data Activity
 └── Destination Dataset
        │
        ▼
Azure Blob Storage (Destination Container)
        │
        ▼
Superstore_Output.csv
```

## Technologies Used

* Microsoft Azure
* Azure Resource Groups
* Azure Storage Account
* Azure Blob Storage
* Azure Data Factory (ADF)

## Implementation Steps

1. Created an Azure Resource Group.
2. Created an Azure Storage Account.
3. Created source and destination Blob Containers.
4. Uploaded the Superstore CSV dataset to the source container.
5. Created an Azure Data Factory instance.
6. Configured a Linked Service to connect ADF with Blob Storage.
7. Created source and destination datasets.
8. Implemented Get Metadata activity to validate source file properties.
9. Implemented Copy Data activity to transfer data.
10. Executed and monitored the pipeline.
11. Verified successful output generation in the destination container.

## Results

* Source dataset successfully detected.
* Metadata validation completed successfully.
* Data copied successfully from source to destination container.
* Output file generated in Blob Storage.
* Pipeline execution status: **Succeeded**.

## Output

**Source File:** `Sample - Superstore.csv`

**Destination File:** `Superstore_Output.csv`

## Conclusion

The project successfully demonstrates an end-to-end Azure data integration workflow using Azure Data Factory. Metadata validation and data movement were completed successfully, showcasing the practical use of Azure Storage and ADF for cloud-based data processing pipelines.

## Author

**Rachit Jain**
