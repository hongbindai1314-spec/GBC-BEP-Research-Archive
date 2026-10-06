"""Reference entry point: Single-level granular-ball representation."""
DESCRIPTION = 'Single-level granular-ball representation'

def configuration():
    return {"description": DESCRIPTION, "same_downstream_head": True, "history_h": 168, "horizon_h": 24}

if __name__ == "__main__":
    print(configuration())
