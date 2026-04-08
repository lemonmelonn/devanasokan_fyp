# —— Boyer-Moore Majority Vote Algorithm ——————————————————————————————————————

def boyer_moore_majority(nums: list) -> int | None:
    # Phase 1: Find candidate
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    # Phase 2: Verify candidate
    verify_count = 0
    for num in nums:
        if num == candidate:
            verify_count += 1

    if verify_count > len(nums) // 2:
        return candidate
    return None  # No majority element exists