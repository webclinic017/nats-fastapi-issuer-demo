from __future__ import annotations

from typing import Any, List, Optional

from quara.wiring.core.container import Container
from quara.wiring.core.settings import BaseAppSettings


def prometheus_metrics_provider(
    container: Container[BaseAppSettings],
) -> Optional[List[Any]]:
    """Add prometheus metrics to your application."""
    if container.settings.telemetry.metrics_enabled:
        from prometheus_fastapi_instrumentator import Instrumentator

        instrumentor = Instrumentator(
            excluded_handlers=[
                path.strip()
                for path in container.settings.telemetry.ignore_path.split(",")
            ]
        )
        instrumentor.instrument(container.app).expose(
            container.app,
            endpoint=container.settings.telemetry.metrics_path,
            include_in_schema=True,
            tags=["Telemetry"],
        )

        return [instrumentor]
