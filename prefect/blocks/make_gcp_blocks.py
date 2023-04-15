from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

credentials_block = GcpCredentials(
    service_account_info={
  "type": "service_account",
  "project_id": "dezoomcamp-steam-project",
  "private_key_id": "ed5ef8e8634f22630c55ec58b201946571567994",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCr+Zk4t++0Fbnt\nEgOIT9q/sKFJlYXgmhWNwi7F3LaFMPtNODzh7T4GgxojIQehLQPm5KS4VNON1m1S\noGpmBAQ6L7J/uAqPhYZeyb6Wr0hDQOlghJegtvunMrZ4QVenwBK22HsHa8pi3I+H\nfjNiTPQkrddL8BuS+tJmA4SevaXw3TMzyJwPMs1TuDSNDy8v3hZrG1tBTERUcg1+\nrFcLRWv6WfJ8tHYIFJTYGUE0np03Y1krOuV8iYr146mJK29L+CQrQmj35TK1d8mb\n0hm4Qc+CP1OmBdVXJfEiJXRG4qSnMHPKpH9wB0y7L0TmeGQHLCpnCmLwyVMjAmIz\nkpdRsAHpAgMBAAECggEAJEL7MJcyMx/wpgEKHyQtXQV2oMAnLDp5KHylJaHaF4AC\nQSBGUCIY1cEvkfAtPmoyPC2CYP6749iukQFTpgKbTJSRl/YbvfL66AI0jmvTuiCW\nBPy4RxJGQlVCXd1zSOMKXyUK3f/3uvxERF7TIVtWEGTadH/ipI2ALzP3MwyMkJqP\nKlZKCwJ+X8aIcZcIRhn+/LmBVha36bZFrhuERjPeBB5vsT0YVpHVIh8cD7rN0Ew2\n9tcypEKm/tLVsKrZUk1QjWtj2RuucsjQGBK+Ee669CMPCLZ7K5WuylSEVblCYI7u\ncee1Z0bwlC2eja7PTuMx99teYuLGXycFtrTY6lbaTQKBgQDU8iyuiP3zkBZwTyag\nhKRbOZIf0TZooIFoTcdqGG+BDWOuNtvH7TyBf1e0dvELS6nIYwv/NrAR7ATskx89\nHqsKCBTcP5XYKpNV0YbnsxM/kLBy3S741RUBKmgAhJyxP/rs10Dxwzrwo1/sDA2b\nhMk5KFg7l7TDf2Safq4YolHZrQKBgQDOvtCcskOgffkQbjbZS+uhZt8LydJ4svDb\nDmfAJ4PZnR9SpAskbK1xy6NFX8wxIwS7lr/YARrgjh9dQOGCOktZeNFoa07Wq0Ut\nLXM9h9d4m8VLMLY4tDLz3fvcmYw2M08ErD0X4WnsGDa+QHjovXlDgbSzetS1P1Ip\nSSWVByyIrQKBgQCk72KuWQshwMOwf43ynGpVAjVtEXWr+k3hRQUk5wJOmdlQUctP\ngi/wOXrsG4g98H/z5sufBHPBneZ+esGibIOcBIBry5A7W1a9DMoJ4okRHfedMDY2\no4xeV8MwS4a2P1ESavMxjr6zLkeYpAlSILpe3CHjHnDzT1PT2jTsfaUaDQKBgQDG\nbTVjb2SgwMcvEdjqrYc1nbotYkLzPSsV07mYH1TYo4jQlEltaDD/qubFSrB76JQ+\nRu1Rr53QMBfCNOc7Sh/Pe7ngcj10o2T9e0XDpIEVbMvq4pHB0pGkpUV58JU14ADT\nB0yLgvlac9L2voJNPq0IMZDxQc6tNlzw6xd69Su08QKBgEHU/ebqLwomlKvbC9p2\nOpqT6FfVwEEOIbyxx2lEnjidvrsGjY7HGja+QDIcBvX3cnx00YdcYLB+ZsmXcDQL\n1pDfUwEuGFidYaiFth/67g3GV+VptVcQt/aMrvLZynFEuolIpIbAWvNpurnb0RTG\nbSUyJ0w4lKB1GT/v0Sl7K8ca\n-----END PRIVATE KEY-----\n",
  "client_email": "dezoomcamp-project@dezoomcamp-steam-project.iam.gserviceaccount.com",
  "client_id": "109853556259701640953",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dezoomcamp-project%40dezoomcamp-steam-project.iam.gserviceaccount.com"
}
  # enter your credentials from the json file
)
credentials_block.save("dezoomcamp-gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("dezoomcamp-gcp-creds"),
    bucket="steam_data_lake_dezoomcamp-steam-project",  
)

bucket_block.save("dezoomcamp-steam-gcs", overwrite=True)
