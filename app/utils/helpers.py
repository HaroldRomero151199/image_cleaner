def extract_local_paths(saved: list) -> list:
    """
    Extract local paths from a list of (local_path, url) tuples.
    """
    return [item[0] for item in saved]


def extract_urls(saved: list) -> list:
    """
    Extract URLs from a list of (local_path, url) tuples.
    """
    return [item[1] for item in saved] 