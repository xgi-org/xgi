"""Utility functions for compressed file handling."""

COMPRESSED_EXTENSIONS = (".gz", ".bz2", ".xz", ".zst")


def is_compressed_path(path, kwargs=None):
    """Check if the path ends with a supported compressed extension
    or if format is specified in kwargs.

    Parameters
    ----------
    path : str
        The file path to check
    kwargs : dict, optional
        Additional keyword arguments that may contain 'format'

    Returns
    -------
    bool
        True if the file should be opened with compression
    """
    if kwargs is not None and kwargs.get("format"):
        return True
    return any(path.endswith(ext) for ext in COMPRESSED_EXTENSIONS)