from common.neo4j.driver import neo4j_driver

driver = neo4j_driver


def execute_query(driver, query):
    with driver.session(database='neo4j') as session:
        session.run(query)



queries = {
    'load_concept_subset': """
    CALL {
    LOAD CSV WITH HEADERS FROM 'file:///Users/mannes/PycharmProjects/google/google_hackathon/import/data/CONCEPT.csv' AS row
    CREATE (:Concept {
        concept_id: row.concept_id,
        concept_name: row.concept_name,
        domain_id: row.domain_id,
        vocabulary_id: row.vocabulary_id,
        concept_class_id: row.concept_class_id,
        standard_concept: row.standard_concept,
        concept_code: row.concept_code,
        valid_start_date: row.valid_start_date,
        valid_end_date: row.valid_end_date,
        invalid_reason: row.invalid_reason
    })} IN TRANSACTIONS OF 500 ROWS
    """ ,
    'load_concept_ancestor': """
    CALL {
    LOAD CSV WITH HEADERS FROM 'file:////Users/mannes/PycharmProjects/google/google_hackathon/import/data/CONCEPT_ANCESTOR.csv' AS row
    CREATE (:ConceptAncestor {
        ancestor_concept_id: row.ancestor_concept_id,
        descendant_concept_id: row.descendant_concept_id,
        min_levels_of_separation: row.min_levels_of_separation,
        max_levels_of_separation: row.max_levels_of_separation
    })} IN TRANSACTIONS OF 500 ROWS
    """ ,
    'load_relationship_query' : """
    CALL {
    LOAD CSV WITH HEADERS FROM 'file:///Users/mannes/PycharmProjects/google/google_hackathon/import/data/RELATIONSHIP.csv' AS row
    CREATE (:Relationship {
        concept_id_1: row.concept_id_1,
        concept_id_2: row.concept_id_2,
        relationship_id: row.relationship_id,
        valid_start_date: row.valid_start_date,
        valid_end_date: row.valid_end_date,
        invalid_reason: row.invalid_reason
    })} IN TRANSACTIONS OF 500 ROWS
    """ 
}
# Batch size
batch_size = 1000

# Execute each query
for name, query in queries.items():
    print(f"Executing query: {name}")
    execute_query(driver, query)

# Close the Neo4j driver
driver.close()


def fetch_data(driver):
    with driver.session(database='hackathon') as session:
        result = session.run("MATCH (n:Concept) RETURN n LIMIT 10")
        for record in result:
            print(record)


fetch_data(driver)
driver.close()
