"""Reference entry point: Gaussian mixture prototypes with the revised head."""
DESCRIPTION = 'Gaussian mixture prototypes with the revised head'

def configuration():
    return {"description": DESCRIPTION, "same_downstream_head": True, "history_h": 168, "horizon_h": 24}

if __name__ == "__main__":
    print(configuration())
