import heapq
from pathlib import Path


def read_line(the_file, file_num: int):
    """
    reads the next line from one partial index file. -> returns a tuple
    """
    line = the_file.readline()

    # return none if theres nothing left to read
    if not line:
        return None

    # each document entry is doc_id:times_in_doc:times_in_important_tags
    term, postings = line.rstrip("\n").split("\t", 1) #
    return (term, file_num, postings)


def merge_partial_indexes(index_dir: str, output_filepath: str) -> None:
    """
    Combines all partial index into one final index
    """
    # find the partial files and sort them by their number (0, 1, 2, 3 ..)
    partial_files = sorted(Path(index_dir).glob("partial_*.txt"),
                           key=lambda p: int(p.stem.split("_")[1]))

    # open all the partial files at the same time
    # ((partial0_term, 0, x:y:z), (partial1_term, 1, x:y:z), (partial2_term, 2, x:y:z) ...)
    files = [open(p, "r", encoding="utf-8") for p in partial_files]

    # start the heap with the first line from every file (sort by term first then file number)
    heap = []
    for i, f in enumerate(files):
        entry = read_line(f, i)
        if entry:
            heapq.heappush(heap, entry)

    with open(output_filepath, "w", encoding="utf-8") as out:
        # keep going until every file has been fully read (until heap empty)
        while heap:
            # pop the smallest term and stat a list of postings for it
            term, i, postings = heapq.heappop(heap)
            all_postings = [postings]

            # we used a line from file i, so read next line and push into the heap
            entry = read_line(files[i], i)
            if entry:
                heapq.heappush(heap, entry)

            # if the next smallest term is same as current, also take it and add to postings
            # goes in order as it goe lowest terms -> file numbers
            while heap and heap[0][0] == term:
                _, j, postings = heapq.heappop(heap)
                all_postings.append(postings)

                # refill the heap from the file we just took from
                entry = read_line(files[j], j)
                if entry:
                    heapq.heappush(heap, entry)

            # write the term once with all postings from every file joined together
            out.write(f"{term}\t{','.join(all_postings)}\n")

    # close all the partial files when we're done
    for f in files:
        f.close()


if __name__ == "__main__":
    merge_partial_indexes("index_output", "index_output/final_index.txt")
