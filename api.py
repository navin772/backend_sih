# from flask import Flask, request, jsonify
from pypdf import PdfReader
# from datasketch import MinHash, MinHashLSH

# app = Flask(__name__)

# @app.route('/calculate_similarity', methods=['POST'])
# def calculate_similarity():
#     try:
#         # Receive PDF file from the client
#         pdf_file = request.files['pdf_file']

#         # Save the received PDF to a file
#         pdf_file.save("input.pdf")

#         # Extract text from the PDF
#         reader = PdfReader("input.pdf")
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()

#         # Split the text into sets of words
#         sentences = text.split('\n')
#         set1 = []
#         for sentence in sentences:
#             words = sentence.split(" ")
#             for word in words:
#                 set1.append(word)

#         # Read other sets (set2 and set3) from your text files as you did before

#         # Create MinHash objects and calculate similarity
#         m1 = MinHash(num_perm=128)
#         m2 = MinHash(num_perm=128)
#         m3 = MinHash(num_perm=128)
#         for d in set1:
#             m1.update(d.encode('utf8'))
#         # Update m2 and m3 with your other sets
#         for d in set1:
#             m2.update(d.encode('utf8'))

#         for d in set1:
#             m3.update(d.encode('utf8'))
            
#         i = 0.02
#         similarity_scores = {}

#         while i < 0.99:
#             # Create LSH index
#             threshold = i
#             lsh = MinHashLSH(threshold=threshold, num_perm=128)
#             lsh.insert("m2", m2)
#             lsh.insert("m3", m3)
#             result = lsh.query(m1)
#             similarity_scores[threshold] = len(result)
#             i += 0.01

#         return jsonify(similarity_scores)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from datasketch import MinHash, MinHashLSH
import pymongo

app = Flask(__name__)

# Initialize MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["minhash_db"] 
collection = db["minhash_collection"] 

# Create an index on the 'minhash' field
collection.create_index([("minhash", pymongo.ASCENDING)])

def find_first_occurrence(scores):
    for key in sorted(scores.keys(), reverse=True):
        if scores[key]:
            return key
    return None

@app.route('/store_minhash', methods=['POST'])
def store_minhash():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400

        # Get the uploaded PDF file
        pdf_file = request.files['pdf_file']

        # Read the PDF file and create a MinHash
        m = MinHash(num_perm=128)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        sentences = text.split('\n')
        for sentence in sentences:
            words = sentence.split(" ")
            for word in words:
                m.update(word.encode('utf8'))

        # Convert the NumPy array to a Python list
        minhash_list = m.digest().tolist()

        # Store the MinHash list in MongoDB
        result = collection.insert_one({"minhash": minhash_list})

        return jsonify({"message": "MinHash stored successfully", "minhash_id": str(result.inserted_id)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/plag_score', methods=['POST'])
def calculate_similarity():
    try:
        # Check if the 'pdf_file' key is in the request's files
        if 'pdf_file' not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400

        # Get the uploaded PDF file
        pdf_file = request.files['pdf_file']

        # Read the PDF file and create a MinHash
        m1 = MinHash(num_perm=128)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        sentences = text.split('\n')
        for sentence in sentences:
            words = sentence.split(" ")
            for word in words:
                m1.update(word.encode('utf8'))

        i = 0.1
        similarity_scores = {}

        while i < 0.99:
            # Create LSH index
            threshold = i
            lsh = MinHashLSH(threshold=threshold, num_perm=128)

            # Query MinHashes stored in MongoDB
            for document in collection.find():
                minhash_id = str(document["_id"])
                minhash = document["minhash"]
                lsh.insert(minhash_id, MinHash(num_perm=128, hashvalues=minhash))

            # Query for similarity by counting the number of matches
            result = lsh.query(m1)
            similarity_scores[threshold] = result
            i += 0.01

        score = {"plag_score": round(find_first_occurrence(similarity_scores)*100)}
        return jsonify(score)
        # return jsonify(round(find_first_occurrence(similarity_scores)*100))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
