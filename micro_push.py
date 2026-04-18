import subprocess
import os

def run_git(args):
    try:
        # Use encoding='utf-8' to handle non-ASCII characters in git output
        result = subprocess.run(['git'] + args, capture_output=True, text=True, check=True, encoding='utf-8', errors='replace')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git {' '.join(args)}: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def micro_push():
    # 1. Reset to origin to ensure a clean start
    print("Resetting to origin/main...")
    res = run_git(['reset', 'origin/main'])
    if res is None:
        print("Failed to reset. Make sure 'origin/main' exists.")
        return

    # 2. Get all unstaged/untracked files
    # We'll stage everything first to see the list, then unstage and add one by one.
    run_git(['add', '.'])
    files_str = run_git(['diff', '--cached', '--name-only'])
    run_git(['reset']) # Unstage all

    if not files_str:
        print("No changes to push.")
        return

    files = files_str.split('\n')
    print(f"Found {len(files)} files to push iteratively.")

    for i, file in enumerate(files):
        if not file or not os.path.exists(file):
            continue
        
        print(f"[{i+1}/{len(files)}] Pushing: {file}")
        
        # Stage one file
        run_git(['add', file])
        
        # Commit
        commit_msg = f"micro-update: {os.path.basename(file)}"
        if run_git(['commit', '-m', commit_msg]):
            # Try to push
            push_res = run_git(['push', 'origin', 'main'])
            if push_res is not None:
                print(f"  Successfully pushed {file}")
            else:
                print(f"  FAILED to push {file} (Likely too large or server error)")
                # Rollback this commit so it doesn't block others
                run_git(['reset', '--soft', 'HEAD~1'])
                run_git(['reset', 'HEAD', file])
        else:
            print(f"  Failed to commit {file}")

if __name__ == "__main__":
    micro_push()
