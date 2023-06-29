# 选课：	

## 问题描述

这个程序旨在解决基于给定课程培养方案的课程选择问题。程序的目标是找到满足以下约束条件的最小化总学分的课程选择方案：

1. 先修课程约束：要选择一门课程，必须同时选择所有的先修课程。
2. 类别学分要求：对于每个类别c，所选课程的总学分必须大于等于该类别的最小学分要求。

## 规划及程序

首先，我们需要定义决策变量和约束条件。假设我们有N门课程可供选择，其中每门课程有唯一的课程ID。我们引入一个二进制决策变量$x_i$，表示是否选择第i门课程，其中i的取值范围是1到N。



现在，我们可以列出整数规划的数学模型：

​                                                       $$ min \sum_{i}(credit_{i} * x_{i})$$

其中，$credit_i$表示第i门课程的学分。

约束条件：

1. 先修课约束：对于每门课程i，如果它有先修课程j，则必须选择先修课程j才能选择课程i。这可以通过添加二进制约束条件来表示： $x_i \leq x_j, for~all~(i, j)~in~prerequisites$
2. 学分约束：对于每个类别c，所选课程的总学分必须大于等于该类别的最小学分要求。这可以通过添加线性约束条件来表示： $\sum_{~for~all~i~in~category~c}(credit_i * x_i), \geq category\_credits(c),~for~all~c$
3. 决策变量约束：决策变量$x_i$必须是二进制变量。 $x_i ∈ \{0, 1\},~for~all~i$



```py
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
```



> 样例输出：
>
> ```python
> Total credits: 31
> 
> Credits per category:
> Programming: 18 credits
> System: 13 credits
> 
> Selected courses by category:
> Programming:
> - Name: Java
>   Prerequisites:
>   Credits: 3
> - Name: Data Structures
>   Prerequisites:
>   Credits: 3
> - Name: Algorithms
>   Prerequisites: Data Structures
>   Credits: 5
> - Name: Software Engineering
>   Prerequisites: Data Structures, Algorithms
>   Credits: 3
> - Name: Compilers
>   Prerequisites: Data Structures, Algorithms
>   Credits: 4
> System:
> - Name: Operating Systems
>   Prerequisites: Java
>   Credits: 4
> - Name: Database Management
>   Prerequisites:
>   Credits: 2
> - Name: Computer Networks
>   Prerequisites: Operating Systems
>   Credits: 4
> - Name: Computer Architecture
>   Prerequisites:
>   Credits: 3
> ```
>
> 
>
> 