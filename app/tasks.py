from celery import shared_task  
from time import sleep  

@shared_task(ignore_result=False)  
def long_running_task(iterations):  
    for i in range(iterations):  
        sleep(1)
        print(f"Iteration {i + 1}/{iterations} completed")  
    return f"Task completed after {iterations} iterations"  
