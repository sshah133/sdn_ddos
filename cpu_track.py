import time
import psutil
import subprocess

def get_pox_pid():
  for proc in psutil.process_iter(['pid', 'cmdline']):
    try:
      if 'pox.py' in ' '.join(proc.info['cmdline']):
        return proc.info['pid']
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      continue
  return None

def monitor_controller(pid, log_file='controller_usage.txt'):
  with open(log_file, 'a') as f:
    while True:
      try:
        proc = psutil.Process(pid)
        cpu = proc.cpu_percent(interval=1)
        mem = proc.memory_percent()
        cmdline = ' '.join(proc.cmdline())
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp}, CPU: {cpu:.2f}%, MEM: {mem:.2f}%, CMD: {cmdline}\n")
        f.flush()
      except psutil.NoSuchProcess:
        print("Controller process ended.")
        break

if __name__ == "__main__":
  pid = get_pox_pid()
  if pid:
    print(f"Monitoring POX controller with PID {pid}")
    monitor_controller(pid)
  else:
    print("POX controller not found.")
