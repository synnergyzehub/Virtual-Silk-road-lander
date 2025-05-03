"""
VOI Jeans SynnergyzeOS Integration Module

This module implements the API integration between VOI Jeans, the Genesis Stack,
and the SynnergyzeOS ERP system at saasapps.in. It provides connector classes and
utility functions for handling transactions, inventory, and reporting.
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import logging
import hashlib
import hmac
import base64
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("voi_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("voi_synnergyze")

class SynnergyzeConnector:
    """
    Core connector class for SynnergyzeOS API integration.
    Handles authentication and base API requests.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the SynnergyzeOS connector.
        
        Args:
            config_file: Path to configuration file (optional)
        """
        # Default configuration
        self.config = {
            "api_base_url": "https://saasapps.in:2082/api",
            "auth_endpoint": "/auth/token",
            "username": os.environ.get("SYNNERGYZE_USERNAME", "Synnadmin"),
            "password": os.environ.get("SYNNERGYZE_PASSWORD", "Gyze@#7171"),
            "client_id": os.environ.get("SYNNERGYZE_CLIENT_ID", ""),
            "client_secret": os.environ.get("SYNNERGYZE_CLIENT_SECRET", ""),
            "timeout": 30,
            "retry_count": 3,
            "retry_delay": 2
        }
        
        # Load configuration from file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        
        # Initialize session and auth token
        self.session = requests.Session()
        self.auth_token = None
        self.token_expiry = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with SynnergyzeOS API and obtain access token.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            auth_url = f"{self.config['api_base_url']}{self.config['auth_endpoint']}"
            
            # Prepare authentication payload
            auth_data = {
                "username": self.config["username"],
                "password": self.config["password"],
                "grant_type": "password"
            }
            
            # Add client credentials if available
            if self.config["client_id"] and self.config["client_secret"]:
                auth_data["client_id"] = self.config["client_id"]
                auth_data["client_secret"] = self.config["client_secret"]
            
            # Make authentication request
            response = self.session.post(
                auth_url,
                json=auth_data,
                timeout=self.config["timeout"]
            )
            
            # Check response
            if response.status_code == 200:
                auth_response = response.json()
                self.auth_token = auth_response.get("access_token")
                
                # Calculate token expiry (default to 1 hour if not specified)
                expires_in = auth_response.get("expires_in", 3600)
                self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
                
                # Update session headers with auth token
                self.session.headers.update({
                    "Authorization": f"Bearer {self.auth_token}",
                    "Content-Type": "application/json"
                })
                
                logger.info("Successfully authenticated with SynnergyzeOS API")
                return True
            else:
                logger.error(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def ensure_authenticated(self) -> bool:
        """
        Ensure the connector has a valid authentication token.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        # Check if token exists and is not expired
        if not self.auth_token or not self.token_expiry or datetime.now() >= self.token_expiry:
            return self.authenticate()
        return True
    
    def api_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                   params: Optional[Dict] = None, retry: int = 0) -> Dict:
        """
        Make an API request to SynnergyzeOS.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request payload (optional)
            params: Query parameters (optional)
            retry: Current retry attempt
            
        Returns:
            Dict: API response as dictionary
        """
        # Ensure we have a valid auth token
        if not self.ensure_authenticated():
            raise ConnectionError("Failed to authenticate with SynnergyzeOS API")
        
        try:
            # Construct full URL
            url = f"{self.config['api_base_url']}{endpoint}"
            
            # Make the request
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params if params else None,
                timeout=self.config["timeout"]
            )
            
            # Handle response based on status code
            if response.status_code in (200, 201, 204):
                # Successful response
                if response.content:
                    return response.json()
                return {"status": "success"}
                
            elif response.status_code == 401:
                # Authentication error - retry once with fresh token
                if retry < 1:
                    logger.info("Authentication token expired, refreshing")
                    self.authenticate()
                    return self.api_request(method, endpoint, data, params, retry + 1)
                else:
                    raise ConnectionError("Authentication failed after retry")
                    
            elif response.status_code >= 500:
                # Server error - retry with backoff
                if retry < self.config["retry_count"]:
                    retry_delay = self.config["retry_delay"] * (2 ** retry)
                    logger.warning(f"Server error, retrying in {retry_delay}s")
                    time.sleep(retry_delay)
                    return self.api_request(method, endpoint, data, params, retry + 1)
                else:
                    raise ConnectionError(f"Server error after {retry} retries")
            
            else:
                # Other error
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise requests.HTTPError(error_msg)
                
        except (requests.RequestException, ConnectionError) as e:
            logger.error(f"API request error: {str(e)}")
            raise
            
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Convenience method for GET requests"""
        return self.api_request("GET", endpoint, params=params)
        
    def post(self, endpoint: str, data: Dict) -> Dict:
        """Convenience method for POST requests"""
        return self.api_request("POST", endpoint, data=data)
        
    def put(self, endpoint: str, data: Dict) -> Dict:
        """Convenience method for PUT requests"""
        return self.api_request("PUT", endpoint, data=data)
        
    def delete(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Convenience method for DELETE requests"""
        return self.api_request("DELETE", endpoint, params=params)


class SalesTransactionManager:
    """
    Manager class for sales transactions between VOI Jeans and SynnergyzeOS.
    """
    
    def __init__(self, connector: SynnergyzeConnector):
        """
        Initialize the sales transaction manager.
        
        Args:
            connector: SynnergyzeConnector instance
        """
        self.connector = connector
        self.sales_endpoint = "/dc_DocumentsSales"
        
    def get_sales_transactions(self, start_date: Optional[str] = None, 
                             end_date: Optional[str] = None,
                             channel: Optional[str] = None,
                             store_id: Optional[str] = None,
                             limit: int = 100, 
                             offset: int = 0) -> Dict:
        """
        Retrieve sales transactions with filtering options.
        
        Args:
            start_date: Start date for filtering (YYYY-MM-DD)
            end_date: End date for filtering (YYYY-MM-DD)
            channel: Sales channel filter (EBO, MBO, etc.)
            store_id: Specific store ID
            limit: Maximum number of records to return
            offset: Pagination offset
            
        Returns:
            Dict: Sales transaction data
        """
        # Prepare query parameters
        params = {
            "limit": limit,
            "offset": offset
        }
        
        # Add optional filters
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if channel:
            params["channel"] = channel
        if store_id:
            params["storeId"] = store_id
            
        # Make API request
        try:
            response = self.connector.get(self.sales_endpoint, params=params)
            logger.info(f"Retrieved {len(response.get('transactions', []))} sales transactions")
            return response
        except Exception as e:
            logger.error(f"Error retrieving sales transactions: {str(e)}")
            raise
    
    def create_sales_transaction(self, transaction_data: Dict) -> Dict:
        """
        Create a new sales transaction in SynnergyzeOS.
        
        Args:
            transaction_data: Transaction data dictionary
            
        Returns:
            Dict: Created transaction response
        """
        try:
            # Add timestamp if not present
            if "timestamp" not in transaction_data:
                transaction_data["timestamp"] = datetime.now().isoformat()
                
            # Add divine alignment metadata
            transaction_data["divineMetadata"] = {
                "alignmentScore": self._calculate_divine_alignment(transaction_data),
                "verificationTimestamp": datetime.now().isoformat(),
                "governanceLevel": "standard"
            }
                
            # Make API request
            response = self.connector.post(self.sales_endpoint, transaction_data)
            logger.info(f"Created sales transaction with ID: {response.get('transactionId')}")
            return response
        except Exception as e:
            logger.error(f"Error creating sales transaction: {str(e)}")
            raise
    
    def update_sales_transaction(self, transaction_id: str, transaction_data: Dict) -> Dict:
        """
        Update an existing sales transaction.
        
        Args:
            transaction_id: Transaction ID to update
            transaction_data: Updated transaction data
            
        Returns:
            Dict: Updated transaction response
        """
        try:
            # Add update timestamp
            transaction_data["lastUpdated"] = datetime.now().isoformat()
            
            # Update divine alignment metadata
            transaction_data["divineMetadata"] = {
                "alignmentScore": self._calculate_divine_alignment(transaction_data),
                "verificationTimestamp": datetime.now().isoformat(),
                "governanceLevel": "standard"
            }
                
            # Make API request
            endpoint = f"{self.sales_endpoint}/{transaction_id}"
            response = self.connector.put(endpoint, transaction_data)
            logger.info(f"Updated sales transaction with ID: {transaction_id}")
            return response
        except Exception as e:
            logger.error(f"Error updating sales transaction: {str(e)}")
            raise
            
    def get_transaction_by_id(self, transaction_id: str) -> Dict:
        """
        Retrieve a specific transaction by ID.
        
        Args:
            transaction_id: Transaction ID to retrieve
            
        Returns:
            Dict: Transaction data
        """
        try:
            endpoint = f"{self.sales_endpoint}/{transaction_id}"
            response = self.connector.get(endpoint)
            logger.info(f"Retrieved transaction with ID: {transaction_id}")
            return response
        except Exception as e:
            logger.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
            raise
    
    def delete_transaction(self, transaction_id: str) -> Dict:
        """
        Delete a transaction by ID.
        
        Args:
            transaction_id: Transaction ID to delete
            
        Returns:
            Dict: Deletion response
        """
        try:
            endpoint = f"{self.sales_endpoint}/{transaction_id}"
            response = self.connector.delete(endpoint)
            logger.info(f"Deleted transaction with ID: {transaction_id}")
            return response
        except Exception as e:
            logger.error(f"Error deleting transaction {transaction_id}: {str(e)}")
            raise
    
    def _calculate_divine_alignment(self, transaction_data: Dict) -> float:
        """
        Calculate divine alignment score for a transaction.
        
        Args:
            transaction_data: Transaction data to evaluate
            
        Returns:
            float: Divine alignment score (0-100)
        """
        # Base alignment score
        alignment = 85.0
        
        # Adjust based on transaction attributes
        
        # Check for fair pricing
        if "items" in transaction_data:
            for item in transaction_data["items"]:
                if item.get("discount", 0) > 40:
                    # Excessive discounts reduce alignment
                    alignment -= 5
        
        # Check for proper documentation
        if not all(k in transaction_data for k in ["customerId", "storeId", "items"]):
            alignment -= 10
            
        # Check for appropriate channel
        if transaction_data.get("channel") not in ["EBO", "MBO", "LIFESTYLE", "ECOMMERCE"]:
            alignment -= 5
            
        # Ensure score is within bounds
        alignment = max(0, min(100, alignment))
        
        return alignment


class InventorySyncManager:
    """
    Manager class for inventory synchronization between VOI Jeans and SynnergyzeOS.
    """
    
    def __init__(self, connector: SynnergyzeConnector):
        """
        Initialize the inventory synchronization manager.
        
        Args:
            connector: SynnergyzeConnector instance
        """
        self.connector = connector
        self.inventory_endpoint = "/dc_DocumentsSales/inventory"
        
    def get_inventory(self, store_id: Optional[str] = None, 
                    product_id: Optional[str] = None,
                    category: Optional[str] = None) -> Dict:
        """
        Retrieve inventory data with filtering options.
        
        Args:
            store_id: Specific store ID filter
            product_id: Specific product ID filter
            category: Product category filter
            
        Returns:
            Dict: Inventory data
        """
        # Prepare query parameters
        params = {}
        
        # Add optional filters
        if store_id:
            params["storeId"] = store_id
        if product_id:
            params["productId"] = product_id
        if category:
            params["category"] = category
            
        # Make API request
        try:
            response = self.connector.get(self.inventory_endpoint, params=params)
            logger.info(f"Retrieved inventory data with {len(response.get('items', []))} items")
            return response
        except Exception as e:
            logger.error(f"Error retrieving inventory: {str(e)}")
            raise
    
    def update_inventory_item(self, item_id: str, inventory_data: Dict) -> Dict:
        """
        Update inventory item data.
        
        Args:
            item_id: Inventory item ID
            inventory_data: Updated inventory data
            
        Returns:
            Dict: Updated inventory response
        """
        try:
            # Add update timestamp
            inventory_data["lastUpdated"] = datetime.now().isoformat()
                
            # Make API request
            endpoint = f"{self.inventory_endpoint}/{item_id}"
            response = self.connector.put(endpoint, inventory_data)
            logger.info(f"Updated inventory item with ID: {item_id}")
            return response
        except Exception as e:
            logger.error(f"Error updating inventory item {item_id}: {str(e)}")
            raise
    
    def sync_inventory_levels(self, store_id: Optional[str] = None) -> Dict:
        """
        Perform a full inventory synchronization.
        
        Args:
            store_id: Optional store ID to sync only specific store
            
        Returns:
            Dict: Synchronization statistics
        """
        try:
            # Endpoint for sync operation
            endpoint = f"{self.inventory_endpoint}/sync"
            
            # Prepare sync data
            sync_data = {
                "syncTimestamp": datetime.now().isoformat(),
                "fullSync": True
            }
            
            # Add store filter if provided
            if store_id:
                sync_data["storeId"] = store_id
                
            # Make API request
            response = self.connector.post(endpoint, sync_data)
            
            # Log sync statistics
            if "stats" in response:
                stats = response["stats"]
                logger.info(f"Inventory sync completed: {stats.get('updated', 0)} updated, "
                          f"{stats.get('created', 0)} created, {stats.get('errors', 0)} errors")
            
            return response
        except Exception as e:
            logger.error(f"Error during inventory sync: {str(e)}")
            raise
    
    def get_low_stock_items(self, threshold: int = 10) -> Dict:
        """
        Get items with stock levels below threshold.
        
        Args:
            threshold: Stock level threshold
            
        Returns:
            Dict: Low stock items
        """
        try:
            endpoint = f"{self.inventory_endpoint}/low-stock"
            params = {"threshold": threshold}
            response = self.connector.get(endpoint, params=params)
            
            logger.info(f"Retrieved {len(response.get('items', []))} low stock items")
            return response
        except Exception as e:
            logger.error(f"Error retrieving low stock items: {str(e)}")
            raise


