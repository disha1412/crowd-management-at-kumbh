import heapq
import random
from collections import deque

class CircularQueue:
    """Circular Queue for efficient O(1) enqueue & dequeue operations."""
    def __init__(self, size):
        self.queue = [None] * size
        self.front = self.rear = -1
        self.size = size

    def enqueue(self, item):
        if (self.rear + 1) % self.size == self.front:
            return False  # Queue is full
        if self.front == -1:
            self.front = 0
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = item
        return True

    def dequeue(self):
        if self.front == -1:
            return None  # Queue is empty
        item = self.queue[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.size
        return item

    def is_empty(self):
        return self.front == -1

class Person:
    def __init__(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.status = "Waiting"  # Possible states: Waiting, Moving, Dipping, Exiting
        self.slot = None
        self.exit_time = None

class RiverDipping:
    def __init__(self, n_slots, dip_time):
        self.n = n_slots  # Number of dipping slots
        self.dip_time = dip_time  # Time per dip
        self.slot_queue = [(0, i) for i in range(n_slots)]  # (Time available, Slot ID)
        heapq.heapify(self.slot_queue)  # Min-heap for slot management
        self.waiting_queue = CircularQueue(1000000)  # Circular queue for large k
        self.event_queue = []  # Event queue to simulate arrivals & departures
        self.time = 0  # Global clock
    
    def person_arrives(self, person):
        """Handles a new person arriving."""
        print(f"[Time {self.time}] Person {person.id} arrives and waits.")
        self.waiting_queue.enqueue(person)
        self.process_queue()

    def process_queue(self):
        """Assigns available slots to waiting people in batches."""
        batch_size = min(self.n, 10)  # Process up to 10 people at once
        batch = []
        
        while not self.waiting_queue.is_empty() and len(self.slot_queue) >= batch_size:
            for _ in range(batch_size):
                available_time, slot = heapq.heappop(self.slot_queue)
                person = self.waiting_queue.dequeue()
                batch.append((person, slot, available_time))
        
        for person, slot, available_time in batch:
            self.assign_slot(person, slot, available_time)

    def assign_slot(self, person, slot, available_time):
        """Assigns a person to a slot and schedules their exit."""
        self.time = max(self.time, available_time)
        person.status = "Dipping"
        person.slot = slot
        person.exit_time = self.time + self.dip_time

        print(f"[Time {self.time}] Person {person.id} moves to Slot {slot} and starts dipping.")
        heapq.heappush(self.event_queue, (person.exit_time, person))  # Schedule exit

    def process_events(self):
        """Processes exit events and moves the queue forward."""
        while self.event_queue and self.event_queue[0][0] <= self.time:
            _, person = heapq.heappop(self.event_queue)
            self.free_slot(person)

    def free_slot(self, person):
        """Handles a person exiting the river and making space for new arrivals."""
        person.status = "Exiting"
        print(f"[Time {self.time}] Person {person.id} leaves Slot {person.slot} and exits.")

        heapq.heappush(self.slot_queue, (self.time, person.slot))  # Slot becomes available
        self.process_queue()  # Immediately assign the next waiting person

    def simulate(self, num_people, interval=1):
        """Simulates the entire process of people arriving, dipping, and exiting."""
        for i in range(num_people):
            arrival_time = self.time + random.randint(0, interval)  # Stagger arrivals
            person = Person(i + 1, arrival_time)
            self.person_arrives(person)
            self.process_events()  # Process events as soon as people enter

        self.process_events()  # Final cleanup to process remaining exits

# Run Simulation
river = RiverDipping(n_slots=10, dip_time=5)  # 10 slots, each person dips for 5 seconds
river.simulate(num_people=500000, interval=2)  # Large k test
