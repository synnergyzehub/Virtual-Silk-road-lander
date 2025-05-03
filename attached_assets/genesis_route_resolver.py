
# genesis_route_resolver.py

import streamlit as st

class GenesisRouteResolver:
    def __init__(self):
        self.state = st.session_state
        self.license_id = self.state.get("license_id", None)
        self.user_type = self.state.get("user_type", None)
        self.completed_onboarding = self.state.get("completed_onboarding", False)
        self.realm = self.state.get("realm", "general")

    def route(self):
        if not self.license_id:
            return "license_verification"

        if not self.completed_onboarding:
            return "onboarding"

        if self.realm == "supply_chain":
            return "inventory_dashboard"

        if self.realm == "commerce":
            return "synergy_hub"

        return "default_home"

    def verify_access(self, page):
        access_rules = {
            "synergy_hub": ["retailer", "manager", "admin"],
            "inventory_dashboard": ["supply_manager", "admin"],
            "onboarding": ["guest", "retailer", "partner"],
            "license_verification": ["guest", "partner", "admin"]
        }
        allowed_roles = access_rules.get(page, [])
        return self.user_type in allowed_roles

    def log_transition(self, destination):
        print(f"[GenesisRouteResolver] Transitioning to: {destination}")
        # Future: Add logging to DB or external tracking system
