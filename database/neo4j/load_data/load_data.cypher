
LOAD CSV WITH HEADERS FROM 'file:///Users/mannes/PycharmProjects/google/google_hackathon/import/CONCEPT_SUBSET.csv' AS row
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
});

LOAD CSV WITH HEADERS FROM 'file:///Users/mannes/PycharmProjects/google/google_hackathon/import/CONCEPT_ANDESTOR.csv' AS row
CREATE (:ConceptAncestor {
    ancestor_concept_id: row.ancestor_concept_id,
    descendant_concept_id: row.descendant_concept_id,
    min_levels_of_separation: row.min_levels_of_separation,
    max_levels_of_separation: row.max_levels_of_separation
})