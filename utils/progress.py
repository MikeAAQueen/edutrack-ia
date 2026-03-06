import pandas as pd

def calculate_progress(df_tasks):
    """
    Calculates the overall completion progress from a pandas DataFrame of tasks.
    Returns the percentage as a float.
    """
    if df_tasks.empty:
        return 0.0
    
    total_tasks = len(df_tasks)
    completed_tasks = len(df_tasks[df_tasks['completed'] == True])
    
    percentage = (completed_tasks / total_tasks) * 100
    return percentage
