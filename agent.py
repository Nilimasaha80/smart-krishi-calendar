import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import Tool

# Crop calendar data for Etawah district, soil-wise and crop-wise
crop_data = {
    "wheat": {
        "Sandy": {
            "Etawah": {
                "calendar": [
                    "Shallow ploughing and leveling",
                    "Apply FYM and phosphorus",
                    "Sowing in lines (Nov 1–15)",
                    "First irrigation at CRI stage (~21 DAS)",
                    "Weed management (30 DAS)",
                    "Top dressing with urea",
                    "Rust and aphid monitoring",
                    "Harvest in April (25% moisture)"
                ],
                "weather_conditions": "Cool dry winters, 15–25°C optimal"
            }
        },
        "Loamy": {
            "Etawah": {
                "calendar": [
                    "Ploughing + 2 harrowings",
                    "FYM + phosphorus (DAP)",
                    "Line sowing (Nov 10–25)",
                    "Irrigation (CRI, tillering, booting)",
                    "2 weedings",
                    "Zinc + urea mix",
                    "Rust-resistant variety preferred",
                    "Harvest late March–early April"
                ],
                "weather_conditions": "Fertile loamy soil ideal for wheat"
            }
        }
    },
    "rice": {
        "Sandy": {
            "Etawah": {
                "calendar": [
                    "Land puddling & transplanting",
                    "High compost dose & FYM",
                    "Paddy transplanting (June–July)",
                    "Regular irrigation every 7 days",
                    "Weeding & zinc application",
                    "Pest (BPH) & blast watch",
                    "Top dressing with urea",
                    "Harvest in October"
                ],
                "weather_conditions": "Monsoon cropping, needs 1000mm+ rain"
            }
        },
        "Clayey": {
            "Etawah": {
                "calenda
