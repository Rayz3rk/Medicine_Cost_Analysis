from neo4j import GraphDatabase
from backend.core.config import settings

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_relationship(self, drug, cost_type, advice):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_relationship, drug, cost_type, advice)

    @staticmethod
    def _create_and_return_relationship(tx, drug, cost_type, advice):
        query = (
            "MERGE (d:Drug {name: $drug}) "
            "MERGE (c:CostType {name: $cost_type}) "
            "MERGE (a:Advice {content: $advice}) "
            "MERGE (d)-[:HAS_COST]->(c) "
            "MERGE (c)-[:OPTIMIZED_BY]->(a) "
            "RETURN d, c, a"
        )
        result = tx.run(query, drug=drug, cost_type=cost_type, advice=advice)
        return result.single()

try:
    neo4j_client = Neo4jClient(settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD)
except Exception as e:
    print(f"Warning: Could not connect to Neo4j. {e}")
    neo4j_client = None

def get_neo4j():
    return neo4j_client
