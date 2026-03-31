from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function
from query_data import query_rag
from db_utils import get_or_build_bot_db_path

embedding_function = get_embedding_function()
db = Chroma(persist_directory='chroma_FAQs', embedding_function=embedding_function)

# Get all documents to extract all questions
all_docs = db.get()
questions = []

for i, doc_content in enumerate(all_docs['documents']):
    if 'Question:' in doc_content:
        # Extract question from the content
        lines = doc_content.split('\n')
        for line in lines:
            if line.strip().startswith('Question:'):
                question = line.replace('Question:', '').strip()
                questions.append(question)
                break

print("=" * 80)
print(f"FOUND {len(questions)} QUESTIONS IN DATABASE")
print("=" * 80)

# Test each question
db_path = get_or_build_bot_db_path('FAQs')
issues = []

for i, question in enumerate(questions, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}: {question}")
    print('='*60)
    
    # Get similarity search results
    results = db.similarity_search_with_score(question, k=3)
    
    print("SIMILARITY RESULTS:")
    best_match = None
    best_score = float('inf')
    
    for j, (doc, score) in enumerate(results):
        print(f"  {j+1}. Score: {score:.4f}")
        if score < best_score:
            best_score = score
            best_match = doc
            if 'Question:' in doc.page_content:
                # Extract question from result
                lines = doc.page_content.split('\n')
                for line in lines:
                    if line.strip().startswith('Question:'):
                        result_question = line.replace('Question:', '').strip()
                        print(f"     Question: {result_question}")
                        break
    
    # Get LLM response
    try:
        llm_answer = query_rag(question, db_path)
        print(f"LLM ANSWER: {llm_answer}")
        
        # Check for issues
        if 'out of scope' in llm_answer.lower():
            if best_score < 0.3:  # Should have found a good match
                issues.append({
                    'question': question,
                    'best_score': best_score,
                    'llm_answer': llm_answer,
                    'issue': 'LLM said out of scope despite good match'
                })
                print("❌ ISSUE: LLM said out of scope despite good match!")
            else:
                print("✅ LLM correctly said out of scope (no good match)")
        else:
            if 'https://' in llm_answer and len(llm_answer.strip()) < 50:
                print("⚠️  WARNING: LLM only provided link")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        issues.append({
            'question': question,
            'error': str(e),
            'issue': 'LLM processing error'
        })

print(f"\n{'='*80}")
print("SUMMARY OF ISSUES")
print('='*80)

for issue in issues:
    print(f"\n❌ Question: {issue.get('question', 'Unknown')}")
    print(f"   Issue: {issue.get('issue', 'Unknown')}")
    if 'best_score' in issue:
        print(f"   Best Match Score: {issue['best_score']:.4f}")
    if 'llm_answer' in issue:
        print(f"   LLM Answer: {issue['llm_answer']}")
    if 'error' in issue:
        print(f"   Error: {issue['error']}")

print(f"\nTotal Issues Found: {len(issues)}")
