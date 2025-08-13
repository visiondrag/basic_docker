import os

def list_current_folder():
    current_dir = os.getcwd()
    result = {
        "current_directory": current_dir,
        "directories": [],
        "files": []
    }

    for item in os.listdir(current_dir):
        if os.path.isdir(item):
            result["directories"].append(item)
        else:
            result["files"].append(item)

    return result