import os
import subprocess

def get_git_commit_id(directory_path):
    try:
        # Run the Git command to get the commit ID
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=directory_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            # Extract the commit ID from the output
            commit_id = result.stdout.strip()
            return commit_id
        else:
            print("Error:", result.stderr)
            return None

    except FileNotFoundError:
        print("Git executable not found.")
        return None
    
if __name__ == '__main__':
    print(get_git_commit_id(os.getcwd()))