class ChannelManager:
    """
    Manager class for sales channel operations.
    """
    
    def __init__(self, connector: SynnergyzeConnector):
        """
        Initialize the channel manager.
        
        Args:
            connector: SynnergyzeConnector instance
        """
        self.connector = connector
        self.channels_endpoint = "/dc_DocumentsSales/channels"
        
    def get_channels(self) -> Dict:
        """
        Retrieve all available sales channels.
        
        Returns:
            Dict: Sales channels data
        """
        try:
            response = self.connector.get(self.channels_endpoint)
            logger.info(f"Retrieved {len(response.get('channels', []))} sales channels")
            return response
        except Exception as e:
            logger.error(f"Error retrieving sales channels: {str(e)}")
            raise
    
    def get_channel_performance(self, channel_id: str, 
                              start_date: Optional[str] = None,
                              end_date: Optional[str] = None) -> Dict:
        """
        Get performance metrics for a specific sales channel.
        
        Args:
            channel_id: Channel ID
            start_date: Start date for metrics (YYYY-MM-DD)
            end_date: End date for metrics (YYYY-MM-DD)
            
        Returns:
            Dict: Channel performance metrics
        """
        try:
            # Prepare endpoint and parameters
            endpoint = f"{self.channels_endpoint}/{channel_id}/performance"
            params = {}
            
            if start_date:
                params["startDate"] = start_date
            if end_date:
                params["endDate"] = end_date
                
            # Make API request
            response = self.connector.get(endpoint, params=params)
            logger.info(f"Retrieved performance metrics for channel {channel_id}")
            return response
        except Exception as e:
            logger.error(f"Error retrieving channel performance: {str(e)}")
            raise
    
    def get_channel_inventory(self, channel_id: str) -> Dict:
        """
        Get inventory allocation for a specific channel.
        
        Args:
            channel_id: Channel ID
            
        Returns:
            Dict: Channel inventory data
        """
        try:
            endpoint = f"{self.channels_endpoint}/{channel_id}/inventory"
            response = self.connector.get(endpoint)
            logger.info(f"Retrieved inventory data for channel {channel_id}")
            return response
        except Exception as e:
            logger.error(f"Error retrieving channel inventory: {str(e)}")
            raise


