"""Reproducible deterministic MODEL, not a Kubernetes run. Standard library only.
Assumptions: readiness poll 5s, 2 failed polls to remove a faulty endpoint;
controller observes missing replica at t=5, replacement startup/readiness at t=20;
all-replica scenario: 2 replacements come up at t=25;
DB scenario: fail t=0, recognized t=10, DB repaired at t=180,
ready on next poll t=185. Results are scenario design inputs, not observations.
"""
import csv, json, pathlib
root=pathlib.Path(__file__).parent/'evidence'; root.mkdir(exist_ok=True)
scenarios=[
 {'id':1,'name':'One Registration replica fails','detection_s':10,'recovery_s':20,'user_impact':'Second replica remains online; reduced headroom, possibly brief 5xx before removal','method':'deterministic model; a failed endpoint removed after two readiness checks'},
 {'id':2,'name':'Both Registration replicas fail','detection_s':10,'recovery_s':25,'user_impact':'Registration unavailable until first replacement is ready; other services unaffected','method':'deterministic model; deployment replaces pods, 25s startup assumption'},
 {'id':3,'name':'Database becomes unavailable','detection_s':10,'recovery_s':185,'user_impact':'DB-dependent registration requests fail; readiness removes both endpoints','method':'deterministic model; DB manually restored at t=180, next readiness check t=185'},
]
with (root/'simulated_results.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=scenarios[0]);w.writeheader();w.writerows(scenarios)
(root/'simulated_results.json').write_text(json.dumps({'type':'MODEL_ONLY','not_real_cluster_measurements':True,'assumptions':__doc__.strip(),'results':scenarios},ensure_ascii=False,indent=2),encoding='utf-8')
for s in scenarios:
 lines=['MODEL EVENT TRACE — NOT KUBERNETES LOG','t=000s failure injected (model)','t=%03ds detection (model)'%s['detection_s'],'t=%03ds service recovered (model)'%s['recovery_s'],'user impact: '+s['user_impact']]
 (root/('model_trace_%d.txt'%s['id'])).write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Created simulated_results.csv/json and 3 model traces. MODEL ONLY.')
