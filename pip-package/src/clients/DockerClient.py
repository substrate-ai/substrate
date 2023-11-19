from dataclasses import dataclass
import importlib.resources
import os
import shutil
import subprocess
import tempfile
from typing import Iterator, Optional, Union
from clients.JobStateMachine import JobStateMachine
import typer
import yaml
from python_on_whales import DockerClient as DockerPyClient
from python_on_whales import DockerException
from utils.console import console
from rich.live import Live
from rich.table import Table
from collections import deque
import docker
from tqdm import tqdm
import sys
from statemachine import StateMachine, State
import re
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.progress import Progress, BarColumn, TimeRemainingColumn, FileSizeColumn, TotalFileSizeColumn, TimeElapsedColumn, DownloadColumn, TransferSpeedColumn, ProgressColumn
from rich.text import Text
import time
from rich.console import Group
from rich.layout import Layout


class TimeElapsedRemainingColumn(ProgressColumn):
    # A custom column displaying time elapsed and remaining.
    def render(self, task):
        elapsed = self.get_elapsed(task)
        remaining = self.get_remaining(task)
        # Format the elapsed and remaining time
        elapsed_str = str(elapsed).split('.')[0]  # Removing milliseconds
        remaining_str = str(remaining).split('.')[0]  # Removing milliseconds
        return Text(f"{elapsed_str}/{remaining_str}", style="progress.time")


@dataclass
class Layer:
    layer_id: str
    total_size: int
    current_size: int

class DockerProgressBar:
    def __init__(self):
        self.layer_sizes = {}
        self.all_layers = set()
        self.pushed_layers = set()
        self.total_size = 0
        self.current_progress = 0
        self.can_be_closed = False
        self.progress = Progress(
        "[progress.percentage]{task.percentage:>3.0f}%",
        BarColumn(),
        DownloadColumn(),
        TimeElapsedColumn(), 
        TextColumn("•", justify="center"),
        TimeRemainingColumn(),
        TransferSpeedColumn()
        )
        self.progress_task = self.progress.add_task("progress_bar", total=0, start=False)

    def split_number_and_unit(self, s):
        """
        Splits a string into its number and unit components.

        :param s: String containing a number followed by a unit (e.g., '28.58MB')
        :return: A tuple with the number part and the unit part
        """
        # Using regular expression to match the number and unit parts
        match = re.match(r"([0-9.]+)([a-zA-Z]+)", s)
        if match:
            number, unit = match.groups()

            return (float(number), unit)
        else:
            return None

    def parse_line_to_dict(self, line: str):
        """
        Parse lines like:
        "#6 sha256:d5dae585b6c1569dc4bab1d9035594dfbe38a179e6aa298b1d79a7af00257daf 4.19MB / 879.14MB 44.1s"
        and
        "#6 sha256:c562fd0c9fc50dd01a438b46afb955cb128e0a4de45b3c23ef3a8e8394018247 1.52kB / 1.52kB 5.7s done"
        into a dictionary format.
        """

        # print("line", line)
        # Strip newline character and split the line into parts
        parts = line.strip().split()

        # print("parts",  parts)

        # Extracting relevant information
        id_part = parts[1]  # id
        current_part = parts[2]  # current
        total_part = parts[4]  # total
        # print("current_part", current_part)
        # print("total_part", total_part)

        # Parsing the sizes into bytes
        def size_to_bytes(size_str):
            size, unit = self.split_number_and_unit(size_str)
            if unit == "MB":
                return size * 1_000_000
            elif unit == "kB":
                return size * 1_000
            elif unit == "GB":
                return size * 1_000_000_000
            elif unit == "B":
                return size
            else:
                raise ValueError(f"Unknown unit: {unit}")

        current_bytes = size_to_bytes(current_part)
        total_bytes = size_to_bytes(total_part)

        # Determine the status
        status = 'Pulled' if parts[-1] == 'done' else 'Pulling'

        if status == 'Pulling':
            progress_detail = {'current': int(current_bytes), 'total': int(total_bytes)}
        else:
            progress_detail = {}

        # Building the dictionary
        parsed_dict = {
            'status': status,
            'progressDetail': progress_detail,
            'id': id_part
        }

        # print("parsed_dict", parsed_dict)
        # print("line", line)

        return parsed_dict
    
    def add_download_string(self, download_string):
        output_line = self.parse_line_to_dict(download_string)
        self.add_datapoint(output_line)

    def add_datapoint(self, output_line):
        # skip datapoint that is not a datapoint
        if output_line.get('status') not in ["Pulling", "Pushing", "Pushed", "Pulled"]:
            return

        layer_id = output_line.get('id')
        self.all_layers.add(layer_id)

        if output_line.get('status') in ['Pulling', 'Pushing']:
            layer_total = output_line['progressDetail'].get('total', 0)
            self.total_size += layer_total - self.layer_sizes.get(layer_id, {'total': 0})['total']
            self.layer_sizes[layer_id] = {'total': layer_total, 'current': output_line['progressDetail'].get('current', 0)}
            self.progress.update(self.progress_task, total=self.total_size)

            current_total_progress = sum(layer['current'] for layer in self.layer_sizes.values())
            self.progress.update(self.progress_task, completed=current_total_progress)

        if output_line.get('status') in ['Pushed', 'Pulled']:
            layer_total_size = self.layer_sizes[layer_id]['total']
            self.layer_sizes[layer_id] = {'total': layer_total_size, 'current': layer_total_size}
            self.pushed_layers.add(layer_id)

        current_total_progress = sum(layer['current'] for layer in self.layer_sizes.values())
        self.progress.update(self.progress_task, completed=current_total_progress)

        if self.all_layers == self.pushed_layers and self.progress:
            self.progress.stop()
            

