from pypdf import PdfReader

STARTING_ID = 11000


reader = PdfReader(
    "CIS_Oracle_MySQL_Enterprise_Edition_8.0_Benchmark_v1.3.0.pdf"
)
in_toc = False
in_recs = False
in_rule = False
output = ""
rules = {"Automated": {}, "Manual": {}}
for page in reader.pages:
    contents = page.extract_text()
    if "Table of Contents" in contents:
        in_toc = True
    if "Overview" in contents and "....." not in contents:
        in_toc = False
    if in_toc:
        for i, line in enumerate(contents.split("\n")):
            if "Page" in line:
                pass
            if "Automated" in line and not line.startswith("Automated"):
                rules["Automated"][line.split(".....")[0]] = {}
            if "Manual" in line and not line.startswith("Manual"):
                rules["Manual"][line.split(".....")[0]] = {}    
    if "Reccomendations" in contents and not in_toc:
        in_recs = True
    if "MySQL RDBMS" in contents and in_recs:
        in_rule = True
    if in_rule:
        pass
        # for line in contents.split("\n"):
        #     if "Page" in line:
        #         pass

print("Automated")
for rule in rules["Automated"]:
    print(rule)
print("Manual")
for rule in rules["Manual"]:
    print(rule)
# with open("output.txt", "w") as file:
#     file.write(output)
