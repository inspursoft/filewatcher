from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time, os, subprocess, logging, subprocess

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

patterns = "*"
ignore_patterns = ""
ignore_directories = False
case_sensitive = True

monitor_path = "/workspace"
check_list = "check.list"
check_list_path = os.path.join(monitor_path, check_list)
exec_path = "/exec"
process = "process.sh"
process_path = os.path.join(exec_path, process)

my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

def find(name, path):
  for root, dir, files in os.walk(path):
    if name in files:
      return True
  return False

def on_created(event):
  file_name = os.path.basename(event.src_path)
  log.info(f"Created file {file_name}...")

def on_modified(event):
  if find(check_list, monitor_path):
    log.info(f"Found {check_list} file under {check_list_path} will checking integrity ...")
    with open(check_list_path, "r") as f:
      integrity = True
      for fname in f.readlines():
        fname = fname.strip()
        if not find(fname, monitor_path):
          log.info(f"Missing {fname} per checking integrity...")  
          integrity = False
      if integrity:
        log.info(f"Met integrity will start processing after 3 seconds...")
        subprocess.call(["rm", "-f", check_list_path])
        time.sleep(3)
        subprocess.call(["sh", process_path])
        
my_event_handler.on_created = on_created
my_event_handler.on_modified = on_modified

go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, monitor_path, recursive=go_recursively)

my_observer.start()
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  my_observer.stop()
  my_observer.join()