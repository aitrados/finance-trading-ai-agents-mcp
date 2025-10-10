import httpx
import json
from typing import Optional, Dict, Any, Union


class RemoteCurl:
    headers = {
        "User-Agent": "Dataset-Python-Client/1.0",
        "Accept": "application/json",
    }

    @classmethod
    def get_setup_http_client(cls, timeout=5) -> httpx.Client:
        """
        Setup HTTP client with default configuration.
        """
        client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            headers=cls.headers,
        )
        return client

    @classmethod
    def curl(cls, url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None,
             data: Optional[Union[Dict[str, Any], str]] = None, timeout: int = 5) -> Dict[str, Any]:
        """
        Execute HTTP requests, similar to curl command

        Args:
            url: Request URL
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            headers: Additional request headers
            data: Request data, can be dictionary or JSON string
            timeout: Timeout in seconds

        Returns:
            Dictionary containing response information
        """
        try:
            # Merge default headers with custom headers
            merged_headers = cls.headers.copy()
            if headers:
                merged_headers.update(headers)

            # Create HTTP client
            client = cls.get_setup_http_client(timeout)

            # Prepare request parameters
            request_kwargs = {
                "url": url,
                "method": method.upper(),
                "headers": merged_headers
            }

            # Process request data
            if data is not None:
                if method.upper() in ["POST", "PUT", "PATCH"]:
                    if isinstance(data, dict):
                        # If it's a dictionary, convert to JSON
                        request_kwargs["json"] = data
                        merged_headers["Content-Type"] = "application/json"
                    elif isinstance(data, str):
                        # If it's a string, send directly as content
                        request_kwargs["content"] = data
                        if "Content-Type" not in merged_headers:
                            merged_headers["Content-Type"] = "application/json"
                else:
                    # For GET requests etc., use data as query parameters
                    if isinstance(data, dict):
                        request_kwargs["params"] = data

            # Send request
            with client as http_client:
                response = http_client.request(**request_kwargs)

                # Construct return result
                result = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "url": str(response.url),
                    "method": method.upper(),
                    "success": response.is_success,
                }

                # Try to parse response content
                try:
                    # First try to parse as JSON
                    result["data"] = response.json()
                    result["content_type"] = "json"
                except json.JSONDecodeError:
                    # If not JSON, return text content
                    result["data"] = response.text
                    result["content_type"] = "text"

                # If request is not successful, add error information
                if not response.is_success:
                    result["error"] = f"HTTP {response.status_code}: {response.reason_phrase}"
                client.close()
                return result

        except httpx.TimeoutException:
            return {
                "success": False,
                "error": f"Request timeout ({timeout} seconds)",
                "status_code": 0,
                "url": url,
                "method": method.upper()
            }
        except httpx.ConnectError as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}",
                "status_code": 0,
                "url": url,
                "method": method.upper()
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unknown error: {str(e)}",
                "status_code": 0,
                "url": url,
                "method": method.upper()
            }

    @classmethod
    def get(cls, url: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None, timeout: int = 5) -> Dict[str, Any]:
        """Convenient method for GET requests"""
        return cls.curl(url, method="GET", headers=headers, data=params, timeout=timeout)

    @classmethod
    def post(cls, url: str, data: Optional[Union[Dict[str, Any], str]] = None,
             headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Dict[str, Any]:
        """Convenient method for POST requests"""
        return cls.curl(url, method="POST", headers=headers, data=data, timeout=timeout)

    @classmethod
    def put(cls, url: str, data: Optional[Union[Dict[str, Any], str]] = None,
            headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Dict[str, Any]:
        """Convenient method for PUT requests"""
        return cls.curl(url, method="PUT", headers=headers, data=data, timeout=timeout)

    @classmethod
    def delete(cls, url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Dict[str, Any]:
        """Convenient method for DELETE requests"""
        return cls.curl(url, method="DELETE", headers=headers, timeout=timeout)

'''
# Usage examples
if __name__ == "__main__":
    # GET request example
    result = RemoteCurl.get("https://httpbin.org/get", params={"key": "value"})
    print("GET result:", result)

    # POST request example
    post_data = {"name": "test", "value": 123}
    result = RemoteCurl.post("https://httpbin.org/post", data=post_data)
    print("POST result:", result)

    # Using custom headers
    custom_headers = {"Authorization": "Bearer token123"}
    result = RemoteCurl.get("https://httpbin.org/headers", headers=custom_headers)
    print("Request with headers:", result)

    # Test your MCP server
    mcp_headers = {"SECRET_KEY": "YOUR_SECRET_KEY"}
    result = RemoteCurl.get("http://127.0.0.1:9000/traditional_indicator/", headers=mcp_headers)
    print("MCP server test:", result)
'''