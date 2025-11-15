
import pandas as pd
import pulp as pl

def solve_assignment(tasks_df: pd.DataFrame, availability_df: pd.DataFrame):
   
    programmers = [c for c in tasks_df.columns if c != 'task']
    tasks = tasks_df['task'].tolist()

    t = {}
    allowed = {}
    for _, row in tasks_df.iterrows():
        task = row['task']
        for prog in programmers:
            val = row.get(prog)
            if pd.isna(val) or float(val) <= 0:
                allowed[(prog, task)] = False
                t[(prog, task)] = 0.0
            else:
                allowed[(prog, task)] = True
                t[(prog, task)] = float(val)

    availability = {row['programmer']: float(row['availability_hours']) 
                    for _, row in availability_df.iterrows()}

    # Model
    model = pl.LpProblem('Asignacion_Tareas', pl.LpMinimize)
    x = pl.LpVariable.dicts('x', (programmers, tasks), lowBound=0, upBound=1, cat='Binary')

  
    model += pl.lpSum(t[(i, j)] * x[i][j] for i in programmers for j in tasks if allowed[(i,j)])

    for j in tasks:
        model += pl.lpSum(x[i][j] for i in programmers if allowed[(i,j)]) == 1, f"assign_{j}"

    for i in programmers:
        model += pl.lpSum(t[(i, j)] * x[i][j] for j in tasks if allowed[(i,j)]) <= availability[i], f"cap_{i}"

    for i in programmers:
        for j in tasks:
            if not allowed[(i,j)]:
                model += x[i][j] == 0, f"ban_{i}_{j}"

    
    status = model.solve(pl.PULP_CBC_CMD(msg=False))
    status_str = pl.LpStatus[model.status]

    if status_str != 'Optimal':
        return {
            "status": status_str,
            "objective": None,
            "assignment": pd.DataFrame(columns=['task','programmer','hours']),
            "load": pd.DataFrame(columns=['programmer','assigned_hours']),
            "raw": model
        }

    rows = []
    for i in programmers:
        for j in tasks:
            if x[i][j].value() is not None and int(round(x[i][j].value())) == 1:
                rows.append({'task': j, 'programmer': i, 'hours': t[(i,j)]})
    assignment_df = pd.DataFrame(rows)

    load_df = assignment_df.groupby('programmer', as_index=False)['hours'].sum().rename(columns={'hours':'assigned_hours'})
  
    load_df = pd.merge(pd.DataFrame({'programmer': programmers}), load_df, on='programmer', how='left').fillna({'assigned_hours':0.0})

    objective_value = pl.value(model.objective)

    return {
        "status": status_str,
        "objective": objective_value,
        "assignment": assignment_df,
        "load": load_df,
        "raw": model
    }

