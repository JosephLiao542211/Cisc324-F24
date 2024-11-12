import random
from collections import OrderedDict

# Constants
# Size of the first-level page table (number of entries)
PAGE_TABLE_LEVEL_1_SIZE = 4
# Size of the second-level page table (number of entries per level-1 entry)
PAGE_TABLE_LEVEL_2_SIZE = 4
FRAME_SIZE = 256               # Frame size in bytes
TLB_SIZE = 8                   # Number of entries in the TLB cache

# Bit mask and shift values for extracting parts of the virtual address
# Number of bits for Level 1 index (4 entries -> 2 bits)
LEVEL_1_BITS = 2
# Number of bits for Level 2 index (4 entries -> 2 bits)
LEVEL_2_BITS = 2
# Number of bits for offset within a frame (256 bytes -> 8 bits)
OFFSET_BITS = 8

# Mask values
LEVEL_1_MASK = (1 << LEVEL_1_BITS) - 1
LEVEL_2_MASK = (1 << LEVEL_2_BITS) - 1
OFFSET_MASK = (1 << OFFSET_BITS) - 1

# Simulated Two-Level Page Table
page_table = {i: {j: random.randint(0, 15) for j in range(
    PAGE_TABLE_LEVEL_2_SIZE)} for i in range(PAGE_TABLE_LEVEL_1_SIZE)}

# Simulated TLB using OrderedDict to implement LRU
tlb = OrderedDict()

# Function to translate a virtual address to a physical address using bit manipulation


def translate_address(virtual_address) -> tuple:
    """
    Translate a virtual address to a physical address using a two-level page table and TLB.
    Returns a tuple with the physical address and a boolean indicating if it was a TLB hit.
    """
    level_1_index = (virtual_address >> (
        LEVEL_2_BITS + OFFSET_BITS)) & LEVEL_1_MASK
    # TODO-1: Level 2 index, and Offset using bit manipulation. In the next two lines, replace the None values with the correct bit manipulation code
    level_2_index = None  # Replace with the correct bit manipulation code
    offset = None  # Replace with the correct bit manipulation code

    physical_address = None  # you don't need to change this line
    is_tlb_hit = False  # you don't need to change this line

    if (level_1_index, level_2_index) in tlb:
        # Placeholder for TLB hit logic
        physical_frame = None   # TODO-2: Replace this line with TLB hit retrieval code

        # Update TLB for LRU by moving accessed item to the end (you don't have to do anything here)
        tlb.move_to_end((level_1_index, level_2_index))
        print(f"TLB hit for virtual page ({level_1_index}, {level_2_index}).")

        # TODO-2.1: Calculate the physical address in the next line using the frame number and offset
        physical_address = None
        is_tlb_hit = None  # TODO-2.2: Set the is_tlb_hit flag

    elif level_1_index in page_table and level_2_index in page_table[level_1_index]:
        # TODO-3: TLB miss. Update next line to retrieve the frame from the two-level page table
        physical_frame = None  # Replace with page table retrieval code
        tlb[(level_1_index, level_2_index)] = physical_frame
        print(f"TLB miss. Retrieved from page table for virtual page ({
              level_1_index}, {level_2_index}).")

        if len(tlb) > TLB_SIZE:
            evicted_page = None  # TODO-4: If TLB is full, evict the least recently used entry
            print(f"Evicted page {evicted_page} from TLB (LRU policy).")

        # TODO-4.1: Using physical_frame obtained in TODO-3, in the next line, calculate the physical address using the frame number and offset
        physical_address = None
        is_tlb_hit = None  # TODO-4.2: Set the is_tlb_hit flag
    else:
        # Page fault (not in the page table)
        print(f"Page fault! Virtual page ({level_1_index}, {
              level_2_index}) is not in page table.")

    return physical_address, is_tlb_hit

# Function to simulate address access pattern and calculate TLB performance


def simulate_address_access(access_pattern):
    tlb_hits = 0
    tlb_misses = 0

    for virtual_address in access_pattern:
        physical_address, was_tlb_hit = translate_address(virtual_address)
        if was_tlb_hit:
            tlb_hits += 1
        else:
            tlb_misses += 1

    print("\nSimulation Results:")
    print(f"Total Accesses: {len(access_pattern)}")
    print(f"TLB Hits: {tlb_hits}")
    print(f"TLB Misses: {tlb_misses}")
    hit_rate = float('NaN')  # TODO-5: Calculate and print the TLB hit rate
    print(f"TLB Hit Rate: {hit_rate:.2f}%")

# Main function to run multiple test cases with different access patterns


def main():
    print("Test Case 1: Sequential Access Pattern")
    sequential_access_pattern = list(range(
        0, PAGE_TABLE_LEVEL_1_SIZE * PAGE_TABLE_LEVEL_2_SIZE * FRAME_SIZE, FRAME_SIZE))
    simulate_address_access(sequential_access_pattern)

    print("\nTest Case 2: Random Access Pattern")
    random_access_pattern = [random.randint(
        0, PAGE_TABLE_LEVEL_1_SIZE * PAGE_TABLE_LEVEL_2_SIZE * FRAME_SIZE - 1) for _ in range(50)]
    simulate_address_access(random_access_pattern)

    print("\nTest Case 3: Repeated Access to Small Subset")
    repeated_access_pattern = [0, FRAME_SIZE, 2 *
                               FRAME_SIZE, 0, FRAME_SIZE, 2 * FRAME_SIZE] * 5
    simulate_address_access(repeated_access_pattern)


# Run the main function
if __name__ == "__main__":
    main()
