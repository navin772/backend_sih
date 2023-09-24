from datasketch import MinHash, MinHashLSH
import time

start = time.time()

with open("text_files/wijesekera2018.txt", "r") as text_file:
    sentences = text_file.readlines()
    sentences = [sentence.strip() for sentence in sentences]
    set1 = []
    for sentence in sentences:
        words = sentence.split(" ")
        for word in words:
            set1.append(word)

with open("text_files/wijesekera2018.txt", "r") as text_file:
    sentences = text_file.readlines()
    sentences = [sentence.strip() for sentence in sentences]
    set2 = []
    for sentence in sentences:
        words = sentence.split(" ")
        for word in words:
            set2.append(word)

# with open("text_files/app_permission3.txt", "r") as text_file:
#     sentences = text_file.readlines()
#     sentences = [sentence.strip() for sentence in sentences]
#     set3 = []
#     for sentence in sentences:
#         words = sentence.split(" ")
#         for word in words:
#             set3.append(word)

m1 = MinHash(num_perm=128)
m2 = MinHash(num_perm=128)
# m3 = MinHash(num_perm=128)
for d in set1:
    m1.update(d.encode('utf8'))
for d in set2:
    m2.update(d.encode('utf8'))
# for d in set3:
#     m3.update(d.encode('utf8'))

i = 0.00
while i < 0.99:

    # Create LSH index
    threshold = i
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    lsh.insert("m2", m2)
    # lsh.insert("m3", m3)
    result = lsh.query(m1)
    # if len(result) > 0:
    #     print("Approximate neighbours with Jaccard similarity > {thresh}".format(thresh=threshold), result)
    print("Approximate neighbours with Jaccard similarity > {thresh}".format(thresh=threshold), result)
    i += 0.01


end = time.time()
print("Time taken: ", end-start)