"""Reference entry point: Conventional spherical granular-ball regression."""
DESCRIPTION = 'Conventional spherical granular-ball regression'

def configuration():
    return {"description": DESCRIPTION, "same_downstream_head": True, "history_h": 168, "horizon_h": 24}

if __name__ == "__main__":
    print(configuration())
