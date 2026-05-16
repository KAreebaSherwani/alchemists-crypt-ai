import requests

payload = {
    'gameState': 'Chamber_02',
    'session_metadata': {'tick_id': 1, 'last_tactic_success': False, 'difficulty_scaling': 0.85},
    'player': {'pos': [12.4, 0.0, 5.2], 'vel': [2.1, 0.0, -0.5], 'active_element': 'Sulfur', 'health': 80, 'is_firing': True},
    'mummies': [
        {'id': 1, 'pos': [2.0, 0.0, 2.1], 'hp': 50, 'state': 'Chasing'}, 
        {'id': 2, 'pos': [5.5, 0.0, 8.3], 'hp': 100, 'state': 'Chasing'}
    ]
}

print("Pinging HIVE MIND (Smart AI)...")
r = requests.post('https://alchemists-crypt-ai-production.up.railway.app/api/v1/hive-mind', json=payload)    
data = r.json()

print('\nHIVE MIND (Smart AI) Results:')
print('Tactic:', data.get('hive_tactic', 'No tactic found'))
for inst in data.get('instructions', []):
    print(f"  Mummy {inst['id']} -> action: {inst['action']} -> target: {inst['target']}")