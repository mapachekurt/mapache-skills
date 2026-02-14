#!/usr/bin/env python3
"""
Monitor the skills/ directory and trigger sync on changes.
Requires: pip install watchdog
"""

import time
import sys
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SkillChangeHandler(FileSystemEventHandler):
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.last_sync = 0
        self.debounce_seconds = 2

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # We only care about changes within skills/
        if "skills" in Path(event.src_path).parts:
            self.trigger_sync(event.src_path)

    def trigger_sync(self, changed_file):
        now = time.time()
        if now - self.last_sync < self.debounce_seconds:
            return
            
        print(f"\n🔔 Change detected in: {changed_file}")
        
        # Run sync script
        sync_script = self.repo_root / "scripts" / "sync_skills.py"
        print("🚀 Triggering sync...")
        subprocess.run([sys.executable, str(sync_script)], cwd=self.repo_root, shell=True)
        
        self.last_sync = now

def main():
    repo_root = Path(__file__).parent.parent
    path_to_watch = repo_root / "skills"
    
    if not path_to_watch.exists():
        print(f"❌ Error: Skills directory not found: {path_to_watch}")
        sys.exit(1)

    print(f"👀 Monitoring skills directory: {path_to_watch}")
    print("💡 (Press Ctrl+C to stop manually)")
    
    event_handler = SkillChangeHandler(repo_root)
    observer = Observer()
    observer.schedule(event_handler, str(path_to_watch), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
