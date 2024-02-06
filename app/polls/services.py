def get_sorted_by_ranks(arr):
    result = []
    for q in sorted(arr, key=lambda x: x["total_answered"], reverse=True):
        if len(result) == 0 and not "rank" in q:
            q["rank"] = 1
        elif not "rank" in q:
            if result[-1]["total_answered"] == q["total_answered"]:
                q["rank"] = result[-1]["rank"]
            elif result[-1]["total_answered"] > q["total_answered"]:
                q["rank"] = result[-1]["rank"] + 1
        result.append(q)
    return result
