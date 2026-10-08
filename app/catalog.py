"""English adaptation of the original nine categories and 23 services."""

DEPARTMENTS = [
    ("housekeeping", "Housekeeping", 60),
    ("food", "Food & Beverage", 60),
    ("events", "Conference & Events", 240),
    ("engineering", "Engineering", 120),
    ("security", "Security", 30),
    ("concierge", "Concierge", 120),
]
# SLA values and category-to-department routing are new demo assumptions.
CATEGORIES = [
    ("cleaning", "Room cleaning & care", "housekeeping", ["Urgent cleaning", "Scheduled cleaning"]),
    (
        "amenities",
        "Amenities & supplies",
        "housekeeping",
        ["Extra towels", "Extra pillows or blankets", "Tea / coffee kit"],
    ),
    ("room_service", "Room service", "food", ["In-room dining"]),
    ("restaurant", "Restaurant services", "food", ["Restaurant table booking"]),
    ("venue", "Venue booking", "events", ["Banquet hall booking", "Conference room booking"]),
    ("event", "Event organisation", "events", ["Wedding", "Corporate event", "Team building", "Birthday"]),
    (
        "maintenance",
        "Repair & maintenance",
        "engineering",
        ["Air conditioning / heating", "Electrical issue", "Plumbing"],
    ),
    ("safety", "Safety & security", "security", ["Lost property", "Room access", "Emergency assistance"]),
    (
        "personal",
        "Personal requests",
        "concierge",
        ["Event tickets", "Transport", "Restaurant recommendations", "Other"],
    ),
]
ROOMS = [f"R{floor}{room:02d}" for floor in range(1, 4) for room in range(1, 4)]
