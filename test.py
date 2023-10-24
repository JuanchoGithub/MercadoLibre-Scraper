def modify_query(query):
    if 'ILIKE' in query:
        field = query.split('ILIKE')[0].split()[-1]
        value = query.split('ILIKE')[1].strip().strip("'").lower()
        modified_query = query.replace('ILIKE', 'LIKE').replace(field, f'LOWER({field})').replace(value, f"'{value}'")
        return modified_query
    return query

example = "${TABLE}.field ILIKE '%Testing%'"
print(f"Example: {example}")
print(f"Changed: {modify_query(example)}")