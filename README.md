# 🛒 Product Promotion Finder

A small Python project created as part of my journey from QA into programming, data processing and automation.

The application consumes data from a public REST API, allows the user to choose filters through the terminal, applies business rules, sorts the results, generates promotion-style summaries and exports the final dataset to CSV.

---

## ✨ Features

* 🌐 Fetch products from a REST API
* 📂 Display a category menu for the user
* ✅ Validate category selection with a loop
* 🔍 Filter by category
* 💰 Filter by maximum price
* ⭐ Filter by minimum rating
* 🔥 Filter by minimum discount percentage
* 📊 Sort products by price
* 🛒 Generate promotion cards in the terminal
* 📄 Export filtered results to CSV

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/product-promotion-finder.git
```

Navigate to the project folder:

```bash
cd product-promotion-finder
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```bash
python product_finder.py
```

Follow the prompts to:

* 📂 Select a product category
* 💰 Define the maximum price
* ⭐ Define the minimum rating
* 🔥 Define the minimum discount

The application will:

* 🛒 Display promotion cards in the terminal
* 📄 Export the filtered results to `output/product_promotions.csv`

---

## 🔄 Current Flow

Choose category from menu

⬇️

Define filters

⬇️

Fetch products from API

⬇️

Apply business rules

⬇️

Sort results

⬇️

Generate promotion cards

⬇️

Export CSV

---

## 🛠️ Technologies and Concepts

* 🐍 Python
* 🌐 Requests
* 📦 JSON Processing
* 📄 CSV Export
* 🧩 Functions
* ⚙️ Parameters
* 🔀 Conditional Logic
* 🔁 Loops
* 📊 Sorting
* ⌨️ User Input
* ✅ Basic Input Validation

---

## 💡 Why I Built This

I wanted to move beyond isolated programming exercises and work on a project that resembles a real-world workflow.

As a QA professional, I naturally think in terms of business rules, data flow, validation and user experience. This project allowed me to practice Python while applying the same mindset used in software testing:

**Input → Processing → Validation → Output**

The goal was not only to learn syntax, but to understand how data moves through an application and how business rules can be translated into code.

---

## 📸 Screenshots

### 🛒 Terminal Output

Add a screenshot of the promotion cards generated in the terminal.

```text
🛒 Product: Red Nail Polish
💰 Price: $8.99
⭐ Rating: 4.36
🏷️ Category: beauty
🔥 Discount: 12.16%
----------------------------------------
```

Example:

```markdown
![Terminal Output](screenshots/terminal_output.png)
```

### 📄 CSV Output

Add a screenshot of the generated CSV file.

Example:

```markdown
![CSV Output](screenshots/csv_output.png)
```

---

## 🔮 Future Improvements

* 🤖 Automate recurring product checks
* 📝 Save historical search results
* 📈 Detect new or improved offers
* 📲 Send alerts through Telegram or email
* ✨ Generate promotional texts automatically
* 🧠 Explore AI agents to summarize, rank and prepare offers for publishing
* 🤝 Integrate with official affiliate programs or approved APIs
