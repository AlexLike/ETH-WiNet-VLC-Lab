from time import sleep, time_ns
from scipy.spatial import distance
from serial import Serial
from shared.byte_coders import *
from random import choices
from string import ascii_lowercase
from numpy import mean, std, sqrt
from scipy import stats

class Measurer():
  """An object that performs the measurements and logs them to console and an appropriately named file."""

  def __init__(self, distance_cm: int, payload_size: int, max_running_time_s: int, serial: Serial):
    self.distance_cm = distance_cm
    self.payload_size = payload_size
    self.running_time_ns = max_running_time_s * 1_000_000_000
    self.s = serial
    self.elapsed_time_ns = 0
    self.sent_payloads = 0
    self.acknowledged_payloads = 0
    self.delays = []

  def receive(self):
    input = dec(self.s.read_until()).strip()
    if (input == "m[R,A]"):
      self.acknowledged_payloads += 1
    return input 

  def measure(self):
    payload_str = "".join(choices(ascii_lowercase, k=self.payload_size))
    bytes_to_send = enc(f"m[{payload_str}\0,AB]\n")
    while self.sent_payloads < 30 and self.elapsed_time_ns < self.running_time_ns:
      sleep(0.01)
      t_0 = time_ns()
      self.s.write(bytes_to_send)
      while self.receive()  != "m[D]":
        pass
      t_1 = time_ns()
      t = t_1 - t_0
      self.elapsed_time_ns += t
      self.sent_payloads += 1
      self.delays.append(t)
    # Wait for the last ACK
    while self.receive() != "":
      pass
  
  def print_and_save_stats(self):
    running_time_s = self.running_time_ns / 1_000_000_000
    success_rate = self.acknowledged_payloads / self.sent_payloads
    throughput = self.acknowledged_payloads * self.payload_size / running_time_s
    mean_delay_s = mean(self.delays) / 1_000_000_000
    standard_deviation_delay_s = std(self.delays) / 1_000_000_000
    confidence_interval = stats.t.interval(alpha=0.98, df=self.sent_payloads-1, loc=mean_delay_s, scale=standard_deviation_delay_s / sqrt(self.sent_payloads))

    print("-" * 20)
    print(f"Distance: {self.distance_cm}cm")
    print(f"Total running time: {running_time_s}s")
    print(f"Acknowledged {self.acknowledged_payloads} / {self.sent_payloads} payloads.")
    print(f"=> Success rate: {success_rate * 100}%")
    print(f"Throughput: {throughput}B/s")
    print(f"Mean Delay: {mean_delay_s}s")
    print(f"Standard Deviation in Delays: {standard_deviation_delay_s}s")
    print(f"98% Confidence Interval: {confidence_interval}s")

    with open(f"results/{self.distance_cm}cm-{self.payload_size}B-results.csv", "w") as out_file:
      (cl, cr) = confidence_interval
      out_file.write(", ".join([str(i) for i in [success_rate, throughput, mean_delay_s, standard_deviation_delay_s, cl, cr]]) + "\n")
      out_file.write(", ".join([str(i) for i in self.delays]))

