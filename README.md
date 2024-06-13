Setup guide (Local Development)

- Backend
  - SAM
    - sam build
  - Local Dynamodb 
    - install yq
    - bootstrap dynamodb table
      - ```aws dynamodb create-table --cli-input-yaml "`cat template.yaml | yq e '.Resources.InventoryTable.Properties' -`" --no-cli-pager --endpoint-url http://localhost:8000```
      

To invoke locally
- ```sam local invoke --env-vars ./test_environment.json --docker-network dynamo_net```