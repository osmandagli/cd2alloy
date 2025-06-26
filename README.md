# CD2Alloy

**CD2Alloy** is a tool that automatically translates UML Class Diagrams (CDs) into Alloy models, enabling formal analysis and model checking on software designs.

---

## 📌 Usage Guide

### 1. Design Your Class Diagram
Create your UML Class Diagram using [PlantUML](https://plantuml.com/), which supports exporting to XMI format.

### 2. Export as XMI
Convert your `.wsd` class diagram into an XMI file using the following command:
```bash
plantuml -txmi:star <cd_name>.wsd
```

### 3. Clone This Repository
Use the following command to clone the repository:
```bash
git clone https://github.com/osmandagli/cd2alloy.git
cd cd2alloy
```

### 4. Place Your XMI File
Copy the `.xmi` file you created and place it in the `data/` directory:

```bash
cp <PlantUML_workspace>/<cd_name>.xmi data/cd.xmi
```

### 5. Run the Translator
Execute the translation by running the main Python script:

```bash
python src/main.py
```

### 6. View the Alloy Output
After running the script, the translated Alloy model will be written to:

```bash
output.als
```

You can open this file using Alloy Analyzer.

---

## 💡 Notes

- The tool assumes the XMI file is generated using **PlantUML with StarUML compatibility**, via:

  ```bash
  plantuml -txmi:star <cd_name>.wsd
  ```
- The Plantuml version used in this project is `1.2025.2`

---

## 📁 Example Files

This repository includes example `.xmi` input and `.als` output files to demonstrate the workflow.  
You can find them under the `data/` and root directories, respectively.

---

## 📫 Feedback & Contribution

Contributions are welcome! Feel free to open issues or submit pull requests.

If you encounter any issues or have suggestions for improvements, reach out via [GitHub](https://github.com/osmandagli).

---

## 🔗 Project Link

You can find the GitHub repository here:  
👉 [https://github.com/osmandagli/cd2alloy](https://github.com/osmandagli/cd2alloy)


