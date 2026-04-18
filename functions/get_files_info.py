import os
import json

def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

        if not os.path.isdir(target_dir):
            raise RuntimeError(f'Error: "{directory}" is not a directory')

        if valid_target_dir is False :
            raise RuntimeError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        contents = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir,item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path) if not is_dir else 0
            contents.append({
                "name" : item,
                "size": size,
                "is_dir": is_dir
            })
        data = json.loads(json.dumps(contents, indent=2))

        for item in data:
            print(f"- {item['name']} file_size={item['size']} bytes, is_dir={item['is_dir']}")
    except Exception as e:
        print(f"Error: {e}")
    
