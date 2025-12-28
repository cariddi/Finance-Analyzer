from datetime import datetime

STATUS_ICON = {
    "EXCELLENT": "🟢 **EXCELLENT**",
    "GREAT": "🟡 **GREAT**",
    "PASS": "🔵 **PASS**",
    "True": "🔵 **PASS**",
    "False": "🔴 **BAD**",
    "BAD": "🔴 **BAD**",
    "N/A": "⚪ **N/A**",
}

def status_badge(status):
    return STATUS_ICON.get(str(status), str(status))

def export_to_markdown(results, filename=None):
    if not filename:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"analysis_{ts}.md"

    with open(filename, "w") as f:
        f.write("# 📊 Company Financial Analysis\n\n")

        for company in results:
            f.write(f"## 🏢 {company['ticker']}\n\n")

            for section, rules in company.items():
                if section == "ticker":
                    continue

                f.write(f"### {section.upper()}\n\n")

                f.write("| Rule | Description | Status | Values |\n")
                f.write("|-----|------------|--------|--------|\n")

                for rule in rules:
                    values = ""
                    if rule["values"]:
                        values = "<br>".join(
                            f"**{k}**: {v}" for k, v in rule["values"].items()
                        )

                    f.write(
                        f"| **{rule['title']}** | "
                        f"{rule['description']} | "
                        f"{status_badge(rule['status'])} | "
                        f"{values} |\n"
                    )

                f.write("\n")

    return filename
