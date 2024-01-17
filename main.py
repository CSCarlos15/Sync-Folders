#!/usr/bin/env python3

import os
import shutil
import time
from filecmp import dircmp
import logging
import argparse

def synchronize_folders(source, replica):
    dc = dircmp(source, replica)
    
    # Copy new/modified files and directories from source to replica
    for item in dc.left_only + dc.diff_files:
        source_path = os.path.join(source, item)
        replica_path = os.path.join(replica, item)
        if os.path.isdir(source_path):
            shutil.copytree(source_path, replica_path)
            logging.info(f'Directory copied from {source_path} to {replica_path}')
        else:
            shutil.copy2(source_path, replica_path)
            logging.info(f'File copied from {source_path} to {replica_path}')

    # Remove files and directories inside replica not coincident with source
    for item in dc.right_only + dc.funny_files:
        item_path = os.path.join(replica, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            logging.info(f'Directory {item_path} has been removed')
        else:
            os.remove(item_path)
            logging.info(f'File {item_path} has been removed')

if __name__ == "__main__":

    #Makes possible to provide inputs for folder paths, sync interval and log file through terminal
    parser = argparse.ArgumentParser(description='Sync folders')
    parser.add_argument('source_folder', help='Path to the source folder')
    parser.add_argument('replica_folder', help='Path to the replica folder')
    parser.add_argument('--interval', type=int, default=10, help='Synchronization interval in hours')
    parser.add_argument('--log_file', help='Log file path')
    args = parser.parse_args()

    #Write logs into a file called logs
    INFO = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=args.log_file, level=logging.INFO, format=INFO)
    
    #Output logs into terminal
    terminal = logging.StreamHandler()
    terminal.setLevel(logging.INFO)
    header = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    terminal.setFormatter(header)
    logging.getLogger('').addHandler(terminal)
    
    while True:
        source_folder = args.source_folder
        replica_folder = args.replica_folder
        synchronize_folders(source_folder, replica_folder)
        time.sleep(args.interval)