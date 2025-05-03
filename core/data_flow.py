"""
Data Flow Visualization Module for Empire OS

This module manages the visualization of data flow from factory to consumer,
providing insights and analytics at each stage of the supply chain.
"""

import os
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from enum import Enum

class DataFlowStage(Enum):
    """Data flow stages in the supply chain"""
    FACTORY = "factory"
    DISTRIBUTION = "distribution"
    STORE = "store"
    CONSUMER = "consumer"

class DataFlowManager:
    """Manages the flow of data across all supply chain stages"""
    
    def __init__(self, data_dir='data/flow_data'):
        """Initialize the data flow manager"""
        self.data_dir = data_dir
        self._ensure_data_dir()
        self.flow_segments = self._init_flow_segments()
        
    def _ensure_data_dir(self):
        """Ensure the data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _init_flow_segments(self):
        """Initialize the flow segments for data visualization"""
        return {
            DataFlowStage.FACTORY.value: {
                "name": "Factory Production",
                "description": "Raw materials to finished products",
                "metrics": [
                    "production_efficiency",
                    "quality_rating",
                    "resource_consumption",
                    "production_time",
                    "divine_alignment"
                ],
                "key_insights": [
                    "Production efficiency patterns",
                    "Quality control effectiveness",
                    "Resource utilization optimization",
                    "Divine alignment of manufacturing processes"
                ]
            },
            DataFlowStage.DISTRIBUTION.value: {
                "name": "Distribution Network",
                "description": "Warehouse operations and logistics",
                "metrics": [
                    "logistics_efficiency",
                    "inventory_turnover",
                    "delivery_time",
                    "warehouse_utilization",
                    "divine_alignment"
                ],
                "key_insights": [
                    "Inventory optimization opportunities",
                    "Logistics efficiency analysis",
                    "Warehouse space utilization patterns",
                    "Divine alignment of distribution processes"
                ]
            },
            DataFlowStage.STORE.value: {
                "name": "Retail Operations",
                "description": "Store-level inventory and sales",
                "metrics": [
                    "sales_velocity",
                    "shelf_efficiency",
                    "store_inventory_health",
                    "markdown_rate",
                    "divine_alignment"
                ],
                "key_insights": [
                    "Sales velocity by store and product",
                    "Inventory health indicators",
                    "Markdown efficiency analysis",
                    "Divine alignment of retail operations"
                ]
            },
            DataFlowStage.CONSUMER.value: {
                "name": "Consumer Experience",
                "description": "Post-purchase customer journey",
                "metrics": [
                    "customer_satisfaction",
                    "return_rate",
                    "repeat_purchase_rate",
                    "demographic_alignment",
                    "divine_alignment"
                ],
                "key_insights": [
                    "Customer satisfaction trends",
                    "Return reason analysis",
                    "Customer lifetime value indicators",
                    "Divine alignment of customer experience"
                ]
            }
        }
    
    def get_flow_stage(self, stage):
        """Get information about a specific flow stage"""
        if stage not in self.flow_segments:
            return None
        return self.flow_segments[stage]
    
    def get_all_flow_stages(self):
        """Get information about all flow stages"""
        return self.flow_segments
    
    def get_flow_metrics(self, stage=None):
        """Get metrics for a specific stage or all stages"""
        if stage and stage in self.flow_segments:
            return self.flow_segments[stage].get("metrics", [])
        
        all_metrics = []
        for stage_info in self.flow_segments.values():
            all_metrics.extend(stage_info.get("metrics", []))
        return list(set(all_metrics))  # Deduplicate
    
    def generate_sample_flow_data(self, client_id, from_date=None, to_date=None, 
                                stage=None, access_level="limited"):
        """
        Generate sample flow data for visualization
        
        Parameters:
        -----------
        client_id : str
            The client identifier
        from_date : str, optional
            Start date for data (ISO format)
        to_date : str, optional
            End date for data (ISO format)
        stage : str, optional
            Specific stage to generate data for
        access_level : str, optional
            Level of detail/access ('limited', 'partial', 'full')
            
        Returns:
        --------
        dict
            Dictionary containing the generated flow data
        """
        # Default date range (last 30 days)
        if not to_date:
            to_date = datetime.now()
        else:
            if isinstance(to_date, str):
                to_date = datetime.fromisoformat(to_date)
                
        if not from_date:
            from_date = to_date - timedelta(days=30)
        else:
            if isinstance(from_date, str):
                from_date = datetime.fromisoformat(from_date)
        
        # Generate date range
        date_range = pd.date_range(from_date, to_date, freq='D')
        
        # Determine stages to include
        stages_to_include = [stage] if stage else list(self.flow_segments.keys())
        
        # Determine data volume based on access level
        data_points = {
            "limited": len(date_range) // 3,  # 1/3 of days
            "partial": len(date_range) // 2,  # 1/2 of days
            "full": len(date_range)           # All days
        }.get(access_level.lower(), len(date_range) // 3)
        
        # Sample dates to include
        if data_points < len(date_range):
            sampled_dates = sorted(np.random.choice(date_range, data_points, replace=False))
        else:
            sampled_dates = date_range
            
        # Generate data for each stage
        flow_data = {
            "client_id": client_id,
            "date_range": {
                "from": from_date.isoformat(),
                "to": to_date.isoformat()
            },
            "access_level": access_level,
            "stages": {}
        }
        
        # Generate stage-specific data
        for stage_name in stages_to_include:
            if stage_name not in self.flow_segments:
                continue
                
            stage_data = []
            stage_info = self.flow_segments[stage_name]
            metrics = stage_info.get("metrics", [])
            
            for date in sampled_dates:
                data_point = {
                    "date": date.isoformat()
                }
                
                # Generate values for each metric
                for metric in metrics:
                    # Base value (0-100)
                    base = np.random.randint(60, 95)
                    # Daily fluctuation (-5 to +5)
                    fluctuation = np.random.randint(-5, 6)
                    # Trend component (gradual improvement over time)
                    trend = int((date - from_date).days / (to_date - from_date).days * 10)
                    
                    value = min(100, max(0, base + fluctuation + trend))
                    data_point[metric] = value
                
                stage_data.append(data_point)
            
            flow_data["stages"][stage_name] = {
                "name": stage_info["name"],
                "description": stage_info["description"],
                "data": stage_data
            }
            
            # Add insights only for full and partial access
            if access_level.lower() in ["full", "partial"]:
                insights = []
                for i, insight_text in enumerate(stage_info.get("key_insights", [])):
                    if i >= 2 and access_level.lower() != "full":
                        continue  # Limit insights for partial access
                    
                    value = np.random.randint(60, 95)
                    impact = np.random.randint(1, 5)
                    insights.append({
                        "text": insight_text,
                        "value": value,
                        "impact": impact
                    })
                
                flow_data["stages"][stage_name]["insights"] = insights
                
        # Save data to file
        file_path = os.path.join(
            self.data_dir, 
            f"{client_id}_{access_level}_{from_date.strftime('%Y%m%d')}_{to_date.strftime('%Y%m%d')}.json"
        )
        
        with open(file_path, 'w') as f:
            json.dump(flow_data, f, indent=2)
            
        return flow_data
    
    def get_flow_connections(self, access_level="limited"):
        """
        Get the connections between flow stages
        
        Parameters:
        -----------
        access_level : str, optional
            Level of detail/access ('limited', 'partial', 'full')
            
        Returns:
        --------
        list
            List of connections between stages
        """
        # Basic connections (available to all levels)
        connections = [
            {
                "from": DataFlowStage.FACTORY.value,
                "to": DataFlowStage.DISTRIBUTION.value,
                "name": "Product Transfer",
                "metrics": ["transfer_efficiency", "quality_retention"]
            },
            {
                "from": DataFlowStage.DISTRIBUTION.value,
                "to": DataFlowStage.STORE.value,
                "name": "Retail Delivery",
                "metrics": ["delivery_timeliness", "inventory_accuracy"]
            },
            {
                "from": DataFlowStage.STORE.value,
                "to": DataFlowStage.CONSUMER.value,
                "name": "Sales Process",
                "metrics": ["purchase_experience", "product_satisfaction"]
            }
        ]
        
        # Additional detailed connections for higher access levels
        if access_level.lower() in ["partial", "full"]:
            connections.extend([
                {
                    "from": DataFlowStage.FACTORY.value,
                    "to": DataFlowStage.STORE.value,
                    "name": "Direct-to-Store",
                    "metrics": ["special_order_efficiency", "production_flexibility"]
                },
                {
                    "from": DataFlowStage.CONSUMER.value,
                    "to": DataFlowStage.FACTORY.value,
                    "name": "Customer Feedback Loop",
                    "metrics": ["feedback_integration", "product_improvement"]
                }
            ])
            
        # Premium connections only available to full access
        if access_level.lower() == "full":
            connections.extend([
                {
                    "from": DataFlowStage.CONSUMER.value,
                    "to": DataFlowStage.DISTRIBUTION.value,
                    "name": "Returns Processing",
                    "metrics": ["return_efficiency", "reverse_logistics_cost"]
                },
                {
                    "from": DataFlowStage.DISTRIBUTION.value,
                    "to": DataFlowStage.FACTORY.value,
                    "name": "Inventory Replenishment Signal",
                    "metrics": ["forecast_accuracy", "production_planning"]
                }
            ])
            
        return connections
    
    def get_divine_insights(self, stage=None, access_level="limited"):
        """
        Get divine alignment insights for a stage or all stages
        
        Parameters:
        -----------
        stage : str, optional
            Specific stage to get insights for
        access_level : str, optional
            Level of detail/access ('limited', 'partial', 'full')
            
        Returns:
        --------
        dict
            Dictionary containing divine insights
        """
        # Determine stages to include
        stages_to_include = [stage] if stage else list(self.flow_segments.keys())
        
        insights = {}
        
        for stage_name in stages_to_include:
            if stage_name not in self.flow_segments:
                continue
                
            stage_info = self.flow_segments[stage_name]
            
            # Generate base divine alignment score (0-100)
            base_score = np.random.randint(60, 95)
            
            # Different levels of detail based on access level
            if access_level.lower() == "limited":
                # Just basic score
                insights[stage_name] = {
                    "name": stage_info["name"],
                    "divine_alignment_score": base_score,
                    "summary": f"Divine alignment is at {base_score}% for {stage_info['name']}."
                }
            elif access_level.lower() == "partial":
                # Score with dimensions
                dimensions = [
                    "Resource Flow Alignment",
                    "Value Creation Alignment",
                    "Decision Alignment",
                    "Information Flow Alignment"
                ]
                
                dimension_scores = {}
                for dim in dimensions:
                    # Score with some variation from base
                    variation = np.random.randint(-15, 16)
                    dim_score = min(100, max(0, base_score + variation))
                    dimension_scores[dim] = dim_score
                
                insights[stage_name] = {
                    "name": stage_info["name"],
                    "divine_alignment_score": base_score,
                    "dimensions": dimension_scores,
                    "summary": f"Divine alignment is at {base_score}% for {stage_info['name']}.",
                    "recommendation": "Focus on improving alignment in the lowest scoring dimensions."
                }
            else:  # full access
                # Comprehensive divine alignment analysis
                dimensions = [
                    "Resource Flow Alignment",
                    "Value Creation Alignment",
                    "Decision Alignment",
                    "Information Flow Alignment"
                ]
                
                dimension_data = {}
                recommendations = []
                
                for dim in dimensions:
                    # Score with some variation from base
                    variation = np.random.randint(-15, 16)
                    dim_score = min(100, max(0, base_score + variation))
                    
                    # Sub-components of each dimension
                    sub_components = {}
                    for i in range(3):  # 3 sub-components per dimension
                        sub_var = np.random.randint(-10, 11)
                        sub_score = min(100, max(0, dim_score + sub_var))
                        sub_components[f"Component {i+1}"] = sub_score
                    
                    dimension_data[dim] = {
                        "score": dim_score,
                        "components": sub_components
                    }
                    
                    # Generate recommendation if score is below threshold
                    if dim_score < 80:
                        recommendations.append({
                            "dimension": dim,
                            "score": dim_score,
                            "text": f"Improve {dim} through targeted interventions in key processes.",
                            "potential_improvement": np.random.randint(5, 26)
                        })
                
                insights[stage_name] = {
                    "name": stage_info["name"],
                    "divine_alignment_score": base_score,
                    "dimensions": dimension_data,
                    "recommendations": recommendations,
                    "summary": f"Comprehensive divine alignment analysis for {stage_info['name']}.",
                    "optimization_potential": np.random.randint(10, 31)
                }
        
        return insights