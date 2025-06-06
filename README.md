# QnA Maker JSON to TSV Converter

This tool converts QnA Maker or Azure Language Studio Custom Question Answering JSON export files to TSV format suitable for importing into Azure Language Studio projects.

## Overview

The `json_to_tsv_converter.py` script takes a QnA Maker JSON export file and converts it to the TSV format required by Azure Language Studio Custom Question Answering. The script creates three TSV files with the proper format:

1. `[filename].tsv` - Main file containing all question/answer pairs
2. `Settings.tsv` - Contains project settings and configuration
3. `Synonyms.tsv` - Contains synonym mappings (if any)

All files are created in a subfolder named after the input file, making it easy to organize multiple projects.

## Requirements

- Python 3.6 or higher
- No additional libraries required (uses only standard Python libraries)

## Usage

```bash
python json_to_tsv_converter.py <json_file_path>
```

### Example

```bash
python json_to_tsv_converter.py knowledgebase_rick01.json
```

This command will:
1. Read the JSON file `knowledgebase_rick01.json`
2. Create a subfolder named `knowledgebase_rick01`
3. Generate three TSV files in that folder:
   - `knowledgebase_rick01.tsv`
   - `Settings.tsv`
   - `Synonyms.tsv`

## Input JSON Format Example

Your input JSON should follow this format:

```json
{
  "qnaDocuments": [
    {
      "id": 1,
      "answer": "You can change the default message if you use the QnAMakerDialog.",
      "source": "Custom Editorial",
      "questions": [
        "How can I change the default message from QnA Maker?"
      ],
      "metadata": [],
      "context": {
        "isContextOnly": false,
        "prompts": []
      }
    },
    {
      "id": 2,
      "answer": "You can use our REST apis to create a KB.",
      "source": "Custom Editorial",
      "questions": [
        "How do I programmatically create a KB?"
      ],
      "metadata": [
        {
          "name": "category",
          "value": "api"
        }
      ],
      "context": {
        "isContextOnly": false,
        "prompts": [
          {
            "displayOrder": 1,
            "qnaId": 3,
            "displayText": "Update KB"
          }
        ]
      }
    }
  ]
}
```

## Output Files Format

### Main TSV File ([filename].tsv)

```
Question	Answer	Source	Metadata	SuggestedQuestions	IsContextOnly	Prompts	QnaId	SourceDisplayName
How can I change the default message from QnA Maker?	You can change the default message if you use the QnAMakerDialog.	Custom Editorial	[]	[]	False	[]	1	Custom Editorial
How do I programmatically create a KB?	You can use our REST apis to create a KB.	Custom Editorial	[{"name": "category", "value": "api"}]	[]	False	[{"displayOrder": 1, "qnaId": 3, "displayText": "Update KB"}]	2	Custom Editorial
```

### Settings.tsv

```
Key	Value
Description	QNA Migration - [filename]
Language	English
DefaultAnswerForKB	No answer found
```

### Synonyms.tsv

```
Synonyms
```

## Importing into Azure Language Studio

After running the script, follow these steps to import your project into Azure Language Studio:

1. **Create a ZIP file**:
   - Navigate to the output subfolder created by the script (e.g., `knowledgebase_rick01`)
   - Select all three TSV files: `[filename].tsv`, `Settings.tsv`, and `Synonyms.tsv`
   - Create a ZIP archive containing these files (e.g., `knowledgebase_rick01.zip`)

2. **Import to Azure Language Studio**:
   - Go to [Azure Language Studio](https://language.cognitive.azure.com/)
   - Navigate to "Custom question answering" under "Projects"
   - Click "Import" to create a new project from your ZIP file
   - Follow the on-screen instructions to complete the import

3. **Review and publish**:
   - Review the imported questions and answers
   - Make any necessary adjustments
   - Test your knowledge base
   - Publish when ready

## Common Issues and Solutions

- **File encoding**: Make sure your input JSON file is UTF-8 encoded to avoid character issues.
- **Line endings**: The script handles different line endings (CRLF/LF), but if you encounter issues, ensure your files use consistent line endings.
- **JSON format**: If you get JSON parse errors, validate your JSON file structure using a JSON validator tool.

## Notes

- The script automatically sets the `Description` field in `Settings.tsv` to "QNA Migration - [filename]"
- The script preserves metadata and prompt follow-ups from the original JSON file
- The `Synonyms.tsv` file is created with just the header, ready for you to add synonyms if needed

## Additional Resources

- [Azure Language Studio Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/overview)
- [Import and Export Knowledge Bases](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/how-to/import-knowledge-bases)
- [TSV Format Specifications](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/reference-tsv-format-custom-qa)
