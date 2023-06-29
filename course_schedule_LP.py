from pulp import LpProblem, LpVariable, lpSum, LpBinary, LpMinimize
from collections import defaultdict

# Define the curriculum information

courses = [
    {"name": "Java", "credits": 3, "difficulty": 2, "prerequisites": [], "category": "Programming"},
    {"name": "Operating Systems", "credits": 4, "difficulty": 3, "prerequisites": ["Java"], "category": "System"},
    {"name": "Data Structures", "credits": 3, "difficulty": 1, "prerequisites": [], "category": "Programming"},
    {"name": "Algorithms", "credits": 5, "difficulty": 4, "prerequisites": ["Data Structures"], "category": "Programming"},
    {"name": "Database Management", "credits": 2, "difficulty": 2, "prerequisites": [], "category": "System"},
    {"name": "Computer Networks", "credits": 4, "difficulty": 3, "prerequisites": ["Operating Systems"], "category": "System"},
    {"name": "Software Engineering", "credits": 3, "difficulty": 2, "prerequisites": ["Data Structures", "Algorithms"], "category": "Programming"},
    {"name": "Compilers", "credits": 4, "difficulty": 3, "prerequisites": ["Data Structures", "Algorithms"], "category": "Programming"},
    {"name": "Computer Architecture", "credits": 3, "difficulty": 1, "prerequisites": [], "category": "System"},
    {"name": "Artificial Intelligence", "credits": 5, "difficulty": 4, "prerequisites": ["Data Structures"], "category": "Programming"}
]

category_credits = {
    "Programming": 18,
    "System": 12
}


# Create the linear programming problem
problem = LpProblem("Course_Selection", LpMinimize)

# Create the decision variables
course_vars = LpVariable.dicts("Course", range(len(courses)), cat=LpBinary)

# Set the objective function
problem += lpSum(courses[i]["credits"] * course_vars[i] for i in range(len(courses)))

# Add the prerequisites constraints
for i, course in enumerate(courses):
    for prereq in course["prerequisites"]:
        j = next(j for j, c in enumerate(courses) if c["name"] == prereq)
        problem += course_vars[i] <= course_vars[j]

# Add the category credits constraints
for category, credits_required in category_credits.items():
    category_courses = [i for i, c in enumerate(courses) if c["category"] == category]
    problem += lpSum(courses[i]["credits"] * course_vars[i] for i in category_courses) >= credits_required

# Solve the problem
problem.solve()

# Calculate total credits
total_credits = sum(course["credits"] for i, course in enumerate(courses) if course_vars[i].value() == 1)
print("Total credits:", total_credits)

# Print the credits per category
print("\nCredits per category:")
category_credits_count = {category: 0 for category in category_credits}
for i, course in enumerate(courses):
    if course_vars[i].value() == 1:
        category_credits_count[course["category"]] += course["credits"]

for category, credits_count in category_credits_count.items():
    print(category + ": " + str(credits_count) + " credits")

# Collect selected courses by category
selected_courses_by_category = defaultdict(list)
for i, course in enumerate(courses):
    if course_vars[i].value() == 1:
        selected_courses_by_category[course["category"]].append(course)

# Print the selected courses by category
print("\nSelected courses by category:")
for category, courses in selected_courses_by_category.items():
    print(category + ":")
    for course in courses:
        print("- Name: " + course["name"])
        print("  Prerequisites: " + ', '.join(course["prerequisites"]))
        print("  Credits: " + str(course["credits"]))