class ReportingManager:
    """
    Manager class for reporting and analytics.
    """
    
    def __init__(self, connector: SynnergyzeConnector):
        """
        Initialize the reporting manager.
        
        Args:
            connector: SynnergyzeConnector instance
        """
        self.connector = connector
        self.reporting_endpoint = "/dc_DocumentsSales/reports"
        
    def get_sales_report(self, report_type: str,
                       start_date: str,
                       end_date: str,
                       channel: Optional[str] = None,
                       store_id: Optional[str] = None,
                       format: str = "json") -> Dict:
        """
        Generate a sales report.
        
        Args:
            report_type: Type of report (daily, weekly, monthly, custom)
            start_date: Start date for report (YYYY-MM-DD)
            end_date: End date for report (YYYY-MM-DD)
            channel: Optional channel filter
            store_id: Optional store filter
            format: Report format (json, csv, xlsx)
            
        Returns:
            Dict: Report data or download link
        """
        try:
            # Prepare endpoint and parameters
            endpoint = f"{self.reporting_endpoint}/sales"
            params = {
                "type": report_type,
                "startDate": start_date,
                "endDate": end_date,
                "format": format
            }
            
            if channel:
                params["channel"] = channel
            if store_id:
                params["storeId"] = store_id
                
            # Make API request
            response = self.connector.get(endpoint, params=params)
            logger.info(f"Generated {report_type} sales report from {start_date} to {end_date}")
            return response
        except Exception as e:
            logger.error(f"Error generating sales report: {str(e)}")
            raise
    
    def get_inventory_report(self, report_type: str,
                          store_id: Optional[str] = None,
                          category: Optional[str] = None,
                          format: str = "json") -> Dict:
        """
        Generate an inventory report.
        
        Args:
            report_type: Type of report (current, historical, forecast)
            store_id: Optional store filter
            category: Optional product category filter
            format: Report format (json, csv, xlsx)
            
        Returns:
            Dict: Report data or download link
        """
        try:
            # Prepare endpoint and parameters
            endpoint = f"{self.reporting_endpoint}/inventory"
            params = {
                "type": report_type,
                "format": format
            }
            
            if store_id:
                params["storeId"] = store_id
            if category:
                params["category"] = category
                
            # Make API request
            response = self.connector.get(endpoint, params=params)
            logger.info(f"Generated {report_type} inventory report")
            return response
        except Exception as e:
            logger.error(f"Error generating inventory report: {str(e)}")
            raise
    
    def get_channel_comparison_report(self, 
                                   start_date: str,
                                   end_date: str,
                                   metrics: List[str],
                                   format: str = "json") -> Dict:
        """
        Generate a channel comparison report.
        
        Args:
            start_date: Start date for report (YYYY-MM-DD)
            end_date: End date for report (YYYY-MM-DD)
            metrics: List of metrics to include (sales, units, margin, etc.)
            format: Report format (json, csv, xlsx)
            
        Returns:
            Dict: Report data or download link
        """
        try:
            # Prepare endpoint and parameters
            endpoint = f"{self.reporting_endpoint}/channel-comparison"
            params = {
                "startDate": start_date,
                "endDate": end_date,
                "metrics": ",".join(metrics),
                "format": format
            }
                
            # Make API request
            response = self.connector.get(endpoint, params=params)
            logger.info(f"Generated channel comparison report from {start_date} to {end_date}")
            return response
        except Exception as e:
            logger.error(f"Error generating channel comparison report: {str(e)}")
            raise


