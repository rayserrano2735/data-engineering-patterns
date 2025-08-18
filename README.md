# Data Engineering Patterns

> A comprehensive collection of production-ready patterns, solutions, and best practices for data engineering challenges.

## 🎯 Purpose

This repository serves as:
- **Personal Reference**: Battle-tested solutions for common data engineering problems
- **Interview Resource**: Demonstrable code examples showing deep technical knowledge
- **Learning Library**: Well-documented patterns with explanations of the "why" behind the code
- **Teaching Material**: Foundation for courses and mentoring

## Code Philosophy

This repository prioritizes **maintainability over cleverness**. 

The code is intentionally written to be:
- Clear and readable by developers at any level
- Debuggable at 3 AM during production issues  
- Maintainable by junior developers
- Self-documenting through clarity

This is a conscious architectural choice, following the same principles as dbt: 
"Code is read 100x more than it's written."

We optimize for the on-call engineer, not the compiler.

## 📚 Pattern Categories

### [SQL Patterns](./sql-patterns/)
Production-ready SQL solutions for complex data challenges.

- **[Table Comparison](./sql-patterns/table-comparison/)** - Compare tables with different schemas, identify differences ⭐
- **Window Functions** - Advanced analytics with ranking, rolling calculations *(coming soon)*
- **CTEs & Subqueries** - Complex query patterns and optimization *(coming soon)*
- **Data Quality Checks** - Validation and anomaly detection patterns *(coming soon)*

### [DBT Patterns](./dbt-patterns/)
Best practices and reusable components for dbt projects.

- **Macros** - Reusable SQL generators and helpers *(coming soon)*
- **Models** - Staging, intermediate, and mart patterns *(coming soon)*
- **Tests** - Custom test implementations *(coming soon)*

### [Spark Patterns](./spark-patterns/)
Optimized PySpark solutions for large-scale data processing.
*(coming soon)*

### [Airflow Patterns](./airflow-patterns/)
DAG patterns and custom operators for reliable orchestration.
*(coming soon)*

### More categories being added regularly...

## 🚀 Quick Start

### Using a Pattern

1. **Browse** the pattern categories above
2. **Navigate** to the specific pattern you need
3. **Read** the pattern's README for detailed usage
4. **Copy** the code and adapt to your needs

### Example: Table Comparison Pattern

```bash
# Navigate to the pattern
cd sql-patterns/table-comparison/

# For tables with same column names
# Use: compare_tables_dynamic.sql

# For tables with different column names
python column_mapper.py
# Follow interactive prompts to map columns
# Get generated SQL with proper mappings
```

## 🛠️ Repository Tools

This repo includes tools to maintain and extend the pattern library:

### Structure Generator
Create new pattern structures consistently:
```bash
# Interactive menu
python tools/create_structure.py -i

# From YAML definition
python tools/create_structure.py structures/new_pattern.yaml
```

### Tree Generator
Document your folder structures:
```bash
# Generate tree view for README files
python tools/generate_tree.py -i
```

### GitKeep Manager
Maintain empty folders in Git:
```bash
# Add .gitkeep to all empty directories
tools/add-gitkeep-to-empty-folders.bat
```

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed tool documentation.

## 📖 Documentation Structure

Each pattern follows this documentation standard:

```
pattern-name/
├── README.md           # Comprehensive guide with:
│                       # - Problem description
│                       # - Solution approach
│                       # - Usage examples
│                       # - Code explanation
│                       # - Best practices
├── main_solution.*     # Primary implementation
├── examples/           # Real-world examples
├── tests/              # Test cases
└── database-specific/  # Vendor-specific variations
```

## 🏗️ Repository Structure

```
data-engineering-patterns/
├── README.md                    # This file
├── CONTRIBUTING.md              # How to add patterns
├── SETUP_GUIDE.md              # Tools setup & usage
├── sql-patterns/               # SQL-based solutions
├── dbt-patterns/               # dbt-specific patterns
├── spark-patterns/             # PySpark patterns
├── airflow-patterns/           # Orchestration patterns
├── python-patterns/            # Python data processing
├── cloud-patterns/             # Cloud-specific (AWS/GCP/Azure)
├── docker-patterns/            # Containerization
├── data-modeling-patterns/     # Modeling approaches
└── tools/                      # Repository utilities
```

## 💡 Using This in Interviews

### The Power Move
When asked a technical question, instead of whiteboarding from memory:

> "I've actually implemented this pattern before. Let me show you my approach..."
> 
> *[Open this repo and navigate to the relevant pattern]*
> 
> "Here's production-ready code that handles edge cases like NULL values and different schemas. Let me walk you through the logic..."

### Key Talking Points
- **Problem-Solution Fit**: Explain why this pattern exists
- **Edge Cases**: Show how you handle NULLs, data types, performance
- **Scalability**: Discuss how it works with large datasets
- **Maintainability**: Point out the documentation and tests
- **Real Experience**: Share where you've used this in production

## 🤝 Contributing

Want to add a new pattern? See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Pattern documentation standards
- Code quality guidelines
- Testing requirements
- How to use the structure generator

## 📈 Growth Plan

### Current Focus
- [x] Table comparison pattern with column mapping
- [x] Repository structure and tooling
- [ ] Window function patterns
- [ ] Data quality check patterns

### Future Additions
- [ ] Spark optimization patterns
- [ ] Airflow DAG patterns
- [ ] Real-time streaming patterns
- [ ] Cloud cost optimization patterns
- [ ] Udemy course development

## 🎓 Learning Path

### For Beginners
1. Start with [SQL Patterns](./sql-patterns/) - fundamental skills
2. Move to [Python Patterns](./python-patterns/) - data processing
3. Explore [DBT Patterns](./dbt-patterns/) - modern analytics engineering

### For Experienced Engineers
1. Dive into optimization patterns
2. Explore cloud-specific solutions
3. Contribute your own patterns!

## 📝 License

This repository is for educational purposes. Feel free to use these patterns in your projects.

## 🌟 Remember

> "The best code is not just working code, but code that teaches, scales, and stands the test of production."

Every pattern here has been battle-tested and refined through real-world use. This isn't just a code collection - it's crystallized experience.

---

*Building great data systems, one pattern at a time.* 🚀