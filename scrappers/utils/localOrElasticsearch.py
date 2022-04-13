# Function to choose if sending 
# products to a local file or 
# to elasticsearch

from elasticsearch import Elasticsearch
import os

def localOrElasticsearch(destination, products, provider):
    if destination == "local":
        file = open("products.js", "a")
        for product in products:
            file.write(f"{{'_source': {product}}},")
    else: 
        elasticsearchClient = Elasticsearch(
            [os.environ.get("ELASTICSEARCH_HOST")], 
            scheme="http", 
            port=os.environ.get("ELASTICSEARCH_PORT")
        )
        elasticsearchClient.delete_by_query(index="products", body={"query": {"match": {"provider": provider}}})
        for product in products: elasticsearchClient.index(index="products", document=product)