class DockerClient:

    

    def __init__(self, server, username, password, use_cache=True) -> None:
        self.docker = DockerPyClient()
        self.docker_py = docker.from_env()
        self.tag =  "substrate:latest"
        self.use_cache = use_cache

        try:
            self.docker.stats()
        except DockerException:
            console.print("Docker engine is not running or not installed, please start docker and try again")
            raise typer.Exit(code=1)
        
        self.docker.login(server=server, username=username, password=password)
        # hack to clean up the login message

        self.docker_py.login(registry=server, username=username, password=password)

    def convert_to_bytes(size_str):
        """
        Convert size string to bytes. Handles kB and MB.
        """
        size_str = size_str.replace('B', '').strip()  # Removing 'B' from kB or MB
        if 'k' in size_str:
            return float(size_str.replace('k', '')) * 1024
        elif 'M' in size_str:
            return float(size_str.replace('M', '')) * 1024 * 1024
        else:
            return float(size_str)  # Assuming the value is already in bytes if no unit is specified

    def push(self, image_name):
        progress_bar = DockerProgressBar()
        status = console.status("Uploading your code to the cloud", spinner="dots")

        group = Group(
            status,
            progress_bar.progress
        )
                
        with Live(group, console=console, refresh_per_second=4, transient=True):
            self.docker.image.tag(self.tag, image_name)
            logs = self.docker_py.api.push(image_name, stream=True, decode=True)

            for log in logs:
                progress_bar.add_datapoint(log)

        console.print(":heavy_check_mark: [bold green]Code uploaded to the cloud")

    # https://towardsdatascience.com/a-complete-guide-to-building-a-docker-image-serving-a-machine-learning-system-in-production-d8b5b0533bde
    def build(self):
        try:
            # open yaml file and get main location
            with open("substrate.yaml", "rt") as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                main_location = yaml_data["main_file_location"]
        except FileNotFoundError:
            console.print("Could not find substrate.yaml file, please make sure you are in the root of your project and have ran substrate-ai init", style="bold red")
            raise typer.Exit(code=1)

        # use tempfile to copy requirements.txt to dockerfile directory (traversable)



        with tempfile.TemporaryDirectory() as tempdir:
            # we do two copy because we can then have different docker layers and thus no recreating the requirement layer when we chaneg the code
            shutil.copyfile("./requirements.txt", os.path.join(tempdir, "requirements.txt"))
            shutil.copytree(".", os.path.join(tempdir, "code"))

            dockerfile_traversable = importlib.resources.files("resources").joinpath("Dockerfile")
            with open(dockerfile_traversable, "rt"):
                    # copy dockerfile to tempdir
                    shutil.copyfile(dockerfile_traversable, os.path.join(tempdir, "Dockerfile"))

            # self.use_cache = True
            # console.print(f"using cache: {cache}")
            logs = self.docker.build(context_path=tempdir, tags=[self.tag], platforms=["linux/amd64"], build_args={"MAIN_LOCATION": main_location}, cache=self.use_cache, stream_logs=True, pull=True)

            build_output_handler = BuildOutputHandler()
            build_output_handler.handle_build_output(logs)

            # handle failed dependencies installation gracefully
             

