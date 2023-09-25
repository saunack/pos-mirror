from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import requests

def get_amount(f):
    cost = 0
    key = "347cfe5b1eec41af86346f017ac53c04"
    location = "eastus"
    endpoint = "https://formrecognizer-1.cognitiveservices.azure.com/"

    flag = False
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", document=f)
    result = poller.result()
    for i,line in enumerate(result.pages[0].lines):
        c = line.content
        print(c)
        if "Paid" in c:
            if "₹" in c:
                cost = float(c[c.index("₹")+1:].strip())
                break
            else:
                flag = True
        if flag:
            cost = float(c[c.index("₹")+1:].strip())
            break
    return cost
