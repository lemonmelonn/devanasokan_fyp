# —— Kadane's Algorithm ——————————————————————————————————————

def kadane(nums: list) -> int:
    current_sum = nums[0]
    max_sum     = nums[0]

    for num in nums[1:]:  # Start from the second element
        current_sum = max(num, current_sum + num)

        if current_sum > max_sum:
            max_sum = current_sum

    return max_sum

worstcase = [-15.50, -25.00, 10.20, -40.00, 65.80, -80.00, 20.15, -55.30, 95.00, -110.00, 30.45, -150.00, 12.00, -18.50, 45.20, -5.10, 75.30, -200.00, 15.40, -30.00]
print(kadane(worstcase))