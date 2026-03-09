import json
from app.agent.graph import graph

requests = [
    {
        'file': 'demo_outputs/script_india.txt',
        'input': {'country': 'IN', 'topic_category': 'tech', 'niche_context': 'AI tools for developers', 'prompt_strategy': 'few_shot'}
    },
    {
        'file': 'demo_outputs/script_usa.txt',
        'input': {'country': 'US', 'topic_category': 'finance', 'niche_context': 'Bitcoin and crypto', 'prompt_strategy': 'few_shot'}
    },
    {
        'file': 'demo_outputs/script_ai.txt',
        'input': {'country': 'US', 'topic_category': 'tech', 'niche_context': 'AI coding assistants', 'prompt_strategy': 'few_shot'}
    }
]

for req in requests:
    print(f'Generating {req["file"]}...')
    try:
        result = graph.invoke(req['input'])
        with open(req['file'], 'w', encoding='utf-8') as f:
            json.dump(result['final_response'], f, indent=2, ensure_ascii=False)
        print(f'Saved {req["file"]}')
    except Exception as e:
        print(f'Error generating {req["file"]}: {e}')
