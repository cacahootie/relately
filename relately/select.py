
def aggregate_right_operand(query):
    kws = ('all', 'any', 'none')
    subcount, subvals = 0, []
    for kw in kws:
        try:
            params = []
            for x in query[kw]:
                params.append(x['right_operand'])
                x['right_operand'] = '%({})s'.format(subcount)
                subcount += 1
        except KeyError:
            continue
        subvals += params
    return query, subvals


def Select(engine, query, mogrify=False):
    query, params = aggregate_right_operand(query)
    sql = engine.jenv.get_template('select.sql').render(query=query)
    if mogrify:
        return engine.mogrify(sql)
    return engine.execute(sql, params)
