import uncurl
import jsw_nx as nx
import requests

def get_hmwk_data(context):
    url = context.url
    headers = context.headers
    res = requests.get(url, headers=headers)
    return res.json()

def get_submit_data(hmwk_data, context):
    params = nx.qs(context.url)
    homework_id = params['homework_id']
    id = nx.get(hmwk_data, 'data.id')
    ids = nx.get(hmwk_data, "meta.finished_exercise_ids")
    results = nx.map(ids, lambda v,i: { "eid": v})
    return ids, {"id": id, "homework_id": homework_id, "results": results}

# open file as string
with open('.tmp/homework_submit_failed.txt', 'r') as f:
    context = uncurl.parse_context(f.read())
    ids, submit_data = get_submit_data(get_hmwk_data(context), context)
    if len(ids) > 0:
        url = nx.tmpl("https://student-api.alo7.com/api/v1/extend_units/{id}/exercise_results",{"id":id})
        res = requests.post(url, data= submit_data)
        print(res.json())
    else:
        print("no exercise_ids")