def transform_data(data):
    transformed_data = {}
    
    for section, content in data.items():
        if section == "visual_representations":
            continue
        
        if isinstance(content, dict):
            if all(isinstance(value, (int, float, str)) for value in content.values()):
                transformed_data[section] = content
            else:
                for key, value in content.items():
                    if key != "visual_representations":
                        transformed_data[key] = value
        else:
            transformed_data[section] = content
    
    return transformed_data