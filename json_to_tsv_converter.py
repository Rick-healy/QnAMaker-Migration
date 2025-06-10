#!/usr/bin/env python3
"""
QnA Maker JSON to TSV Converter Script

This script converts QnA Maker JSON export files to TSV format following the standard QnA Maker format.
It creates a folder named after the input JSON file and generates three TSV files:
1. Main QnA file with the same name as the JSON file
2. Settings.tsv with customized description
3. Synonyms.tsv with default content

Usage:
    python json_to_tsv_converter.py <json_file_path>

Example:
    python json_to_tsv_converter.py export.json
"""

import json
import os
import sys
import shutil
from pathlib import Path


def convert_json_to_tsv(json_file_path):
    """
    Convert a QnA Maker JSON file to TSV format.
    
    Args:
        json_file_path (str): Path to the JSON file to convert
    
    Returns:
        None
    """
    # Validate file exists and has .json extension
    if not os.path.exists(json_file_path):
        print(f"Error: File {json_file_path} does not exist.")
        sys.exit(1)
    
    if not json_file_path.lower().endswith('.json'):
        print("Error: Input file must be a JSON file with .json extension.")
        sys.exit(1)
    
    try:
        # Get file base name and create folder
        file_path = Path(json_file_path)
        base_name = file_path.stem  # Gets filename without extension
        folder_path = os.path.join(file_path.parent, base_name)
        
        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")
        
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Create main QnAs.tsv file
        create_qnas_tsv(data, folder_path, base_name)
        
        # Create Settings.tsv file
        create_settings_tsv(folder_path, base_name)
        
        # Create Synonyms.tsv file
        create_synonyms_tsv(folder_path)
        
        print(f"Conversion completed successfully. Files are located in {folder_path}")
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_file_path}. Error details: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


def clean_text_for_tsv(text):
    """
    Clean text by removing or replacing characters that could break TSV format.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
        
    # Replace tab characters with spaces
    text = text.replace('\t', ' ')
    
    # Replace newlines with a space
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    
    # Remove multiple spaces
    while '  ' in text:
        text = text.replace('  ', ' ')
        
    return text.strip()

def create_qnas_tsv(data, folder_path, base_name):
    """
    Create the QnAs TSV file from the JSON data.
    
    Args:
        data (dict): The JSON data
        folder_path (str): The folder to save the TSV file
        base_name (str): The base name for the output file
        
    Returns:
        None
    """
    output_file_path = os.path.join(folder_path, f"{base_name}.tsv")
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as tsv_file:
            # Write header
            tsv_file.write("Question\tAnswer\tSource\tMetadata\tSuggestedQuestions\tIsContextOnly\tPrompts\tQnaId\tSourceDisplayName\n")
            
            # Write data
            for qna in data.get("qnaDocuments", []):
                # Get questions array
                questions = qna.get("questions", [""])
                
                # Get other fields and clean them
                answer = clean_text_for_tsv(qna.get("answer", ""))
                source = clean_text_for_tsv(qna.get("source", ""))
                metadata = json.dumps(qna.get("metadata", []))
                
                # Format context data
                context = qna.get("context", {})
                is_context_only = str(context.get("isContextOnly", False))
                prompts = json.dumps(context.get("prompts", []))
                
                # Set ID and source display name
                qna_id = str(qna.get("id", ""))
                source_display_name = clean_text_for_tsv(qna.get("source", ""))  # Using source as display name if not specified
                
                # Default suggested questions as empty array
                suggested_questions = "[]"
                
                # Create a row for each question
                for question in questions:
                    # Clean the question text
                    clean_question = clean_text_for_tsv(question)
                    
                    # Write the row
                    row = f"{clean_question}\t{answer}\t{source}\t{metadata}\t{suggested_questions}\t{is_context_only}\t{prompts}\t{qna_id}\t{source_display_name}\n"
                    tsv_file.write(row)
                
        print(f"Created QnAs file: {output_file_path}")
        
    except Exception as e:
        print(f"Error creating QnAs TSV file: {str(e)}")
        raise


def create_settings_tsv(folder_path, base_name):
    """
    Create the Settings TSV file.
    
    Args:
        folder_path (str): The folder to save the TSV file
        base_name (str): The base name for the description
        
    Returns:
        None
    """
    settings_path = os.path.join(folder_path, "Settings.tsv")
    
    try:
        with open(settings_path, 'w', encoding='utf-8') as settings_file:
            settings_file.write("Key\tValue\n")
            settings_file.write(f"Description\tQNA Migration - {base_name}\n")
            settings_file.write("Language\tEnglish\n")
            settings_file.write("DefaultAnswerForKB\tNo answer found\n")
            
        print(f"Created Settings file: {settings_path}")
        
    except Exception as e:
        print(f"Error creating Settings TSV file: {str(e)}")
        raise


def create_synonyms_tsv(folder_path):
    """
    Create the Synonyms TSV file.
    
    Args:
        folder_path (str): The folder to save the TSV file
        
    Returns:
        None
    """
    synonyms_path = os.path.join(folder_path, "Synonyms.tsv")
    
    try:
        with open(synonyms_path, 'w', encoding='utf-8') as synonyms_file:
            synonyms_file.write("Synonyms\n")
            
        print(f"Created Synonyms file: {synonyms_path}")
        
    except Exception as e:
        print(f"Error creating Synonyms TSV file: {str(e)}")
        raise


def main():
    """Main function to handle command line arguments and run conversion."""
    if len(sys.argv) != 2:
        print("Usage: python json_to_tsv_converter.py <json_file_path>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    convert_json_to_tsv(json_file_path)


if __name__ == "__main__":
    main()
