import random
from collections import OrderedDict

# Constants
PAGE_TABLE_LEVEL_1_SIZE = 4
PAGE_TABLE_LEVEL_2_SIZE = 4
FRAME_SIZE = 256
TLB_SIZE = 8

LEVEL_1_BITS = 2
LEVEL_2_BITS = 2
OFFSET_BITS = 8

LEVEL_1_MASK = (1 << LEVEL_1_BITS) - 1
LEVEL_2_MASK = (1 << LEVEL_2_BITS) - 1
OFFSET_MASK = (1 << OFFSET_BITS) - 1

page_table = {i: {j: random.randint(0, 15) for j in range(
    PAGE_TABLE_LEVEL_2_SIZE)} for i in range(PAGE_TABLE_LEVEL_1_SIZE)}

tlb = OrderedDict()

def translate_address(virtual_address) -> tuple:
    """
    Translate a virtual address to a physical address using a two-level page table and TLB.
    """
    level_1_index = (virtual_address >> (LEVEL_2_BITS + OFFSET_BITS)) & LEVEL_1_MASK
    # TODO-1: Level 2 index, and Offset using bit manipulation
    level_2_index = (virtual_address >> OFFSET_BITS) & LEVEL_2_MASK
    offset = virtual_address & OFFSET_MASK

    physical_address = None
    is_tlb_hit = False

    if (level_1_index, level_2_index) in tlb:
        # TLB hit logic
        physical_frame = tlb[(level_1_index, level_2_index)]
        tlb.move_to_end((level_1_index, level_2_index))
        print(f"TLB hit for virtual page ({level_1_index}, {level_2_index}).")

        # Calculate physical address
        physical_address = (physical_frame * FRAME_SIZE) + offset
        is_tlb_hit = True

    elif level_1_index in page_table and level_2_index in page_table[level_1_index]:
        # TLB miss. Retrieve frame from page table
        physical_frame = page_table[level_1_index][level_2_index]
        tlb[(level_1_index, level_2_index)] = physical_frame
        print(f"TLB miss. Retrieved from page table for virtual page ({level_1_index}, {level_2_index}).")

        if len(tlb) > TLB_SIZE:
            # Evict least recently used entry
            evicted_page = next(iter(tlb))
            tlb.pop(evicted_page)
            print(f"Evicted page {evicted_page} from TLB (LRU policy).")

        # Calculate physical address
        physical_address = (physical_frame * FRAME_SIZE) + offset
        is_tlb_hit = False
    else:
        # Page fault
        print(f"Page fault! Virtual page ({level_1_index}, {level_2_index}) is not in page table.")

    return physical_address, is_tlb_hit

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
    hit_rate = (tlb_hits / len(access_pattern)) * 100 if len(access_pattern) > 0 else 0
    print(f"TLB Hit Rate: {hit_rate:.2f}%")

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

if __name__ == "__main__":
    main()