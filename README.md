# Azure Language Studio Project Generator

This utility generates a complete Azure Language Studio project from a QnA Maker knowledgebase export file. It solves the challenge of converting between incompatible formats when migrating from QnA Maker to Azure Language Studio Custom Question Answering.

## Background and Purpose

Microsoft is transitioning from the older QnA Maker service to the newer Azure Language Studio Custom Question Answering service. This creates a specific migration challenge:

- **QnA Maker**: Provides knowledgebase exports in JSON format via its REST API
- **Azure Language Studio**: Requires a complete project structure with multiple TSV files packaged as a ZIP

An Azure Language Studio project is not equivalent to a QnA Maker knowledgebase file. The project requires multiple specific TSV files, one of which is a converted version of the knowledgebase content.

This utility creates a complete Azure Language Studio project by:
1. Converting the QnA Maker JSON export to the required TSV format
2. Generating the additional required TSV files (Settings.tsv, Synonyms.tsv)
3. Organizing these files in the structure required for Azure Language Studio project import

## Understanding Azure Language Studio Projects vs. QnA Maker Knowledgebases

The fundamental difference that makes migration challenging:

1. QnA Maker operates with single knowledgebase files (exported as JSON via REST API)
2. Azure Language Studio operates with complete projects consisting of multiple files:
   - A primary TSV file containing the Q&A pairs (converted from knowledgebase content)
   - A Settings.tsv file with project configuration
   - A Synonyms.tsv file for synonym mappings
   - All packaged in a specific structure as a ZIP file

A QnA Maker knowledgebase file is not equivalent to an Azure Language Studio project. The project is a more comprehensive structure that includes the knowledgebase content plus additional configuration files.

## How This Tool Generates Azure Language Studio Projects

The `json_to_tsv_converter.py` script generates a complete Azure Language Studio project by:

