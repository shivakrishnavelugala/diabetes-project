"""
Recommendation building utilities.
"""
from typing import Dict, Any


FEATURES = ["Glucose", "BloodPressure", "BMI", "Age", "Insulin"]


def get_risk_category(score: float) -> str:
    """Convert risk score to risk category."""
    if score <= 39:
        return "LOW RISK"
    if score <= 69:
        return "MODERATE RISK"
    return "HIGH RISK"


def _build_diet_recommendations(risk_level: str) -> list:
    """Build diet recommendations based on risk level."""
    if risk_level == "LOW RISK":
        return [
            {"name": "Leafy Greens", "emoji": "🥬", "description": "Spinach, kale, and other greens are rich in fiber and nutrients.", "why": "Excellent source of vitamins and minerals for maintaining good health."},
            {"name": "Berries", "emoji": "🫐", "description": "Blueberries, strawberries, and raspberries are nutrient-rich.", "why": "Low glycemic index and packed with antioxidants."},
            {"name": "Whole Grains", "emoji": "🌾", "description": "Oats, brown rice, and quinoa provide sustained energy.", "why": "Supports stable energy levels and good digestion."},
            {"name": "Lean Proteins", "emoji": "🐔", "description": "Chicken, fish, and legumes are excellent protein sources.", "why": "Helps maintain muscle and keeps you feeling full longer."},
            {"name": "Healthy Fats", "emoji": "🥑", "description": "Avocados, nuts, and olive oil support heart health.", "why": "Essential for nutrient absorption and sustained energy."},
        ]
    elif risk_level == "MODERATE RISK":
        return [
            {"name": "Leafy Greens", "emoji": "🥬", "description": "Spinach, kale, arugula - rich in vitamins and minerals.", "why": "Critical for blood sugar management and overall wellness."},
            {"name": "Fiber-Rich Vegetables", "emoji": "🥦", "description": "Broccoli, cauliflower, Brussels sprouts help regulate glucose.", "why": "Slows sugar absorption and improves blood sugar control."},
            {"name": "Legumes & Beans", "emoji": "🫘", "description": "Lentils, chickpeas, and black beans are high in fiber.", "why": "Excellent protein and fiber for steady energy and fullness."},
            {"name": "Fatty Fish", "emoji": "🐟", "description": "Salmon, mackerel, and sardines provide omega-3s.", "why": "Supports cardiovascular health and reduces inflammation."},
            {"name": "Nuts & Seeds", "emoji": "🌰", "description": "Almonds, walnuts, flaxseeds in appropriate portions.", "why": "Healthy fats and fiber that support sustained energy."},
        ]
    else:  # HIGH RISK
        return [
            {"name": "Non-Starchy Vegetables", "emoji": "🥬", "description": "Leafy greens, broccoli, peppers - minimal carbohydrates.", "why": "Essential for blood sugar management with no glycemic spike."},
            {"name": "High-Fiber Vegetables", "emoji": "🥦", "description": "Cauliflower, zucchini, asparagus with excellent fiber.", "why": "Promotes fullness and stable blood sugar levels."},
            {"name": "Legumes (Measured)", "emoji": "🫘", "description": "Lentils and beans in controlled portions.", "why": "Protein and fiber while being mindful of carbohydrate intake."},
            {"name": "Lean Proteins", "emoji": "🐟", "description": "Fish, poultry, tofu as primary protein sources.", "why": "Supports metabolism and muscle maintenance without excess calories."},
            {"name": "Healthy Fats (Measured)", "emoji": "🥑", "description": "Olive oil, nuts in controlled portions for satiety.", "why": "Promotes fullness and supports nutrient absorption."},
        ]


