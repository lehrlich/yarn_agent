"""
Ravelry API client for fetching yarn data.

Note: Ravelry has a public API that requires authentication.
Get credentials at: https://www.ravelry.com/pro/developer
"""

import time
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any
from ratelimit import limits, sleep_and_retry

from ..models.yarn import Yarn, YarnMetrics


class RavelryClient:
    """Client for interacting with the Ravelry API."""

    BASE_URL = "https://api.ravelry.com"

    def __init__(self, access_key: str, personal_key: str, rate_limit: int = 1):
        """
        Initialize the Ravelry client.

        Args:
            access_key: Ravelry API access key
            personal_key: Ravelry API personal key
            rate_limit: Maximum requests per second (default: 1)
        """
        self.auth = (access_key, personal_key)
        self.rate_limit = rate_limit
        self.session = requests.Session()

    @sleep_and_retry
    @limits(calls=1, period=1)  # 1 call per second by default
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a rate-limited request to the Ravelry API.

        Args:
            endpoint: API endpoint (e.g., "/yarns/search.json")
            params: Query parameters

        Returns:
            JSON response as dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, auth=self.auth, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            raise

    def search_yarns(
        self,
        query: Optional[str] = None,
        weight: Optional[str] = None,
        fiber: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
        sort: str = "projects",
    ) -> List[Yarn]:
        """
        Search for yarns on Ravelry.

        Args:
            query: General search query (brand, name, etc.)
            weight: Yarn weight filter (e.g., "Fingering", "Worsted")
            fiber: Fiber type filter (e.g., "Wool", "Cotton")
            page: Page number for pagination
            page_size: Number of results per page
            sort: Sort order ("projects", "name", "rating")

        Returns:
            List of Yarn objects
        """
        params = {
            "page": page,
            "page_size": page_size,
            "sort": sort,
        }

        if query:
            params["query"] = query
        if weight:
            params["weight"] = weight
        if fiber:
            params["fiber"] = fiber

        response = self._make_request("/yarns/search.json", params)
        yarns = []

        for yarn_data in response.get("yarns", []):
            yarn = self._parse_yarn(yarn_data)
            if yarn:
                yarns.append(yarn)

        return yarns

    def get_yarn_details(self, yarn_id: str) -> Optional[Yarn]:
        """
        Get detailed information about a specific yarn.

        Args:
            yarn_id: Ravelry yarn ID

        Returns:
            Yarn object with detailed information
        """
        try:
            response = self._make_request(f"/yarns/{yarn_id}.json")
            yarn_data = response.get("yarn", {})
            return self._parse_yarn(yarn_data)
        except Exception as e:
            print(f"Error fetching yarn {yarn_id}: {e}")
            return None

    def get_popular_yarns(
        self,
        limit: int = 100,
        weight: Optional[str] = None,
        fiber: Optional[str] = None
    ) -> List[Yarn]:
        """
        Get the most popular yarns based on project count.

        This is the key method for trend analysis - it autonomously
        samples the most relevant yarns for analysis.

        Args:
            limit: Maximum number of yarns to retrieve
            weight: Filter by yarn weight
            fiber: Filter by fiber type

        Returns:
            List of popular Yarn objects
        """
        yarns = []
        page = 1
        page_size = 50

        while len(yarns) < limit:
            batch = self.search_yarns(
                weight=weight,
                fiber=fiber,
                page=page,
                page_size=page_size,
                sort="projects"
            )

            if not batch:
                break

            yarns.extend(batch)
            page += 1

            if len(batch) < page_size:
                break

        return yarns[:limit]

    def get_yarns_by_category(self, category: str, limit: int = 50) -> List[Yarn]:
        """
        Get yarns for a specific category (weight or fiber).

        This enables autonomous sampling across different categories
        for comparative trend analysis.

        Args:
            category: Category to search (e.g., "Fingering", "Wool")
            limit: Maximum number of yarns

        Returns:
            List of Yarn objects in that category
        """
        # Determine if category is a weight or fiber
        weights = ["Thread", "Cobweb", "Lace", "Light Fingering", "Fingering",
                   "Sport", "DK", "Worsted", "Aran", "Bulky", "Super Bulky", "Jumbo"]

        if category in weights:
            return self.get_popular_yarns(limit=limit, weight=category)
        else:
            return self.get_popular_yarns(limit=limit, fiber=category)

    def _parse_yarn(self, yarn_data: Dict[str, Any]) -> Optional[Yarn]:
        """
        Parse yarn data from Ravelry API response.

        Args:
            yarn_data: Raw yarn data from API

        Returns:
            Yarn object or None if parsing fails
        """
        try:
            metrics = YarnMetrics(
                project_count=yarn_data.get("projects", 0),
                favorites=yarn_data.get("favorites", 0),
                rating=yarn_data.get("rating_average"),
                comments=yarn_data.get("comments", 0),
                queued=yarn_data.get("queued_projects_count", 0),
                in_stash=yarn_data.get("stash_count", 0),
            )

            # Parse yarn weight
            weight_data = yarn_data.get("yarn_weight", {})
            yarn_weight = weight_data.get("name", "Unknown") if weight_data else "Unknown"

            # Parse fiber type (take first fiber if multiple)
            fiber_data = yarn_data.get("yarn_fibers", [])
            fiber_type = fiber_data[0].get("fiber_type", {}).get("name", "Unknown") if fiber_data else "Unknown"

            # Brand info
            company = yarn_data.get("yarn_company", {})
            brand = company.get("name", "Unknown") if company else "Unknown"

            yarn = Yarn(
                id=str(yarn_data.get("id")),
                name=yarn_data.get("name", "Unknown"),
                brand=brand,
                yarn_weight=yarn_weight,
                fiber_type=fiber_type,
                metrics=metrics,
                scraped_at=datetime.now(),
                permalink=yarn_data.get("permalink"),
                yardage=yarn_data.get("yardage"),
                grams=yarn_data.get("grams"),
                texture=yarn_data.get("texture"),
                discontinued=yarn_data.get("discontinued", False),
            )

            return yarn

        except Exception as e:
            print(f"Error parsing yarn data: {e}")
            return None
