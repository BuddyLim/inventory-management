aws dynamodb create-table --cli-input-yaml "`cat template.yaml | yq e '.Resources.InventoryTable.Properties' -`" --no-cli-pager --endpoint-url http://localhost:8000

sam local invoke GetInventoryFunction --env-vars ./test_environment.json --docker-network dynamo_net -e ./handlers/get_inventory_handler/events.json

sam local invoke CreateInventoryFunction --env-vars ./test_environment.json --docker-network dynamo_net -e ./handlers/create_inventory_handler/events.json

sam local invoke StatsInventoryFunction --env-vars ./test_environment.json --docker-network dynamo_net