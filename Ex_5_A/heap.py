import heapq

if __name__ == '__main__':
    heap = []

    heapq.heappush(heap, 1)
    heapq.heappush(heap, 7)
    heapq.heappush(heap, 3)
    heapq.heappush(heap, 5)

    while heap:
        print(heapq.heappop(heap))
