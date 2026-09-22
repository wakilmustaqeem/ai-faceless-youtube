"""Visual asset stage with a local-video readiness gate."""


def run(script: str, backend: str = "local-wan2.2-ti2v-5b", local_ready: bool = False) -> dict:
    """Queue visual production without claiming that a local renderer is available.

    Rendering is enabled only after the local preflight has been run and approved.
    """
    if not local_ready:
        return {
            "stage": "visuals",
            "status": "blocked_preflight",
            "backend": backend,
            "asset_sources": [],
            "next_action": "run scripts/check_local_video_env.py on the production machine",
        }
    return {
        "stage": "visuals",
        "status": "ready_to_render",
        "backend": backend,
        "asset_sources": [],
    }