class BuildOutputHandler:
    def consume_iterator(self, logs: Iterator[str], until: Optional[str] = None):
        for log in logs:
            if until is not None and until.lower() in log.lower():
                break

    def handle_build_output(self, logs: Iterator[str]):
        self.consume_iterator(logs, until="FROM 038700340820.dkr.ecr.us-east-1.amazonaws.com/substrate-ai:base")

        self.handle_base_image_downloading(logs)

        self.consume_iterator(logs, until="RUN python3.10 -m pip install")

        self.handle_dependecy_installation(logs)

        self.consume_iterator(logs)

    def handle_base_image_downloading_helper(self, logs: Iterator[str]) -> Optional[str]:
        progress_bar = DockerProgressBar()
        status = console.status("Downloading base image (only done once)", spinner="dots")

        group = Group(
            status,
            progress_bar.progress
        )
                
        with Live(group, console=console, refresh_per_second=4, transient=True):
            first_log = next(logs, None)
            if first_log and "done" in first_log.lower() or "cached" in first_log.lower():
                return
            
            if self.check_is_downloading_line(first_log):
                clean_log = self.remove_before_second_space(first_log)
                progress_bar.add_download_string(clean_log)   

            for log in logs:
                if self.check_is_done(log):
                    return ":heavy_check_mark: [bold green]Base image downloaded"
                if self.check_is_downloading_line(log):
                    clean_log = self.remove_before_second_space(log)
                    progress_bar.add_download_string(clean_log)   

    def handle_base_image_downloading(self, logs: Iterator[str]):
        output = self.handle_base_image_downloading_helper(logs)
        if output:
            console.print(output)

     

    def handle_dependecy_installation_helper(self, logs: Iterator[str]) -> str:
        last_n_logs = LastNLogs()
        table = last_n_logs.get_table()
        spinner = console.status("Installing dependencies\n (Ran only when requirements.txt is modified)", spinner="dots")

        group = Group(
            spinner,
            table
        )

        # TODO bug, why does spinner not showing up?

        with Live(group, transient=True) as live:
            first_log = next(logs, None)


            if first_log and "cached" in first_log.lower():
                return ":heavy_check_mark: [bold green]Dependencies up-to-date"
            
            last_n_logs.parse_dependency_line(self.remove_before_second_space(first_log))


            for log in logs:
                if self.check_is_done(log):
                    return ":heavy_check_mark: [bold green]Dependencies installed"

                last_n_logs.parse_dependency_line(self.remove_before_second_space(log))
                table = last_n_logs.get_table()
                # live.update(group)
                live.update(table)


    def handle_dependecy_installation(self, logs: Iterator[str]):

        output = self.handle_dependecy_installation_helper(logs)
        console.print(output)



        

    def remove_before_second_space(self, s):
        """
        Removes everything before the second space in the given string.
        
        :param s: The input string.
        :return: Modified string with everything before the second space removed.
        """
        # Initialize counters
        space_count = 0
        for i, char in enumerate(s):
            if char == ' ':
                space_count += 1
                if space_count == 2:
                    return s[i + 1:].strip()
        return s  # Return the original string if less than two spaces are found

    def check_is_downloading_line(self, s):
        pattern = re.compile(r"^#(\d+)\s+sha256:([a-f0-9]{64})\s+([\d.]+(GB|MB|kB|B))\s+/\s+([\d.]+(GB|MB|kB|B))\s+(\d+(\.\d+)?s)(\s+done)?\n?$")
        return bool(pattern.match(s))

    def check_is_done(self, s):
        """
        check if format is like
        #6 DONE 152.1s
        """
        pattern = r'#\d+ DONE \d+\.\d+s\n?'
        return bool(re.match(pattern, s))

class LastNLogs:
    def __init__(self, n=3):
        self.recent_logs = deque(maxlen=n)
        self.table = Table(show_header=False, show_edge=False)

    def get_table(self):
        return self.table
    
    def parse_dependency_line(self, log: str):
        if "━" in log or "" == log or " " == log:
            return
        
        self.recent_logs.append(log) # TODO try unbuffered output, see if progress bar works

        # rich left padding only, need 4 numbers
        table = Table(show_header=False, show_edge=False, padding=(0, 10, 0, 0))
        table.add_column("Column 1", no_wrap=True)

        for recent_log in self.recent_logs:
            table.add_row(f"    {recent_log}")

        self.table = table