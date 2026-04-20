from my_first_ai_agent.cat_agent import run_cat_agent
import json

def handler(event, context):
    run_cat_agent()

    return {
        'statusCode': 200,
        'body': json.dumps(f"executed cat agent")
    }