class GenesisIntegrationManager:
    """
    Manager class for integrating SynnergyzeOS data with Genesis Stack.
    """
    
    def __init__(self, synnergyze_connector: SynnergyzeConnector, genesis_api_url: str, genesis_api_key: str):
        """
        Initialize the Genesis integration manager.
        
        Args:
            synnergyze_connector: SynnergyzeConnector instance
            genesis_api_url: Genesis Stack API URL
            genesis_api_key: Genesis Stack API key
        """
        self.synnergyze = synnergyze_connector
        self.genesis_api_url = genesis_api_url
        self.genesis_api_key = genesis_api_key
        
        # Initialize session for Genesis API
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.genesis_api_key}",
            "Content-Type": "application/json",
            "X-Divine-Alignment": "true"
        })
        
        # Initialize managers
        self.sales_manager = SalesTransactionManager(synnergyze_connector)
        self.inventory_manager = InventorySyncManager(synnergyze_connector)
        self.channel_manager = ChannelManager(synnergyze_connector)
        self.reporting_manager = ReportingManager(synnergyze_connector)
    
    def _genesis_api_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                          params: Optional[Dict] = None) -> Dict:
        """
        Make an API request to the Genesis Stack.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request payload (optional)
            params: Query parameters (optional)
            
        Returns:
            Dict: API response as dictionary
        """
        try:
            # Construct full URL
            url = f"{self.genesis_api_url}{endpoint}"
            
            # Make the request
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params if params else None,
                timeout=30
            )
            
            # Handle response
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {"status": "success"}
            
        except requests.RequestException as e:
            logger.error(f"Genesis API request error: {str(e)}")
            raise
    
    def sync_transaction_to_genesis(self, transaction_id: str) -> Dict:
        """
        Synchronize a transaction from SynnergyzeOS to Genesis Stack.
        
        Args:
            transaction_id: Transaction ID to synchronize
            
        Returns:
            Dict: Synchronization result
        """
        try:
            # Get transaction from SynnergyzeOS
            transaction = self.sales_manager.get_transaction_by_id(transaction_id)
            
            # Transform for Genesis
            genesis_transaction = self._transform_transaction_for_genesis(transaction)
            
            # Send to Genesis
            result = self._genesis_api_request(
                "POST", 
                "/api/v1/transactions", 
                data=genesis_transaction
            )
            
            logger.info(f"Synchronized transaction {transaction_id} to Genesis Stack")
            return result
        except Exception as e:
            logger.error(f"Error synchronizing transaction {transaction_id}: {str(e)}")
            raise
    
    def _transform_transaction_for_genesis(self, transaction: Dict) -> Dict:
        """
        Transform a SynnergyzeOS transaction for Genesis Stack.
        
        Args:
            transaction: SynnergyzeOS transaction data
            
        Returns:
            Dict: Transformed transaction for Genesis
        """
        # Basic transformation
        genesis_transaction = {
            "externalId": transaction.get("id"),
            "source": "SynnergyzeOS",
            "timestamp": transaction.get("timestamp"),
            "transactionType": "SALE",
            "storeId": transaction.get("storeId"),
            "channelId": transaction.get("channel"),
            "customerId": transaction.get("customerId"),
            "items": [],
            "totals": {
                "subtotal": transaction.get("subtotal", 0),
                "tax": transaction.get("tax", 0),
                "discount": transaction.get("discount", 0),
                "total": transaction.get("total", 0)
            },
            "paymentMethod": transaction.get("paymentMethod"),
            "sourceData": transaction
        }
        
        # Transform line items
        if "items" in transaction:
            for item in transaction["items"]:
                genesis_item = {
                    "productId": item.get("productId"),
                    "sku": item.get("sku"),
                    "name": item.get("name"),
                    "quantity": item.get("quantity", 0),
                    "unitPrice": item.get("unitPrice", 0),
                    "discount": item.get("discount", 0),
                    "tax": item.get("tax", 0),
                    "total": item.get("total", 0)
                }
                genesis_transaction["items"].append(genesis_item)
        
        # Add divine governance attributes
        genesis_transaction["divineAttributes"] = {
            "alignmentScore": transaction.get("divineMetadata", {}).get("alignmentScore", 85),
            "governanceLevel": transaction.get("divineMetadata", {}).get("governanceLevel", "standard"),
            "verificationTimestamp": datetime.now().isoformat()
        }
        
        return genesis_transaction
    
    def sync_inventory_to_genesis(self, full_sync: bool = False, store_id: Optional[str] = None) -> Dict:
        """
        Synchronize inventory from SynnergyzeOS to Genesis Stack.
        
        Args:
            full_sync: Perform a full synchronization
            store_id: Optional store ID filter
            
        Returns:
            Dict: Synchronization result
        """
        try:
            # Get inventory data
            inventory_data = self.inventory_manager.get_inventory(store_id=store_id)
            
            # Transform for Genesis
            genesis_inventory = self._transform_inventory_for_genesis(inventory_data, full_sync)
            
            # Send to Genesis
            result = self._genesis_api_request(
                "POST", 
                "/api/v1/inventory/sync", 
                data=genesis_inventory
            )
            
            logger.info(f"Synchronized inventory to Genesis Stack: {len(inventory_data.get('items', []))} items")
            return result
        except Exception as e:
            logger.error(f"Error synchronizing inventory: {str(e)}")
            raise
    
    def _transform_inventory_for_genesis(self, inventory_data: Dict, full_sync: bool) -> Dict:
        """
        Transform SynnergyzeOS inventory data for Genesis Stack.
        
        Args:
            inventory_data: SynnergyzeOS inventory data
            full_sync: Indicates if this is a full sync
            
        Returns:
            Dict: Transformed inventory for Genesis
        """
        genesis_inventory = {
            "source": "SynnergyzeOS",
            "timestamp": datetime.now().isoformat(),
            "fullSync": full_sync,
            "items": [],
            "sourceData": {} if full_sync else inventory_data
        }
        
        # Transform inventory items
        if "items" in inventory_data:
            for item in inventory_data["items"]:
                genesis_item = {
                    "productId": item.get("productId"),
                    "sku": item.get("sku"),
                    "name": item.get("name"),
                    "quantity": item.get("quantity", 0),
                    "availableQuantity": item.get("availableQuantity", 0),
                    "reservedQuantity": item.get("reservedQuantity", 0),
                    "storeId": item.get("storeId"),
                    "location": item.get("location", ""),
                    "lastUpdated": item.get("lastUpdated")
                }
                genesis_inventory["items"].append(genesis_item)
        
        # Add divine governance attributes
        genesis_inventory["divineAttributes"] = {
            "alignmentScore": 90,  # Inventory data typically has high alignment
            "governanceLevel": "standard",
            "verificationTimestamp": datetime.now().isoformat()
        }
        
        return genesis_inventory
    
    def generate_genesis_report(self, report_type: str, parameters: Dict) -> Dict:
        """
        Generate a report in Genesis Stack from SynnergyzeOS data.
        
        Args:
            report_type: Type of report to generate
            parameters: Report parameters
            
        Returns:
            Dict: Report generation result
        """
        try:
            # Get data from SynnergyzeOS based on report type
            synnergyze_data = None
            
            if report_type == "sales":
                synnergyze_data = self.reporting_manager.get_sales_report(
                    report_type=parameters.get("periodType", "daily"),
                    start_date=parameters.get("startDate"),
                    end_date=parameters.get("endDate"),
                    channel=parameters.get("channel"),
                    store_id=parameters.get("storeId")
                )
            elif report_type == "inventory":
                synnergyze_data = self.reporting_manager.get_inventory_report(
                    report_type=parameters.get("inventoryType", "current"),
                    store_id=parameters.get("storeId"),
                    category=parameters.get("category")
                )
            elif report_type == "channel":
                synnergyze_data = self.reporting_manager.get_channel_comparison_report(
                    start_date=parameters.get("startDate"),
                    end_date=parameters.get("endDate"),
                    metrics=parameters.get("metrics", ["sales", "units", "margin"])
                )
            
            # Transform for Genesis
            genesis_report_request = {
                "reportType": report_type,
                "parameters": parameters,
                "sourceData": synnergyze_data,
                "generateTimestamp": datetime.now().isoformat()
            }
            
            # Send to Genesis
            result = self._genesis_api_request(
                "POST", 
                "/api/v1/reports/generate", 
                data=genesis_report_request
            )
            
            logger.info(f"Generated {report_type} report in Genesis Stack")
            return result
        except Exception as e:
            logger.error(f"Error generating Genesis report: {str(e)}")
            raise