1. Taking a QnA Maker JSON knowledgebase export file (obtained via the [QnA Maker Download API](https://learn.microsoft.com/en-us/rest/api/qnamaker/knowledgebase/download?view=rest-qnamaker-v4.0&tabs=HTTP))
2. Converting the knowledgebase content to the required TSV format
3. Generating the additional required project files:
   - `[filename].tsv` - Primary file containing all question/answer pairs (converted from the knowledgebase)
   - `Settings.tsv` - Contains project settings and configuration (generated with default values)
   - `Synonyms.tsv` - Contains synonym mappings (generated as an empty template)
4. Organizing these files in a subfolder with the correct structure for Azure Language Studio project import

This provides a complete conversion pipeline that enables seamless migration without data loss or manual recreation.

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

## Step 1: Obtaining the QnA Maker Knowledgebase Export

The first step is to export your existing knowledgebase from QnA Maker in JSON format. This can only be done using the QnA Maker REST API, as the portal doesn't provide a complete export feature.

### Using the QnA Maker Download API

1. Use the [QnA Maker Download API](https://learn.microsoft.com/en-us/rest/api/qnamaker/knowledgebase/download?view=rest-qnamaker-v4.0&tabs=HTTP) to export your knowledgebase.

2. Save the API response as a JSON file on your local machine. You might use Postman, curl, or any other API tool to make this request and save the response.

3. This JSON file contains your knowledgebase content but is not in a format that Azure Language Studio can directly import as a project. It will serve as the input for our project generation script.

### Input JSON Format Example

Your input JSON should follow this structure (this is the standard format provided by the QnA Maker Download API):

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
This file contains the converted knowledgebase content from your QnA Maker export.

### Settings.tsv

```
Key	Value
Description	QNA Migration - [filename]
Language	English
DefaultAnswerForKB	No answer found
```
This file contains project-specific settings required by Azure Language Studio that weren't part of the original QnA Maker knowledgebase.

### Synonyms.tsv

```
Synonyms
```
This is an additional required file for Azure Language Studio projects that supports synonym matching. It's not part of the QnA Maker knowledgebase, but is required for a complete Azure Language Studio project.

## Why Migration is Necessary

Microsoft is transitioning from QnA Maker to Azure Language Studio Custom Question Answering as part of their AI service improvements. Some key reasons for this migration:

1. **Service End-of-Life**: QnA Maker is being deprecated in favor of Azure Language Studio
2. **Enhanced Features**: Azure Language Studio offers improved question answering capabilities
3. **Better Integration**: Azure Language Studio integrates better with other Azure Cognitive Services
4. **Performance Improvements**: The newer service offers better performance and scalability

This migration tool helps you preserve your investment in QnA Maker by transferring your knowledge bases to the new service.

## Complete Migration Process

The complete migration process from QnA Maker to Azure Language Studio involves these key steps:

1. **Export from QnA Maker**:
   - Use the [QnA Maker Download API](https://learn.microsoft.com/en-us/rest/api/qnamaker/knowledgebase/download?view=rest-qnamaker-v4.0&tabs=HTTP) to export your knowledge base as JSON
   - This is the only official way to extract your complete knowledge base data

2. **Format Conversion** (this is where this tool comes in):
   - Use this script to convert the JSON export to the required TSV file structure
   - The script creates all necessary files in the exact format expected by Azure Language Studio

3. **Prepare for Import**:
   - Create a ZIP archive containing the generated TSV files
   - **Important**: Azure Language Studio will only accept imports in this specific format

4. **Import to Azure Language Studio**:
   - Import the ZIP file to create a new project in Azure Language Studio

## Step 3: Creating the ZIP File for Import

After running the script, you need to properly package the files for import into Azure Language Studio:

1. **Create a ZIP file containing your project files**:
   - Navigate to the output subfolder created by the script (e.g., `knowledgebase_rick01`)
   - Select all three TSV files: `[filename].tsv`, `Settings.tsv`, and `Synonyms.tsv`
   - Create a ZIP archive containing these files (e.g., `knowledgebase_rick01.zip`)
   - **Important**: Do not add any additional folders within the ZIP - the TSV files must be at the root level of the ZIP archive

2. **Import your project to Azure Language Studio**:
   - Go to [Azure Language Studio](https://language.cognitive.azure.com/)
   - Navigate to "Custom question answering" under "Projects"
   - Click "Import" to create a new project from your ZIP file
   - Select your newly created ZIP file when prompted

3. **Review and publish**:
   - Review the imported questions and answers
   - Make any necessary adjustments
   - Test your knowledge base
   - Publish when ready

## Common Issues and Solutions

### Export Issues
- **API Access**: Ensure you have the correct endpoint key to access the QnA Maker API
- **Large Knowledge Bases**: Very large knowledge bases might timeout during export - consider exporting in smaller chunks if possible

### Conversion Issues
- **File encoding**: Make sure your input JSON file is UTF-8 encoded to avoid character issues
- **Line endings**: The script handles different line endings (CRLF/LF), but if you encounter issues, ensure your files use consistent line endings
- **JSON format**: If you get JSON parse errors, verify that the JSON matches the expected QnA Maker export format

### Import Issues
- **ZIP structure**: Azure Language Studio expects the TSV files to be at the root level of the ZIP archive - don't nest them in folders
- **File names**: Don't rename the Settings.tsv or Synonyms.tsv files
- **Format errors**: If import fails, check for special characters or formatting issues in your questions or answers

## Important Notes

- The script automatically sets the `Description` field in `Settings.tsv` to "QNA Migration - [filename]"
- The script preserves metadata and prompt follow-ups from the original JSON file
- The `Synonyms.tsv` file is created with just the header, as QnA Maker exports don't include synonyms
- You may need to adjust confidence thresholds and other settings after import in Azure Language Studio
- Test your knowledge base thoroughly after migration to ensure it behaves as expected

## Additional Resources

- [QnA Maker Download API](https://learn.microsoft.com/en-us/rest/api/qnamaker/knowledgebase/download?view=rest-qnamaker-v4.0&tabs=HTTP) - To export your QnA Maker knowledge base
- [QnA Maker to Language Service Migration Guide](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/how-to/migrate-qnamaker) - Official migration guidance
- [Azure Language Studio Documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/overview) - Learn about the new service
- [Import and Export Knowledge Bases](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/how-to/import-knowledge-bases) - Details on the import process
- [TSV Format Specifications](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/custom-question-answering/reference-tsv-format-custom-qa) - Reference for the TSV format
