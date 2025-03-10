import json
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from chains import generate_chain, reflect_chain
from langchain_core.messages import AIMessage
from typing import List, TypedDict
from vector_store import QDRANT_COLLECTION_NAME

class State(TypedDict):
    question: str
    context: List[Document]
    ans: str
    history: List[dict]

def retrieve_node(state, client, embeddings):
    query_vector = embeddings.embed_query(state['question'])
    search_results = client.search(QDRANT_COLLECTION_NAME, query_vector=query_vector, limit=5)
    retrieved_docs = [Document(page_content=result.payload['text']) for result in search_results]
    return {'context': retrieved_docs}

def generation_node(state, prompt):
    docs_content = "\n\n".join(doc.page_content for doc in state['context'])
    messages = prompt.format(question=state['question'], context=docs_content)
    conversation = state.get('history', []) + [{'role': 'user', 'content': state['question']}]
    response = generate_chain.invoke({"messages": conversation + [messages]})
    return {'ans': response, 'history': conversation + [{'role': 'assistant', 'content': response.content}]}

def reflection_node(state):
    res = reflect_chain.invoke({"messages": [state['ans'].content]})
    reflection_output = json.loads(res.content)
    
    if reflection_output.get("output") == "incorrect":
        return {
            "question": reflection_output["suggested_correction"],
            "context": state["context"],
            "history": state["history"]
        }

    return {"ans": AIMessage(content="correct"), "history": state["history"]}

def should_continue(state):
    return END if state['ans'] == "correct" else generation_node

def build_workflow(client, embeddings, prompt):
    builder = StateGraph(State)
    memory = MemorySaver()
    
    builder.add_node('retrieve', lambda state: retrieve_node(state, client, embeddings))
    builder.add_node('generate', lambda state: generation_node(state, prompt))
    builder.add_node('reflect', reflection_node)
    
    builder.add_edge(START, 'retrieve')
    builder.add_edge('retrieve', 'generate')
    builder.add_edge('generate', 'reflect')
    
    builder.add_conditional_edges('reflect', should_continue)
    
    return builder.compile(memory)

