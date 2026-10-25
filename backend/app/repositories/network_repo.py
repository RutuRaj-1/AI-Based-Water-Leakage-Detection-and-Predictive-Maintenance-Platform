"""
Network Repository.
"""

from typing import Any, Dict, List, Optional
from app.simulation.network_builder import PuneNetworkBuilder


class NetworkRepository:
    def __init__(self):
        self.network = PuneNetworkBuilder.get_network_metadata()

    def list_networks(self, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        items = [self.network]
        return {
            "items": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": len(items),
                "total_pages": 1,
            },
        }

    def get_network(self, network_id: str) -> Optional[Dict[str, Any]]:
        if network_id in [self.network["id"], self.network["code"], "default", "pune"]:
            return self.network
        return self.network
