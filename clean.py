def clean_output(output):
    cleaned_list = []
    task_number = 1
    
    for line in output:
        cleaned_line = line.replace('**', '').replace('\n', '').strip()
        
        if cleaned_line and cleaned_line[0].isdigit() and cleaned_line[1] == '.':
            cleaned_list.append(f"{cleaned_line[3:].strip()}")
            task_number += 1
    return cleaned_list