def _build_exercise_recommendations(risk_level: str) -> list:
    """Build exercise recommendations based on risk level."""
    if risk_level == "LOW RISK":
        return [
            {"title": "Aerobic Activity", "detail": "30-45 minutes of moderate intensity (brisk walking, cycling) 5 days per week."},
            {"title": "Strength Training", "detail": "2-3 days per week targeting major muscle groups."},
            {"title": "Flexibility", "detail": "Yoga or stretching 2-3 times per week to improve range of motion."},
            {"title": "Daily Movement", "detail": "Stay active throughout the day with regular movement breaks."},
        ]
    elif risk_level == "MODERATE RISK":
        return [
            {"title": "Structured Aerobic Activity", "detail": "30-40 minutes of moderate-to-brisk activity 4-5 days per week (walking, swimming, cycling)."},
            {"title": "Regular Strength Training", "detail": "2-3 days per week with progressive resistance as tolerated."},
            {"title": "Activity Breaks", "detail": "5-10 minute movement breaks every hour to prevent prolonged sitting."},
            {"title": "Flexible Activity", "detail": "Low-impact options like water aerobics or tai chi for joint protection."},
        ]
    else:  # HIGH RISK
        return [
            {"title": "Gradual Activity Progression", "detail": "Start with 10-15 minute walks daily, gradually increasing duration. Consult healthcare provider first."},
            {"title": "Gentle Strength Training", "detail": "Light resistance exercises 2-3 times per week under professional guidance if possible."},
            {"title": "Frequent Movement Breaks", "detail": "Move for 1-2 minutes every 30 minutes to improve circulation and metabolism."},
            {"title": "Supervised Activity", "detail": "Consider working with a fitness professional experienced with health management."},
        ]


def _build_lifestyle_recommendations(risk_level: str) -> list:
    """Build lifestyle recommendations based on risk level."""
    if risk_level == "LOW RISK":
        return [
            "Maintain consistent sleep schedule of 7-9 hours per night.",
            "Manage stress through meditation, hobbies, or social activities.",
            "Stay hydrated with plenty of water throughout the day.",
            "Maintain regular meal timing to support steady metabolism.",
            "Continue annual health check-ups to monitor your wellness.",
        ]
    elif risk_level == "MODERATE RISK":
        return [
            "Prioritize 7-9 hours of quality sleep each night for metabolic support.",
            "Implement stress management techniques daily (meditation, walking, deep breathing).",
            "Drink water consistently - aim for 8-10 glasses per day.",
            "Eat at regular times each day to maintain stable blood sugar.",
            "Schedule regular health check-ups (at least twice yearly).",
            "Track key health metrics like weight, blood pressure, and activity levels.",
        ]
    else:  # HIGH RISK
        return [
            "Prioritize 7-9 hours of quality sleep as it significantly affects blood sugar regulation.",
            "Practice daily stress reduction (even 10 minutes helps regulate glucose).",
            "Maintain consistent hydration - drink water regularly throughout the day.",
            "Eat at fixed times each day to stabilize blood sugar levels.",
            "Schedule regular healthcare visits (every 3-6 months recommended).",
            "Monitor and log key health metrics: weight, blood pressure, glucose (if available).",
            "Consult with healthcare professionals to develop a personalized management plan.",
        ]


