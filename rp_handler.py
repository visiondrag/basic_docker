import runpod
import time
import sys
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

def test_import_methods():
    import os
    import sys
    
    results = {}
    
    # Method 1: Direct package import
    try:
        from code.func import check_run
        results["method_1_package_import"] = {"success": True, "result": check_run()}
    except Exception as e:
        results["method_1_package_import"] = {"success": False, "error": str(e)}
    
    # Method 2: Add to sys.path and import
    try:
        sys.path.append('code')
        from func import check_run as check_run_2
        results["method_2_syspath"] = {"success": True, "result": check_run_2()}
    except Exception as e:
        results["method_2_syspath"] = {"success": False, "error": str(e)}
    
    # Method 3: Add absolute path to sys.path
    try:
        code_path = os.path.abspath('code')
        if code_path not in sys.path:
            sys.path.append(code_path)
        from func import check_run as check_run_3
        results["method_3_abspath"] = {"success": True, "result": check_run_3()}
    except Exception as e:
        results["method_3_abspath"] = {"success": False, "error": str(e)}
    
    # Method 4: importlib
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("func", "code/func.py")
        func_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(func_module)
        results["method_4_importlib"] = {"success": True, "result": func_module.check_run()}
    except Exception as e:
        results["method_4_importlib"] = {"success": False, "error": str(e)}
    
    # Method 5: exec with open
    try:
        with open('code/func.py', 'r') as f:
            code_content = f.read()
        local_vars = {}
        exec(code_content, {}, local_vars)
        results["method_5_exec"] = {"success": True, "result": local_vars['check_run']()}
    except Exception as e:
        results["method_5_exec"] = {"success": False, "error": str(e)}
    
    # Method 6: Change working directory temporarily
    try:
        original_cwd = os.getcwd()
        os.chdir('code')
        sys.path.insert(0, '.')
        from func import check_run as check_run_6
        result = check_run_6()
        os.chdir(original_cwd)
        results["method_6_chdir"] = {"success": True, "result": result}
    except Exception as e:
        results["method_6_chdir"] = {"success": False, "error": str(e)}
        try:
            os.chdir(original_cwd)  # Make sure we change back
        except:
            pass
    
    return results

def debug_code_directory():
    import os
    debug_info = {
        "code_dir_exists": os.path.exists('code'),
        "code_is_directory": os.path.isdir('code'),
        "code_contents": [],
        "init_py_exists": False,
        "func_py_exists": False,
        "current_working_directory": os.getcwd(),
        "python_path": sys.path
    }
    
    if os.path.exists('code'):
        try:
            debug_info["code_contents"] = os.listdir("code")
            debug_info["init_py_exists"] = os.path.exists('code/__init__.py')
            debug_info["func_py_exists"] = os.path.exists('code/func.py')
        except Exception as e:
            debug_info["error_reading_code_dir"] = str(e)
    
    return debug_info

def handler(event):
    a = list_current_folder()
    debug_info = debug_code_directory()
    import_tests = test_import_methods()
    
    return {
        "folder_listing": a,
        "debug": debug_info,
        "import_tests": import_tests
    }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler })
