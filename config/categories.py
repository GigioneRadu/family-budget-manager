"""
Budget Categories Configuration
All categories and subcategories for the Family Budget Manager
"""

BUDGET_CATEGORIES = {
    "Children": [
        "Childcare",
        "Medical & Consultations",
        "School Supplies & Toys",
        "School Tuition",
        "Children's Food",
        "Children's Entertainment"
    ],
    "Entertainment": [
        "Concerts",
        "Theatre & Opera",
        "Cinema",
        "Music (CDs, Downloads, etc.)",
        "Sports Events",
        "Video/DVD (Purchase)",
        "Video/DVD (Rental)",
        "Books"
    ],
    "Food": [
        "Dining Out & Catering",
        "Groceries",
        "Fruits & Vegetables",
        "Meat & Deli",
        "Fish & Seafood"
    ],
    "Gifts and Charity": [
        "Religious Donations",
        "Gifts",
        "Gift 1",
        "Gift 2"
    ],
    "Housing": [
        "Cable/Satellite",
        "Electricity",
        "Gas",
        "House Cleaning",
        "Home Maintenance & Repairs",
        "Utilities",
        "Natural Gas/Oil",
        "Internet Service",
        "Mobile Phone",
        "Landline Phone",
        "Other Housing Expenses",
        "Waste Removal & Recycling",
        "Water & Bottled Water"
    ],
    "Insurance": [
        "Health Insurance",
        "Home Insurance",
        "Life Insurance"
    ],
    "Loans": [
        "Personal Loan",
        "Overdraft",
        "Credit Card",
        "Personal Debt",
        "Student Loan"
    ],
    "Personal Care": [
        "Clothing",
        "Hygiene Products",
        "Hair Salon & Manicure",
        "Fitness & Beauty Salon",
        "Medical & Consultations"
    ],
    "Pets": [
        "Pet Food",
        "Grooming",
        "Veterinary & Medicine",
        "Pet Toys"
    ],
    "Savings or Investments": [
        "Investments",
        "Retirement Account"
    ],
    "Taxes": [
        "Federal Taxes",
        "Local Taxes",
        "State Taxes"
    ],
    "Transportation": [
        "Public Transport & Taxi",
        "Fuel/Gasoline",
        "Car Insurance",
        "License & Registration",
        "Car Maintenance",
        "Parking",
        "Vehicle Taxes"
    ]
}

# Category colors for visualizations
CATEGORY_COLORS = {
    "Children": "#FF6B6B",
    "Entertainment": "#4ECDC4",
    "Food": "#45B7D1",
    "Gifts and Charity": "#FFA07A",
    "Housing": "#98D8C8",
    "Insurance": "#6C5CE7",
    "Loans": "#FDCB6E",
    "Personal Care": "#FF7675",
    "Pets": "#74B9FF",
    "Savings or Investments": "#55EFC4",
    "Taxes": "#A29BFE",
    "Transportation": "#FD79A8"
}

# Category icons (emoji)
CATEGORY_ICONS = {
    "Children": "👶",
    "Entertainment": "🎭",
    "Food": "🍕",
    "Gifts and Charity": "🎁",
    "Housing": "🏠",
    "Insurance": "🛡️",
    "Loans": "💳",
    "Personal Care": "💄",
    "Pets": "🐾",
    "Savings or Investments": "💰",
    "Taxes": "📊",
    "Transportation": "🚗"
}

def get_all_categories():
    """Returns list of all main categories"""
    return list(BUDGET_CATEGORIES.keys())

def get_subcategories(category):
    """Returns subcategories for a given category"""
    return BUDGET_CATEGORIES.get(category, [])

# Income categories (simple list, no subcategories)
INCOME_CATEGORIES = [
    "💼 Salary",
    "🎁 Bonus",
    "🏢 Freelance/Business",
    "🏠 Rental Income",
    "📈 Investments",
    "🎉 Gifts & Inheritance",
    "💰 Other Income"
]

def get_all_subcategories_flat():
    """Returns flat list of all subcategories with their parent category"""
    result = []
    for category, subcategories in BUDGET_CATEGORIES.items():
        for subcategory in subcategories:
            result.append({
                "category": category,
                "subcategory": subcategory,
                "icon": CATEGORY_ICONS.get(category, "📌"),
                "color": CATEGORY_COLORS.get(category, "#95A5A6")
            })
    return result

def get_income_categories():
    """Returns list of income categories"""
    return INCOME_CATEGORIES