def _build_insights(risk_level: str, glucose: float, blood_pressure: float, bmi: float, age: int, insulin: float) -> Dict[str, str]:
    """Build personalized health insights based on risk level and user data."""
    insights = {}
    
    # Analyze key risk factors
    high_glucose = glucose >= 140
    high_bp = blood_pressure >= 140
    high_bmi = bmi >= 30
    elevated_insulin = insulin >= 150
    
    if risk_level == "LOW RISK":
        insights["title"] = "Great News: Low Risk Profile"
        insights["summary"] = "Your current health assessment shows a low diabetes risk. You're doing well with your health metrics."
        insights["positive"] = "Your glucose, blood pressure, BMI, and insulin levels all indicate good metabolic control."
        insights["maintenance"] = "Continue with healthy lifestyle habits: maintain regular physical activity, balanced nutrition, and adequate sleep."
        insights["habits"] = "Keep up your current healthy practices—consistency is key to maintaining this positive health status."
        insights["next_steps"] = "Annual check-ups are sufficient. Stay mindful of gradual changes and maintain your current healthy routine."
    
    elif risk_level == "MODERATE RISK":
        insights["title"] = "Moderate Risk: Action Recommended"
        insights["summary"] = "Your assessment indicates moderate diabetes risk. This is a good time to make targeted lifestyle adjustments."
        
        # Identify specific risk factors
        risk_factors = []
        if high_glucose:
            risk_factors.append("elevated glucose levels")
        if high_bp:
            risk_factors.append("higher blood pressure")
        if high_bmi:
            risk_factors.append("increased BMI")
        if elevated_insulin:
            risk_factors.append("elevated insulin levels")
        
        if risk_factors:
            factors_text = ", ".join(risk_factors)
            insights["risk_factors"] = f"Key areas of concern: {factors_text}."
        else:
            insights["risk_factors"] = "Multiple factors contributed to your moderate risk assessment."
        
        insights["action"] = "Focus on increasing physical activity, improving dietary choices, and monitoring your health regularly."
        insights["targets"] = "Work toward: balanced meals, 150+ minutes of activity weekly, and maintaining a stable weight."
        insights["monitoring"] = "Check-ups every 6 months and consider tracking your health metrics at home."
    
    else:  # HIGH RISK
        insights["title"] = "High Risk: Professional Guidance Strongly Recommended"
        insights["summary"] = "Your assessment indicates higher diabetes risk. Professional medical support is important."
        
        # Identify specific risk factors
        risk_factors = []
        if high_glucose:
            risk_factors.append("significantly elevated glucose")
        if high_bp:
            risk_factors.append("elevated blood pressure")
        if high_bmi:
            risk_factors.append("high BMI")
        if elevated_insulin:
            risk_factors.append("elevated insulin")
        
        if risk_factors:
            factors_text = ", ".join(risk_factors)
            insights["risk_factors"] = f"Contributing factors: {factors_text}. These require attention."
        else:
            insights["risk_factors"] = "Multiple health indicators suggest increased risk that needs professional review."
        
        insights["urgent"] = "Please consult with a healthcare professional—they can provide personalized diagnosis and treatment options."
        insights["immediate_actions"] = "Start: daily physical activity (even short walks), reduce processed foods, monitor blood pressure and weight regularly."
        insights["professional_support"] = "Working with a doctor, dietitian, or diabetes educator can significantly improve outcomes."
    
    return insights


def build_recommendations(glucose: float, blood_pressure: float, bmi: float, age: int, insulin: float, risk_score: float, risk_category: str) -> Dict[str, Any]:
    """
    Build comprehensive, risk-level-specific recommendations and personalized insights.
    
    Args:
        glucose: Blood glucose level (mg/dL)
        blood_pressure: Blood pressure (mmHg)
        bmi: Body Mass Index (kg/m²)
        age: Age in years
        insulin: Insulin level (µU/mL)
        risk_score: Risk score (0-100)
        risk_category: Risk category (LOW RISK, MODERATE RISK, HIGH RISK)
    
    Returns:
        Dictionary with diet, exercise, lifestyle recommendations and personalized insights
    """
    risk_percentage = float(risk_score)
    
    # Build risk-level-specific recommendations
    diet_more = _build_diet_recommendations(risk_category)
    exercise = _build_exercise_recommendations(risk_category)
    lifestyle = _build_lifestyle_recommendations(risk_category)
    
    # Build personalized insights
    insights = _build_insights(risk_category, glucose, blood_pressure, bmi, age, insulin)
    
    return {
        "diet_more": diet_more,
        "exercise": exercise,
        "lifestyle": lifestyle,
        "insights": insights,
        "risk_category": risk_category,
        "risk_score": round(risk_percentage, 2),
    }
