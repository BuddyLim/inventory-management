# Inventory Management

### Milestones:
- Local development using SAM
- Bootstrapping local DynamoDB
- Get inventory function:
	- With `datetime` filter iso standard (✅)
		- Validation (TBD)
	- Pagination (TBD)
-  Stats inventory function:
	- Aggregate by category (✅)
-  Create inventory function:
	- Normalize name for consistent hashing (✅)
		- `Sha1` hashing as primary key (✅)
	- Normalize category to unique ID (TDB)
- Deploying to AWS using SAM (✅)
- Minor testing (not very complete 😬)
- Frontend deployment to S3 & Cloudfront (✅)


### Setup guide (Local Development)

- #### Backend
  - Install necessary libraries from any of the `requirements.txt`
  - Dynamodb docker (in the `/cag-dynamodb`)
    - `docker-compose up`
  - Local Dynamodb (in the `/cag-app`)
    - install `yq` (Yaml parser, I'd prefer to use this to sync with whatever changes is done to `template.yml`)
    - To bootstrap local dynamodb table:
      - ```aws dynamodb create-table --cli-input-yaml "`cat template.yaml | yq e '.Resources.InventoryTable.Properties' -`" --no-cli-pager --endpoint-url http://localhost:8000```
      
- ### SAM (in the `/cag-app`)
	- To invoke locally:
		    - `sam build` (every code changes need to be rebuild)
		    - `GetInventoryFunction` Example:
		      - ```sam local invoke GetInventoryFunction -e handlers/get_inventory_handler/get_events.json --env-vars ./test_environment.json --docker-network dynamo_net;```
		      - ```sam local invoke GetInventoryFunction -e handlers/get_inventory_handler/filter_events.json --env-vars ./test_environment.json --docker-network dynamo_net;```
		    - `CreateInventoryFunction` Example:
		      - ```sam local invoke CreateInventoryFunction -e handlers/create_inventory_handler/create_events.json --env-vars ./test_environment.json --docker-network dynamo_net;```
		    - `StatsInventoryFunction` Example:
		      - ```sam local invoke StatsInventoryFunction -e handlers/stats_inventory_handler/events.json --env-vars ./test_environment.json --docker-network dynamo_net;```
	- To deploy, run:
	  - `sam build`
	  - `sam validate`
	  - `sam deploy`

  - Testing (abliet not very through.., in the `/cag-app`)
    - `python3 -m pytest tests/ -v`

- ### Frontend
  - `npm run dev`