# Helper functions

def export_data_to_csv(data: List[Dict], filename: str) -> str:
    """
    Export data to a CSV file.
    
    Args:
        data: List of dictionaries containing data
        filename: Output filename
        
    Returns:
        str: Path to the created CSV file
    """
    try:
        df = pd.DataFrame(data)
        output_path = f"{filename}.csv"
        df.to_csv(output_path, index=False)
        logger.info(f"Exported data to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error exporting data to CSV: {str(e)}")
        raise


def import_data_from_csv(filepath: str) -> List[Dict]:
    """
    Import data from a CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        List[Dict]: Imported data as list of dictionaries
    """
    try:
        df = pd.read_csv(filepath)
        data = df.to_dict(orient="records")
        logger.info(f"Imported {len(data)} records from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Error importing data from CSV: {str(e)}")
        raise


def calculate_checksum(data: Dict) -> str:
    """
    Calculate a secure checksum for data verification.
    
    Args:
        data: Data to checksum
        
    Returns:
        str: Hexadecimal checksum
    """
    try:
        # Convert data to stable string representation
        data_str = json.dumps(data, sort_keys=True)
        
        # Calculate SHA-256 hash
        hash_obj = hashlib.sha256(data_str.encode())
        return hash_obj.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating checksum: {str(e)}")
        raise


