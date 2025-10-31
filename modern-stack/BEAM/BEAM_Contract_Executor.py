# BEAM_Contract_Executor.py
#
# This script demonstrates the core automation logic for transforming the enhanced
# BEAM Table (the Zero-Translation Governance Contract) into executable dbt Semantic Layer
# code, thereby enforcing the governance standard at an enterprise scale.
#
# The script simulates reading the BEAM Table, which now contains the mandatory
# EDM linking fields: PHYSICAL_EDM_TABLE, PHYSICAL_EDM_COLUMN, and AGGREGATION_TYPE.

import yaml
import os

# --- 1. SIMULATED BEAM TABLE CONTRACT ---
# This list of dictionaries represents data pulled from the centralized BEAM Table.
# Each entry is a single atomic metric definition, complete with the new contractual fields.
BEAM_TABLE_CONTRACT = [
    {
        "METRIC_NAME": "total_billed_revenue",
        "DESCRIPTION": "The total amount billed for all service events.",
        "PHYSICAL_EDM_TABLE": "fct_service_event",
        "PHYSICAL_EDM_COLUMN": "billed_amount",
        "AGGREGATION_TYPE": "sum",
    },
    {
        "METRIC_NAME": "count_of_service_events",
        "DESCRIPTION": "The number of unique service events recorded.",
        "PHYSICAL_EDM_TABLE": "fct_service_event",
        "PHYSICAL_EDM_COLUMN": "service_event_id",
        "AGGREGATION_TYPE": "count_distinct",
    },
    # Note: Complex metrics (like average) are handled by the KPI Library
    # which consumes these atomic metrics. They are not defined here.
]

# --- 2. FILE GENERATION PATHS ---
# Define the output directory and file for the Semantic Models (where measures live)
OUTPUT_DIR = "semantic_layer_output"
SEMANTIC_MODELS_FILE = os.path.join(OUTPUT_DIR, "semantic_models.yml")

# --- 3. CORE LOGIC FUNCTIONS ---

def generate_semantic_model_config(contract_data):
    """
    Groups metrics by their EDM table and generates the MetricFlow Semantic Model config.
    """
    # 1. Group metrics by their physical source table (PHYSICAL_EDM_TABLE)
    models_by_table = {}
    for entry in contract_data:
        table = entry["PHYSICAL_EDM_TABLE"]
        if table not in models_by_table:
            models_by_table[table] = []
        models_by_table[table].append(entry)

    # 2. Structure the data into the MetricFlow YAML format
    semantic_models = []
    for table_name, metrics in models_by_table.items():
        # The Semantic Model name is derived from the EDM table name
        model_name = f"sm_{table_name}"
        
        # Build the list of measures and dimensions for this model
        measures = []
        for metric in metrics:
            measures.append({
                "name": metric["METRIC_NAME"],
                "expr": metric["PHYSICAL_EDM_COLUMN"], # The physical column is the expression
                "agg": metric["AGGREGATION_TYPE"],
                "description": metric["DESCRIPTION"],
                "valid_for": [table_name], # Simple example: entity is valid for its own table
            })

        # Create the full Semantic Model definition
        semantic_models.append({
            "name": model_name,
            "description": f"Semantic Model derived from the BEAM Table for the {table_name} EDM entity.",
            "defaults": {"agg_time_dimension": "service_event_timestamp"}, # Assume a standard time dim
            "entities": [{"name": table_name, "type": "primary"}], # Assume the table is the primary entity
            "measures": measures,
            "dimensions": [
                {"name": "service_event_timestamp", "type": "time", "expr": "event_timestamp", "type_params": {"time_granularity": "day"}},
            ],
            # Assumes dbt model exists matching the physical table name
            "model": table_name
        })

    # 3. Wrap the content for the final YAML file structure
    final_output = {
        "version": 2,
        "semantic_models": semantic_models
    }

    return final_output

def execute_automation(contract_data, output_filepath):
    """Executes the transformation and writes the output YAML file."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Generate the MetricFlow config structure
    yaml_data = generate_semantic_model_config(contract_data)

    # Write the YAML file
    with open(output_filepath, 'w') as f:
        yaml.dump(yaml_data, f, sort_keys=False, indent=4)

    print(f"✅ Success: dbt Semantic Models generated at {output_filepath}")
    print(f"   Model Count: {len(yaml_data['semantic_models'])}")
    print("   Review the generated YAML file content below:")
    print("-" * 30)
    print(yaml.dump(yaml_data, default_flow_style=False, sort_keys=False, indent=2))
    print("-" * 30)


# --- 4. EXECUTION ---
if __name__ == "__main__":
    execute_automation(BEAM_TABLE_CONTRACT, SEMANTIC_MODELS_FILE)
