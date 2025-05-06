import os
import threading
import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy 
assert numpy 


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()

if os.path.exists("tempR.mp3"):
    os.remove("tempR.mp3")  # Remove the existing file if it exists
    # print(f"Temporary file '{input_mp3}' deleted.")

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


stop_event = threading.Event()  # Event to signal stopping the recording

def wait_for_enter_to_stop():
    """
    Wait for the user to press Enter to stop the recording.
    """
    input("Press Enter to stop the recording...\n")
    stop_event.set()  # Signal to stop the recording loop
    q.put(None)  # Ensure the queue is unblocked

def rcn():
    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        if args.filename is None:
            args.filename = 'tempR.mp3'  # Use a fixed filename

        # Start a thread to wait for Enter key press
        stop_thread = threading.Thread(target=wait_for_enter_to_stop)
        stop_thread.start()

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                        channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                print('#' * 80)
                print('Recording... Press Enter to stop.')
                print('#' * 80)
                while not stop_event.is_set():  # Check the stop event
                    try:
                        data = q.get(timeout=0.1)  # Timeout to check the stop event
                        if data is None:  # Stop signal received
                            break
                        file.write(data)
                    except queue.Empty:
                        continue  # Continue if no data is available in the queue

    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