# Main integration function
def initialize_integration(config_file: Optional[str] = None) -> GenesisIntegrationManager:
    """
    Initialize the VOI Jeans integration with Genesis Stack.
    
    Args:
        config_file: Optional path to configuration file
        
    Returns:
        GenesisIntegrationManager: Configured integration manager
    """
    try:
        # Initialize SynnergyzeOS connector
        synnergyze_connector = SynnergyzeConnector(config_file)
        
        # Authenticate
        if not synnergyze_connector.authenticate():
            raise ConnectionError("Failed to authenticate with SynnergyzeOS")
        
        # Get Genesis configuration from environment or config file
        genesis_api_url = os.environ.get("GENESIS_API_URL", "https://api.genesis-ecosystem.org")
        genesis_api_key = os.environ.get("GENESIS_API_KEY", "")
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                genesis_api_url = config.get("genesis_api_url", genesis_api_url)
                genesis_api_key = config.get("genesis_api_key", genesis_api_key)
        
        # Initialize integration manager
        integration_manager = GenesisIntegrationManager(
            synnergyze_connector,
            genesis_api_url,
            genesis_api_key
        )
        
        logger.info("Successfully initialized VOI Jeans integration with Genesis Stack")
        return integration_manager
    except Exception as e:
        logger.error(f"Error initializing integration: {str(e)}")
        raise


if __name__ == "__main__":
    # Example usage
    try:
        # Initialize integration
        integration = initialize_integration()
        
        # Sync recent transactions
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Get recent transactions
        sales_manager = integration.sales_manager
        recent_transactions = sales_manager.get_sales_transactions(
            start_date=yesterday,
            end_date=today
        )
        
        # Sync each transaction to Genesis
        if "transactions" in recent_transactions:
            for transaction in recent_transactions["transactions"]:
                integration.sync_transaction_to_genesis(transaction["id"])
        
        # Sync inventory
        integration.sync_inventory_to_genesis(full_sync=True)
        
        logger.info("Integration test completed successfully")
    except Exception as e:
        logger.error(f"Integration test failed: {str(e)}")