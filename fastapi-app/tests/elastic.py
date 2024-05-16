from elasticsearch import Elasticsearch

# curl -k -XGET https://172.19.0.2:9200/_cluster/health?pretty -u elastic
client = Elasticsearch(
    "http://172.19.0.2:9200/",
    # api_key="U1dhN2NZOEJXZFdEbjVpSWRWbFg6VjBjTUpDcl9UYzZsa211bXF0V0V5UQ==",
    # verify_certs=False,
)

# API key should have cluster monitor rights
client.info()
